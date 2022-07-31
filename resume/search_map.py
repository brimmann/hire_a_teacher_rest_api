from django.forms import model_to_dict
import nltk


from hire_a_teacher_rest_api import settings
from resume.models import Resume, Skill, Education, Experience, RelSearchConfig
import pickle


# class Singleton(type):
#     _instances = {}
#
#     def __call__(cls, *args, **kwargs):
#         if cls not in cls._instances:
#             cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
#             return cls._instances[cls]
#         else:
#             raise SingletonException('Instance already exist, singleton classes can only have one instance')


class SearchMapGen(object):
    __ready_map = None
    __raw_map = None
    __user_id = None

    def __init__(self, direct=False):
        if not direct:
            raise ValueError("Use factory method, SearchMapGen.generate(user_id)")

    @classmethod
    def generate(cls, user_id):
        instance = cls(True)
        cls.__user_id = user_id
        instance.__get_raw_data()
        instance.__structure_raw_data()
        instance.__pack_data()
        instance.__store_map()

    def __get_raw_data(self):
        resume = Resume.objects.get(user_id=self.__user_id)
        resume_id = resume.user_id
        experiences = Experience.objects.filter(resume_id=resume_id)
        skills = Skill.objects.filter(resume_id=resume_id)
        educations = Education.objects.filter(resume_id=resume_id)
        self.__raw_map = {
            "heading": resume.heading,
            "address": resume.address,
            "exp_titles": experiences.values_list("title", flat=True),
            "edu_fields_of_study": educations.values_list("field_of_study", flat=True),
            "skills": skills.values_list("skill", flat=True),
        }

    def __structure_raw_data(self):
        raw_map = self.__raw_map
        exp_titles = " ".join(list(raw_map["exp_titles"]))
        edu_fields_of_study = " ".join(list(raw_map["edu_fields_of_study"]))
        skills = " ".join(list(raw_map["skills"]))
        self.__raw_map = {
            "heading": [
                word for word in raw_map["heading"].split(" ") if len(word) > 1
            ],
            "city": raw_map["address"],
            "exp_titles": [word for word in exp_titles.split(" ") if len(word) > 1],
            "edu_fields_of_study": [
                word for word in edu_fields_of_study.split(" ") if len(word) > 1
            ],
            "skills": [word for word in skills.split(" ") if len(word) > 1],
        }

    def __pack_data(self):
        raw_map = self.__raw_map
        combined_data = (
            raw_map["heading"]
            + raw_map["exp_titles"]
            + raw_map["edu_fields_of_study"]
            + raw_map["skills"]
        )

        set_of_combined_data = set(combined_data)

        tagged_data = nltk.pos_tag(list(set_of_combined_data))
        cleaned_data = []

        for el in tagged_data:
            if el[1] == "NN" or el[1] == "NNS" or el[1] == "NNP" or el[1] == "NNPS":
                cleaned_data.append(el[0])

        print(cleaned_data)
        final_data = {"keywords": list(cleaned_data), "city": raw_map["city"]}
        self.__ready_map = final_data

    def __store_map(self):
        record = RelSearchConfig.objects.filter(resume_id=self.__user_id)
        if "teacher".casefold() in self.__ready_map["keywords"]:
            self.__ready_map["keywords"].remove("teacher".casefold())
        if not record:
            resume = Resume.objects.get(user_id=self.__user_id)
            record = RelSearchConfig(
                resume=resume,
                keywords=self.__ready_map["keywords"],
                city=self.__raw_map["city"],
            )
            record.save()
            return
        record.update(
            keywords=self.__ready_map["keywords"], city=self.__raw_map["city"]
        )

    @staticmethod
    def get_search_map(user_id):
        try:
            rel_search_config = RelSearchConfig.objects.get(resume_id=user_id)
            return model_to_dict(rel_search_config, fields=["keywords", "city"])
        except RelSearchConfig.DoesNotExist:
            return None
