from dj_rest_auth.views import PasswordResetConfirmView
from django.urls import path, include, re_path

from users.views import (
    TeacherDetailView,
    OrgDetailView,
    CustomLoginView,
    get_teacher_details,
    get_org_details,
)

# re_path(
#     r"^rest-auth/password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$",
#     PasswordResetConfirmView.as_view(),
#     name="password_reset_confirm",
# ),
urlpatterns = [
    # path("auth/", include("dj_rest_auth.urls")),
    # path(
    #     "rest-auth/password/reset/confirm/<str:uidb64>/<str:token>",
    #     PasswordResetConfirmView.as_view(),
    #     name="password_reset_confirm",
    # ),
    # path("reset/", )
    path(
        "password_reset/",
        include("django_rest_passwordreset.urls", namespace="password_reset"),
    ),
    path("login/", CustomLoginView.as_view()),
    path("resume/", include("resume.urls")),
    path("jobs/", include("jobs.urls")),
    path("feeback/", include("feedback.urls")),
    path("registration/", include("dj_rest_auth.registration.urls")),
    path("teacher/get_details", get_teacher_details),
    path("teacher/add_details", TeacherDetailView.as_view()),
    path("org/get_details", get_org_details),
    path("org/add_details", OrgDetailView.as_view()),
]
