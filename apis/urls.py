from django.urls import path, include

from users.views import TeacherDetailView, OrgDetailView, CustomLoginView

urlpatterns = [
    path('login/', CustomLoginView.as_view()),
    path('resume/', include('resume.urls')),
    path('registration/', include('dj_rest_auth.registration.urls')),
    path('teacher/add_details', TeacherDetailView.as_view()),
    path('org/add_details', OrgDetailView.as_view()),
]
