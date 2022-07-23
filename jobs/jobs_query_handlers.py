from django.db.models import Q

from jobs.models import Job


def get_non_awarded_jobs(org_id):
    jobs = Job.objects.filter(org=org_id)
    jobs = jobs.filter(Q(status="active") | Q(status="inactive"))
    return list(jobs.values())
