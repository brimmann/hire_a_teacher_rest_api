from dj_rest_auth.views import LoginView
from rest_framework import generics
from rest_framework.permissions import AllowAny

from .models import TeacherDetail, OrgDetail
from .serializers import TeacherDetailsSerializer, OrgDetailsSerializer
from .permissions import IsTeacher, IsOrg, TypeMatches


class TeacherDetailView(generics.CreateAPIView):
    permission_classes = (IsTeacher, )
    queryset = TeacherDetail.objects.all()
    serializer_class = TeacherDetailsSerializer


class OrgDetailView(generics.CreateAPIView):
    permission_classes = (IsOrg, )
    queryset = OrgDetail.objects.all()
    serializer_class = OrgDetailsSerializer


class CustomLoginView(LoginView):
    permission_classes = (TypeMatches, )
