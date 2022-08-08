from rest_framework import authentication
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from feedback.models import Token
from feedback.operations import generate_tokens, get_tokens, validate_token, get_teacher_info, create_feedback, \
    calculate_feedback
from jobs.models import Interview


@api_view(["POST"])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([IsAuthenticated])
def select_applicant(request):
    if bool(request.data):
        print(request.data)
        data = request.data
        own_interview = (
            Interview.objects.filter(id=data["interview_id"])
            .filter(job__org_id=request.user.id)
            .exists()
        )
        if not own_interview:
            return Response({"message": "Not found"})

        generate_tokens(data["interview_id"], data["days"], data["students"])
        interview = Interview.objects.get(id=data["interview_id"])
        job = interview.job
        job.status = "awarded"
        job.save()
        interview.delete()

    return Response({"message": "success"})


@api_view()
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_tokens_endpoint(request):
    if request.user.type == "org":
        res_data = get_tokens(request.user.id)
        return Response(res_data)

    return Response({"message": "Not found"})


@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([AllowAny])
def get_info_endpoint(request):
    token = request.data["token"]
    check = validate_token(token)
    print("Check:", check)

    if type(check) is Token:
        return Response(get_teacher_info(check.teacher_id, check.job_id))
    else:
        return Response(check)


@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([AllowAny])
def submit_feedback_endpoint(request):
    token = request.data["token"]
    rating = request.data["rating"]
    check = validate_token(token)

    if type(check) is Token:
        create_feedback(check, rating)
        calculate_feedback(check.teacher_id)
        return Response("success")
    else:
        return Response("my_bad_request")
