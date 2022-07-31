from rest_framework import generics, authentication
from rest_framework.decorators import (
    permission_classes,
    authentication_classes,
    api_view,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from jobs.models import Job, Application
from jobs.permissions import IsOrg, IsOrgSelf, AllowWithdraw
from jobs.serializers import JobSerializer, ApplicationSerializer
from jobs.jobs_query_handlers import (
    get_non_awarded_jobs,
    get_relevant_jobs,
    search_jobs,
    get_applications_teacher,
    get_org_apps,
    get_org_apps_job_based,
search_teachers
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
            res_data = get_org_apps_job_based(request.user.id, request.query_params['job_id'])
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
