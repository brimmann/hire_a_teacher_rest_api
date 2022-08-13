from rest_framework import generics, authentication
from rest_framework.decorators import (
    permission_classes,
    authentication_classes,
    api_view,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from jobs.models import Job, Application, Interview
from jobs.permissions import IsOrg, IsOrgSelf, AllowWithdraw
from jobs.serializers import JobSerializer, ApplicationSerializer, InterviewSerializer
from jobs.jobs_query_handlers import (
    get_non_awarded_jobs,
    get_relevant_jobs,
    search_jobs,
    get_applications_teacher,
    get_org_apps,
    get_org_apps_job_based,
    search_teachers,
    get_interviews_teacher,
    get_interviews_org,
)
from jobs.permissions import IsTeacher


class CreateJobView(generics.CreateAPIView):
    permission_classes = (IsOrg,)
    serializer_class = JobSerializer

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        request.data["org"] = request.user.id
        print(request.data)


class UpdateJobView(generics.UpdateAPIView):
    permission_classes = (IsOrgSelf,)
    serializer_class = JobSerializer
    queryset = Job.objects.all()


class DeleteJobView(generics.DestroyAPIView):
    permission_classes = (IsOrgSelf,)
    serializer_class = JobSerializer
    queryset = Job.objects.all()


class CreateInterviewView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = InterviewSerializer

    def finalize_response(self, request, response, *args, **kwargs):
        super().finalize_response(request, response, *args, **kwargs)
        print(response.data)
        if request.method == "POST":
            data = response.data
            self.remove_application(data["teacher"], data["job"])
        return response

    @staticmethod
    def remove_application(teacher_id, job_id):
        app = Application.objects.filter(teacher_id=teacher_id).filter(job_id=job_id)
        if not app.exists():
            return None
        app.delete()
        job = Job.objects.get(id=job_id)
        job.status = "interviewing"
        job.save()


@api_view()
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([IsOrg])
def get_jobs(request):
    res_data = get_non_awarded_jobs(request.user.id)
    return Response(res_data)


@api_view()
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_rel_jobs(request):
    res_data = get_relevant_jobs(request.user.id)
    return Response(res_data)


@api_view()
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_search_job(request):
    print("search_string" in request.query_params)

    if bool(request.query_params):
        if "search_string" in request.query_params:
            search_string = request.query_params["search_string"]
            search_string = search_string.lower()
            search_string = " ".join(search_string.split("+"))
            print("added", search_string)
            res_data = search_jobs(search_string, request.user.id)
            return Response(res_data)

    res_data = {"matched_jobs": []}

    return Response(res_data)


class CreateApplicationView(generics.CreateAPIView):
    permission_classes = (IsTeacher,)
    serializer_class = ApplicationSerializer

    def finalize_response(self, request, response, *args, **kwargs):
        super().finalize_response(request, response, *args, **kwargs)
        if request.data:
            if request.data["job"]:
                self.__increase_apps(request.data["job"])

        return response

    @staticmethod
    def __increase_apps(job_id):
        job = Job.objects.get(id=job_id)
        job.apps_no = job.apps_no + 1
        job.save()


@api_view()
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_applications(request):
    if request.user.type == "teacher":
        res_data = get_applications_teacher(request.user.id)
    else:
        if bool(request.query_params):
            res_data = get_org_apps_job_based(
                request.user.id, request.query_params["job_id"]
            )
        else:
            res_data = get_org_apps(request.user.id)
    return Response(res_data)


@api_view()
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([IsAuthenticated])
def search_teacher_get(request):
    if bool(request.query_params):
        if "search_string" in request.query_params:
            search_string = request.query_params["search_string"]
            search_string = search_string.lower()
            search_string = " ".join(search_string.split("+"))
            res_data = search_teachers(search_string)
            return Response(res_data)

    res_data = {"matched_teachers": []}

    return Response(res_data)


class DeleteApplicationView(generics.DestroyAPIView):
    permission_classes = (AllowWithdraw,)
    serializer_class = ApplicationSerializer
    queryset = Application.objects.all()
    job = None

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        self.job = Application.objects.get(id=self.kwargs["pk"]).job

    def finalize_response(self, request, response, *args, **kwargs):
        super().finalize_response(request, response, *args, **kwargs)
        self.__decrease_apps(self.job)

        return response

    @staticmethod
    def __decrease_apps(job):
        job.apps_no = job.apps_no - 1
        job.save()


@api_view()
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_interviews(request):
    if request.user.type == "teacher":
        res_data = get_interviews_teacher(request.user.id)
    else:
        res_data = get_interviews_org(request.user.id)
    return Response(res_data)


@api_view(['DELETE'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_interview_teacher(request):
    if bool(request.query_params["id"]):
        interview_id = request.query_params["id"]
        user_id = request.user.id
        if request.user.type == "teacher":
            interview = Interview.objects.filter(id=interview_id).filter(teacher_id=user_id)
        else:
            interview = Interview.objects.filter(id=interview_id).filter(job__org_id=user_id)
        if interview.exists():
            print("delete this", interview_id, user_id)
            deleting_interview = Interview.objects.get(id=interview_id)
            deleting_interview.job.status = "active"
            deleting_interview.job.save()
            deleting_interview.delete()
        else:
            return Response({"message": "not found"})
    return Response({"message": "success"})
