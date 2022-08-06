import uuid
from collections import defaultdict
from pprint import pprint

import arrow

from feedback.models import Token
from jobs.models import Interview


def generate_tokens(interview_id, days, numbers):
    interview = Interview.objects.get(id=interview_id)
    job_id = interview.job_id
    teacher_id = interview.teacher_id
    arrow_now = arrow.now()
    arrow_act_date = arrow_now.shift(days=days)
    act_date = arrow_act_date.format("YYYY-MM-DD")

    for _ in range(numbers):
        token = uuid.uuid4().hex[:8].upper()
        token = token[:4] + "-" + token[4:]
        token = Token(token=token, job_id=job_id, teacher_id=teacher_id, activation_date=act_date)
        token.save()


def get_tokens(org_id):
    tokens = Token.objects.filter(job__org_id=org_id)
    jobs = tokens.values("job_id", "job__title", "teacher__teacherdetail__full_name", "activation_date").distinct()
    result = []
    for job in jobs:
        job["job_title"] = job["job__title"]
        del job["job__title"]
        job["teacher"] = job["teacher__teacherdetail__full_name"]
        del job["teacher__teacherdetail__full_name"]
        arrow_date = arrow.get(job["activation_date"], "YYYY-MM-DD")
        job["activation_date"] = arrow_date.format("MMMM DD, YYYY")

    print()

    for job in jobs:
        temp = {
            "header": job,
            "tokens": list(tokens.filter(job_id=job["job_id"]).values("token", "status"))
        }
        result.append(temp)
    if len(result) < 1:
        return {"tokens": []}

    return {"tokens": result}

    pprint(result)

