from django.urls import path, include
from resume.views import (
    ResumeView,
    ExperienceView,
    EducationView,
    SkillView,
    get_resume,
    ResumeUpdate,
    ExperienceUpdate,
    EducationUpdate,
)

urlpatterns = [
    path("", get_resume),
    path("create", ResumeView.as_view()),
    path("update/<int:pk>", ResumeUpdate.as_view()),
    path("create/exp", ExperienceView.as_view()),
    path("update/exp/<int:pk>", ExperienceUpdate.as_view()),
    path("create/edu", EducationView.as_view()),
    path("update/edu/<int:pk>", EducationUpdate.as_view()),
    path("create/skill", SkillView.as_view()),
]
