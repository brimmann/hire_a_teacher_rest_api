import json

from django.shortcuts import render
from rest_framework import generics, authentication
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework.exceptions import NotFound
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from resume.models import Resume, Experience, Education, Skill, Language
from resume.permissions import IsMyResume, IsMyResumeUpdate, DeleteResume
from resume.resume_assembler import ResumeAssembler
from resume.serializers import (
    ResumeSerializer,
    ExperienceSerializer,
    EducationSerializer,
    SkillSerializer,
    LangSerializer,
)
from users.permissions import IsTeacher


class ResumeView(generics.CreateAPIView):
    permission_classes = (IsTeacher,)
    serializer_class = ResumeSerializer


class ResumeUpdate(generics.UpdateAPIView):
    permission_classes = (IsTeacher,)
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer


class ExperienceView(generics.CreateAPIView):
    permission_classes = (IsMyResume,)
    serializer_class = ExperienceSerializer


class ExperienceUpdate(generics.UpdateAPIView):
    permission_classes = (IsMyResumeUpdate,)
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer


class ExperienceDelete(generics.DestroyAPIView):
    permission_classes = (DeleteResume,)
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer


class EducationView(generics.CreateAPIView):
    permission_classes = (IsMyResume,)
    serializer_class = EducationSerializer


class EducationUpdate(generics.UpdateAPIView):
    permission_classes = (IsMyResumeUpdate,)
    queryset = Education.objects.all()
    serializer_class = EducationSerializer


class EducationDelete(generics.DestroyAPIView):
    permission_classes = (DeleteResume,)
    queryset = Education.objects.all()
    serializer_class = EducationSerializer


class SkillView(generics.CreateAPIView):
    permission_classes = (IsMyResume,)
    serializer_class = SkillSerializer


class SkillUpdate(generics.UpdateAPIView):
    permission_classes = (IsMyResumeUpdate,)
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer


class SkillDelete(generics.DestroyAPIView):
    permission_classes = (DeleteResume,)
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer


class LangView(generics.CreateAPIView):
    permission_classes = (IsMyResume,)
    serializer_class = LangSerializer


class LangUpdate(generics.UpdateAPIView):
    permission_classes = (IsMyResumeUpdate,)
    queryset = Language.objects.all()
    serializer_class = LangSerializer


class LangDelete(generics.DestroyAPIView):
    permission_classes = (DeleteResume,)
    queryset = Language.objects.all()
    serializer_class = LangSerializer


@api_view()
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_resume(request):
    print("function called")
    resume_assembler = ResumeAssembler(request.user.id)
    if resume_assembler.is_resume_exist():
        resume_assembler.build()
        return Response(resume_assembler.resume_dict)

    raise NotFound
