from django.urls import path
from jobs.views import (
    CreateJobView,
    get_jobs,
    UpdateJobView,
    DeleteJobView,
    get_rel_jobs,
    get_search_job,
    CreateApplicationView,
)

urlpatterns = [
    path("", get_jobs),
    path("create", CreateJobView.as_view()),
    path("update/<int:pk>", UpdateJobView.as_view()),
    path("delete/<int:pk>", DeleteJobView.as_view()),
    path("get_rel", get_rel_jobs),
    path("search", get_search_job),
    path("apply", CreateApplicationView.as_view()),
]
