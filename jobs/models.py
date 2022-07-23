from django.db import models

from users.models import OrgDetail


class Job(models.Model):
    title = models.CharField(max_length=55, default="")
    org = models.ForeignKey(OrgDetail, on_delete=models.CASCADE, default=None)
    status = models.CharField(max_length=10, default="active")
    exp_level = models.CharField(max_length=55, default="")
    type = models.CharField(max_length=44, default="")
    city = models.CharField(max_length=44, default="")
    date_posted = models.CharField(max_length=16, default="")
    expire_date = models.CharField(max_length=12, default="")
    description = models.TextField(default="")
    tags = models.CharField(max_length=128, default="")
    apps_no = models.IntegerField(default=0)

    def __str__(self):
        return self.org.org_name.__str__() + " job"
