from django.urls import path, include

from users.views import (
    TeacherDetailView,
    OrgDetailView,
    CustomLoginView,
    get_teacher_details,
    get_org_details,
)

urlpatterns = [
    path("login/", CustomLoginView.as_view()),
    path("resume/", include("resume.urls")),
    path("jobs/", include("jobs.urls")),
    path("registration/", include("dj_rest_auth.registration.urls")),
    path("teacher/get_details", get_teacher_details),
    path("teacher/add_details", TeacherDetailView.as_view()),
    path("org/get_details", get_org_details),
    path("org/add_details", OrgDetailView.as_view()),
]
