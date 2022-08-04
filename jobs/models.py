from django.db import models

from users.models import OrgDetail, User


class Job(models.Model):
    title = models.CharField(max_length=55, default="")
    org = models.ForeignKey(OrgDetail, on_delete=models.CASCADE, default=None)
    status = models.CharField(max_length=16, default="active")
    exp_level = models.CharField(max_length=55, default="")
    type = models.CharField(max_length=44, default="")
    city = models.CharField(max_length=44, default="")
    date_posted = models.CharField(max_length=16, default="")
    expire_date = models.CharField(max_length=12, default="")
    description = models.TextField(default="")
    tags = models.CharField(max_length=128, default="")
    apps_no = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.title} - {self.org.org_name}"


class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    date_applied = models.CharField(max_length=16, default="")

    def __str__(self):
        return f"{self.job.title} - { self.teacher.email} - {self.job.org.org_name}"


class Interview(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.CharField(max_length=55, default="")
    address = models.TextField(default="")

    def __str__(self):
        return f"for {self.teacher.email} at {self.job.org.org_name} - id:{self.id}"
