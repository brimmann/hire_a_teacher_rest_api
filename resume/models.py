from django.contrib.postgres.fields import ArrayField
from django.db import models

from users.models import User


class Resume(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    intro = models.TextField(default="")
    heading = models.CharField(max_length=44, default="")
    address = models.CharField(max_length=88, default="")
    email = models.CharField(max_length=32, default="")

    def __str__(self):
        return self.user.email + "- resume"


class Experience(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    title = models.CharField(max_length=44, default="")
    org = models.CharField(max_length=44, default="")
    start_date_month = models.CharField(max_length=44, default="")
    start_date_year = models.CharField(max_length=44, default="")
    end_date_month = models.CharField(max_length=44, default="")
    end_date_year = models.CharField(max_length=44, default="")
    description = models.TextField(default="")

    def __str__(self):
        return self.resume.user.__str__() + "-exp"


class Education(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    level = models.CharField(max_length=44, default="")
    field_of_study = models.CharField(max_length=44, default="")
    school = models.CharField(max_length=44, default="")
    schoolLocation = models.CharField(max_length=44, default="")
    start_date_month = models.CharField(max_length=44, default="")
    start_date_year = models.CharField(max_length=44, default="")
    end_date_month = models.CharField(max_length=44, default="")
    end_date_year = models.CharField(max_length=44, default="")

    def __str__(self):
        return self.resume.user.__str__() + "-edu"


class Skill(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    skill = models.CharField(max_length=44, default="")

    def __str__(self):
        return self.resume.user.__str__() + "-skill"


class Language(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    language = models.CharField(max_length=44, default="")
    level_of_fluency = models.CharField(max_length=44, default="")

    def __str__(self):
        return self.resume.user.__str__() + "-lang"


class RelSearchConfig(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    city = models.CharField(max_length=44, default="")
    keywords = ArrayField(models.CharField(max_length=44))
