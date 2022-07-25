from django.db.models import Q

from jobs.models import Job
from resume.search_map import SearchMapGen


def get_non_awarded_jobs(org_id):
    jobs = Job.objects.filter(org=org_id)
    jobs = jobs.filter(Q(status="active") | Q(status="inactive"))
    return list(jobs.values())


def get_relevant_jobs(teacher_id):
    jobs_mini = list(Job.objects.values("id", "title", "description", "tags"))
    search_map = SearchMapGen.get_search_map(teacher_id)

    if search_map is None:
        return {"error": "Resume relevant search configuration is not found"}

    match_job_ids = []
    matched_jobs = []

    for job in jobs_mini:
        for key, section in job.items():
            if key != "id":
                for keyword in search_map["keywords"]:
                    if keyword in section:
                        print('match this', keyword)
                        match_job_ids.append(job["id"])

    if len(match_job_ids) < 1:
        return {"not_found": "No relevant jobs found"}

    for job_id in match_job_ids:
        matched_jobs.append(Job.objects.filter(id=job_id).values()[0])

    return {"relevant_jobs": matched_jobs}

    print("da", matched_jobs)
