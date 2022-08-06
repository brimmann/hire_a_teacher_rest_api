from pprint import pprint

import arrow
from django.db.models import Q
from django.forms import model_to_dict

from jobs.models import Job, Application, Interview
from resume.models import RelSearchConfig, Resume
from resume.search_map import SearchMapGen

import nltk
import requests
import json

SEARCH_BASE_URL = "api.tomtom.com/search/2/search"
API_KEY = "q1TIKeqJMLhzvbUmQTKP9g6t3Q2jTgzk"
ENTRY_TYPE_SET = "Municipality,MunicipalitySubdivision,CountrySecondarySubdivision,CountryTertiarySubdivision"


def get_non_awarded_jobs(org_id):
    jobs = Job.objects.filter(org=org_id)
    jobs = jobs.filter(Q(status="active") | Q(status="inactive"))
    return list(jobs.values())


def get_relevant_jobs(teacher_id):
    search_map = SearchMapGen.get_search_map(teacher_id)
    if search_map is None:
        return {"error": "Resume relevant search configuration is not found"}

    matched_jobs = match_jobs(search_map, teacher_id)
    temp = []
    if matched_jobs is None:
        return {"relevant_jobs": {}}
    for matched_job in matched_jobs:
        temp.append(matched_job.values()[0])

    return {"relevant_jobs": temp}


def search_jobs(search_string, teacher_id):
    if len(search_string) < 1:
        return {"matched_jobs": []}
    SearchMapGenAdv.generate(search_string)
    search_map = SearchMapGenAdv.getMap()

    matched_jobs = match_jobs(search_map, teacher_id)
    temp = []
    if matched_jobs is None:
        return {"matched_jobs": []}

    for matched_job in matched_jobs:
        temp.append(matched_job.values()[0])

    return {"matched_jobs": temp}


def search_teachers(search_string):
    if len(search_string) < 1:
        return {"matched_teachers": []}
    SearchMapGenAdv.generate(search_string)
    search_map = SearchMapGenAdv.getMap()
    rel_search_configs = RelSearchConfig.objects.all()
    result_ids = []
    if "teacher".casefold() in search_map["keywords"]:
        search_map["keywords"].remove("teacher".casefold())

    for rel_search_config in rel_search_configs:
        for keyword in rel_search_config.keywords:
            for word in search_map["keywords"]:
                if keyword.casefold() in word.casefold():
                    result_ids.append(rel_search_config.resume_id)

    if len(result_ids) < 1:
        return {"matched_teachers": []}

    result = []
    for result_id in result_ids:
        resume = Resume.objects.get(user_id=result_id)
        result.append(
            {
                "teacher_id": resume.user_id,
                "full_name": resume.user.teacherdetail.full_name,
                "headline": resume.heading,
                "brief": resume.intro,
            }
        )

    return {"matched_teachers": result}


def match_jobs(search_map, teacher_id):
    jobs = Job.objects.exclude(Q(status__exact="interviewing") | Q(status__exact="awarded"))

    jobs_mini = list(jobs.values("id", "title", "description", "tags"))
    match_job_ids = []
    matched_jobs = []

    for job in jobs_mini:
        for key, section in job.items():
            if key != "id":
                for keyword in search_map["keywords"]:
                    if keyword.casefold() in section.casefold():
                        match_job_ids.append(job["id"])

    match_job_ids = list(set(match_job_ids))

    applications = Application.objects.all()

    for application in applications:
        for match_job_id in match_job_ids:
            if (
                application.job_id == match_job_id
                and application.teacher_id == teacher_id
            ):
                match_job_ids.remove(match_job_id)

    if len(match_job_ids) < 1:
        return None

    for job_id in match_job_ids:
        matched_jobs.append(Job.objects.filter(id=job_id))

    return matched_jobs


def get_applications_teacher(teacher_id):
    applications = Application.objects.all()
    result = []

    for application in applications:
        if application.teacher_id == teacher_id:
            single_result = model_to_dict(application.job)
            single_result["app_id"] = application.id
            single_result["date_applied"] = application.date_applied
            result.append(single_result)

    print(result)
    if len(result) < 1:
        return {"applications": []}

    return {"applications": result}


class SearchMapGenAdv:
    __ready_map = None
    __raw_map = None

    def __init__(self, direct=False):
        if not direct:
            raise ValueError(
                "Use factory method, SearchMapGenAdv.generate(search_string)"
            )

    @classmethod
    def generate(cls, search_string):
        cls.__raw_map = search_string
        instance = cls(True)
        instance.__tokenize()
        instance.__separate_keywords_and_places()
        cls.__setMap(instance.__raw_map)

    @classmethod
    def getMap(cls):
        return cls.__ready_map

    @classmethod
    def __setMap(cls, ready_map):
        cls.__ready_map = ready_map

    def __tokenize(self):
        self.__raw_map = self.__raw_map.split(" ")
        self.__raw_map = set(self.__raw_map)
        self.__raw_map = list(self.__raw_map)
        tagged_map = nltk.pos_tag(self.__raw_map)
        cleaned_map = []
        for el in tagged_map:
            if (
                el[1] == "NN"
                or el[1] == "NNS"
                or el[1] == "NNP"
                or el[1] == "NNPS"
                or el[1] == "JJ"
                or el[1] == "NNPS"
            ):
                cleaned_map.append(el[0])
        self.__raw_map = cleaned_map

    def __separate_keywords_and_places(self):
        words = self.__raw_map
        places = []
        results = []

        for word in words:
            response = requests.get(
                f"https://{SEARCH_BASE_URL}/{word}.json?key={API_KEY}&typeahead=true&countrySet=PAK&entityTypeSet={ENTRY_TYPE_SET}"
            )
            if response.json()["summary"]["numResults"] > 0:
                for result in response.json()["results"]:
                    entity_type = (
                        result["entityType"][0].lower() + result["entityType"][1:]
                    )
                    results.append(result["address"][entity_type])

        for result in results:
            for word in words:
                if result.casefold() == word.casefold():
                    places.append(result)
                    words.remove(word)

        keywords = words

        self.__raw_map = {"places": places, "keywords": keywords}


def get_org_apps(org_id):
    applications = Application.objects.filter(job__org_id=org_id)
    result = []

    for application in applications:
        unified_object = {
            "job": model_to_dict(application.job),
            "app": model_to_dict(application),
        }
        unified_object["app"][
            "teacher_name"
        ] = application.teacher.teacherdetail.full_name
        result.append(unified_object)

    if len(result) < 1:
        return {"applications": []}

    return {"applications": result}


def get_org_apps_job_based(org_id, job_id):
    applications = Application.objects.filter(job__org_id=org_id).filter(job_id=job_id)
    result = {"job": model_to_dict(Job.objects.get(id=job_id)), "apps": []}

    for application in applications:
        teacher_name = application.teacher.teacherdetail.full_name
        app = model_to_dict(application)
        app["teacher_name"] = teacher_name
        result["apps"].append(app)

    if len(result["apps"]) < 1:
        return {"applications": {}}

    return result


def get_interviews_teacher(teacher_id):
    interviews = Interview.objects.filter(teacher_id=teacher_id)
    result = []

    for interview in interviews:
        mod_interview = model_to_dict(interview)
        mod_interview["time"] = arrow.get(
            mod_interview["time"], "YYYY-MM-DD HH:mm A"
        ).format("dddd, MMMM D, YYYY - hh:mm A")
        temp = {
            "interview": mod_interview,
            "job": model_to_dict(interview.job),
        }
        result.append(temp)

    if len(result) < 1:
        return {"interviews": []}

    return {"interviews": result}


def get_interviews_org(org_id):
    interviews = Interview.objects.filter(job__org_id=org_id)
    result = []

    for interview in interviews:
        mod_interview = model_to_dict(interview)
        mod_interview["time"] = arrow.get(
            mod_interview["time"], "YYYY-MM-DD HH:mm A"
        ).format("dddd, MMMM D, YYYY - hh:mm A")
        temp = {
            "interview": mod_interview,
            "job": model_to_dict(interview.job),
        }
        result.append(temp)

    if len(result) < 1:
        return {"interviews": []}

    print(result)

    return {"interviews": result}
