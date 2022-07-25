from rest_framework import generics, authentication
from rest_framework.decorators import (
    permission_classes,
    authentication_classes,
    api_view,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from jobs.models import Job
from jobs.permissions import IsOrg, IsOrgSelf
from jobs.serializers import JobSerializer
from jobs.jobs_query_handlers import get_non_awarded_jobs, get_relevant_jobs


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
