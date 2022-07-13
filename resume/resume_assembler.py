from resume.models import Resume, Experience, Education, Language, Skill
from users.models import User, TeacherDetail


class ResumeAssembler:
    resume_dict = {}
    intro = None
    exp = None
    edu = None
    lang = None
    skills = None

    def __init__(self, user_id):
        self.user_id = user_id

    def fetch_intro(self):
        user_details = TeacherDetail.objects.get(user_id=self.user_id)
        resume = Resume.objects.get(user_id=self.user_id)
        self.intro = {
            "fullName": user_details.full_name,
            "headline": resume.heading,
            "phoneNumber": user_details.phone_number,
            "emailAddress": resume.email,
            "address": resume.address,
            "brief": resume.intro,
        }

    def fetch_exp(self):
        self.exp = list(Experience.objects.filter(resume_id=self.user_id).values())

    def fetch_edu(self):
        self.edu = list(Education.objects.filter(resume_id=self.user_id).values())

    def fetch_lang(self):
        self.lang = list(Language.objects.filter(resume_id=self.user_id).values())

    def fetch_skill(self):
        self.skills = list(Skill.objects.filter(resume_id=self.user_id).values())

    def build(self):
        self.fetch_intro()
        self.fetch_exp()
        self.fetch_edu()
        self.fetch_lang()
        self.fetch_skill()

        self.resume_dict["intro"] = self.intro
        self.resume_dict["experiences"] = self.exp
        self.resume_dict["educations"] = self.edu
        self.resume_dict["skills"] = self.skills
        self.resume_dict["languages"] = self.lang

    def is_resume_exist(self):
        return Resume.objects.filter(user_id=self.user_id).exists()
