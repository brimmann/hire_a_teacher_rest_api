from django.urls import path
from jobs.views import CreateJobView, get_jobs, UpdateJobView, DeleteJobView

urlpatterns = [
    path("", get_jobs),
    path("create", CreateJobView.as_view()),
    path("update/<int:pk>", UpdateJobView.as_view()),
    path("delete/<int:pk>", DeleteJobView.as_view()),
]
