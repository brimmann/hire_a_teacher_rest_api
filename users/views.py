import requests
from dj_rest_auth.views import LoginView
from rest_framework import generics, authentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import TeacherDetail, OrgDetail
from .serializers import TeacherDetailsSerializer, OrgDetailsSerializer
from .permissions import IsTeacher, IsOrg, TypeMatches


class TeacherDetailView(generics.CreateAPIView):
    permission_classes = (IsTeacher,)
    queryset = TeacherDetail.objects.all()
    serializer_class = TeacherDetailsSerializer


@api_view()
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_teacher_details(request, format=None):
    user_details = TeacherDetail.objects.filter(user_id=request.user.id).values()[0]
    print(user_details)
    return Response(user_details)


class OrgDetailView(generics.CreateAPIView):
    permission_classes = (IsOrg,)
    queryset = OrgDetail.objects.all()
    serializer_class = OrgDetailsSerializer


@api_view()
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_org_details(request, format=None):
    user_details = OrgDetail.objects.filter(user_id=request.user.id).values()[0]
    print(user_details)
    return Response(user_details)


class CustomLoginView(LoginView):
    permission_classes = (TypeMatches,)
