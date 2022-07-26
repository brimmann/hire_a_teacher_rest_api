from pprint import pprint

from django.db.models import Q

from jobs.models import Job
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

    matched_jobs = match_jobs(search_map)
    temp = []
    if matched_jobs is None:
        return {"relevant_jobs": {}}
    for matched_job in matched_jobs:
        temp.append(matched_job.values()[0])
    print(temp)

    return {"relevant_jobs": temp}


def search_jobs(search_string):
    if len(search_string) < 1:
        return {"matched_jobs": []}
    SearchMapGenAdv.generate(search_string)
    search_map = SearchMapGenAdv.getMap()

    matched_jobs = match_jobs(search_map)
    temp = []
    if matched_jobs is None:
        return {"matched_jobs": []}

    for matched_job in matched_jobs:
        temp.append(matched_job.values()[0])
    print(temp)

    return {"matched_jobs": temp}


def match_jobs(search_map):
    jobs_mini = list(Job.objects.values("id", "title", "description", "tags"))
    print("to", search_map)
    match_job_ids = []
    matched_jobs = []

    for job in jobs_mini:
        for key, section in job.items():
            if key != "id":
                for keyword in search_map["keywords"]:
                    if keyword.casefold() in section.casefold():
                        print("match this", keyword)
                        match_job_ids.append(job["id"])

    match_job_ids = list(set(match_job_ids))

    if len(match_job_ids) < 1:
        return None

    for job_id in match_job_ids:
        matched_jobs.append(Job.objects.filter(id=job_id))

    return matched_jobs


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
        print(tagged_map)
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

        print(cleaned_map)

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
