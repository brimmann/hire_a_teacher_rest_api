import uuid
from collections import defaultdict
from pprint import pprint

import arrow

from feedback.models import Token, Feedback
from jobs.models import Interview, Job
from resume.models import Resume
from users.models import TeacherDetail


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


def validate_token(token):
    token = Token.objects.filter(token=token)
    if not token.exists():
        return "token_not_found"
    elif token[0].status == "used":
        return "token_used"
    elif token[0].status == 'inactive':
        return "token_inactive"
    else:
        return token[0]


def get_teacher_info(teacher_id, job_id):
    teacher = TeacherDetail.objects.get(user_id=teacher_id)
    job = Job.objects.get(id=job_id)

    return {
        "teacher_name": teacher.full_name,
        "teacher_heading": teacher.user.resume.heading,
        "org": job.org.org_name
    }


def create_feedback(token, rating):
    token.status = "used"
    token.save()
    feedback = Feedback(token=token, rating=rating)
    feedback.save()


def calculate_feedback(teacher_id):
    feedbacks = Feedback.objects.filter(token__teacher_id=teacher_id)
    feedbacks_list = list(feedbacks.values_list("rating", flat=True))
    avg_feedback = sum(feedbacks_list) / len(feedbacks_list)
    resume = Resume.objects.get(user_id=teacher_id)
    resume.ranking = avg_feedback
    resume.students = len(feedbacks_list)
    resume.save()

