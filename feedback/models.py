from django.db import models

from jobs.models import Job
from users.models import User


class Token(models.Model):
    token = models.CharField(max_length=9, primary_key=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    activation_date = models.CharField(max_length=18, default="")
    status = models.CharField(max_length=27, default="inactive")
