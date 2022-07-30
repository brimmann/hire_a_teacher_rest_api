from django.urls import path, include
from resume.views import (
    ResumeView,
    ExperienceView,
    ExperienceDelete,
    EducationView,
    EducationDelete,
    SkillView,
    SkillUpdate,
    SkillDelete,
    get_resume,
    ResumeUpdate,
    ExperienceUpdate,
    EducationUpdate,
    LangView,
    LangUpdate,
    LangDelete,
    get_resume_public,
)

urlpatterns = [
    path("", get_resume),
    path("public", get_resume_public),
    path("create", ResumeView.as_view()),
    path("update/<int:pk>", ResumeUpdate.as_view()),
    path("create/exp", ExperienceView.as_view()),
    path("delete/exp/<int:pk>", ExperienceDelete.as_view()),
    path("update/exp/<int:pk>", ExperienceUpdate.as_view()),
    path("create/edu", EducationView.as_view()),
    path("update/edu/<int:pk>", EducationUpdate.as_view()),
    path("delete/edu/<int:pk>", EducationDelete.as_view()),
    path("create/skill", SkillView.as_view()),
    path("update/skill/<int:pk>", SkillUpdate.as_view()),
    path("delete/skill/<int:pk>", SkillDelete.as_view()),
    path("create/lang", LangView.as_view()),
    path("update/lang/<int:pk>", LangUpdate.as_view()),
    path("delete/lang/<int:pk>", LangDelete.as_view()),
]
