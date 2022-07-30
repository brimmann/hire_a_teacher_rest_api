from rest_framework import generics, authentication
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework.exceptions import NotFound
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from resume.search_map import SearchMapGen

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

    def finalize_response(self, request, response, *args, **kwargs):
        super().finalize_response(request, response, *args, **kwargs)
        if response.status_code == 200:
            SearchMapGen.generate(request.user.id)
            print("search-map called")
        return response



class ExperienceView(generics.CreateAPIView):
    permission_classes = (IsMyResume,)
    serializer_class = ExperienceSerializer

    def finalize_response(self, request, response, *args, **kwargs):
        super().finalize_response(request, response, *args, **kwargs)
        if response.status_code == 200:
            SearchMapGen.generate(request.user.id)
        return response


class ExperienceUpdate(generics.UpdateAPIView):
    permission_classes = (IsMyResumeUpdate,)
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer

    def finalize_response(self, request, response, *args, **kwargs):
        super().finalize_response(request, response, *args, **kwargs)
        if response.status_code == 200:
            SearchMapGen.generate(request.user.id)
        return response


class ExperienceDelete(generics.DestroyAPIView):
    permission_classes = (DeleteResume,)
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer

    def finalize_response(self, request, response, *args, **kwargs):
        super().finalize_response(request, response, *args, **kwargs)
        if response.status_code == 200:
            SearchMapGen.generate(request.user.id)
        return response


class EducationView(generics.CreateAPIView):
    permission_classes = (IsMyResume,)
    serializer_class = EducationSerializer

    def finalize_response(self, request, response, *args, **kwargs):
        super().finalize_response(request, response, *args, **kwargs)
        if response.status_code == 200:
            SearchMapGen.generate(request.user.id)
        return response


class EducationUpdate(generics.UpdateAPIView):
    permission_classes = (IsMyResumeUpdate,)
    queryset = Education.objects.all()
    serializer_class = EducationSerializer

    def finalize_response(self, request, response, *args, **kwargs):
        super().finalize_response(request, response, *args, **kwargs)
        if response.status_code == 200:
            SearchMapGen.generate(request.user.id)
        return response


class EducationDelete(generics.DestroyAPIView):
    permission_classes = (DeleteResume,)
    queryset = Education.objects.all()
    serializer_class = EducationSerializer

    def finalize_response(self, request, response, *args, **kwargs):
        super().finalize_response(request, response, *args, **kwargs)
        if response.status_code == 200:
            SearchMapGen.generate(request.user.id)
        return response


class SkillView(generics.CreateAPIView):
    permission_classes = (IsMyResume,)
    serializer_class = SkillSerializer

    def finalize_response(self, request, response, *args, **kwargs):
        super().finalize_response(request, response, *args, **kwargs)
        if response.status_code == 200:
            SearchMapGen.generate(request.user.id)
        return response


class SkillUpdate(generics.UpdateAPIView):
    permission_classes = (IsMyResumeUpdate,)
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer

    def finalize_response(self, request, response, *args, **kwargs):
        super().finalize_response(request, response, *args, **kwargs)
        if response.status_code == 200:
            SearchMapGen.generate(request.user.id)
        return response


class SkillDelete(generics.DestroyAPIView):
    permission_classes = (DeleteResume,)
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer

    def finalize_response(self, request, response, *args, **kwargs):
        super().finalize_response(request, response, *args, **kwargs)
        if response.status_code == 200:
            SearchMapGen.generate(request.user.id)
        return response


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


@api_view()
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_resume_public(request):
    resume_assembler = ResumeAssembler(request.query_params['id'])
    if resume_assembler.is_resume_exist():
        resume_assembler.build()
        return Response(resume_assembler.resume_dict)

    raise NotFound


