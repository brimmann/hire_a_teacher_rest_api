from django.urls import path
from jobs.views import (
    CreateJobView,
    get_jobs,
    UpdateJobView,
    DeleteJobView,
    get_rel_jobs,
    get_search_job,
    CreateApplicationView,
    get_applications,
    DeleteApplicationView,
    search_teacher_get,
    CreateInterviewView,
    get_interviews,
    delete_interview_teacher
)

urlpatterns = [
    path("", get_jobs),
    path("create", CreateJobView.as_view()),
    path("update/<int:pk>", UpdateJobView.as_view()),
    path("delete/<int:pk>", DeleteJobView.as_view()),
    path("get_rel", get_rel_jobs),
    path("search", get_search_job),
    path("search/teachers", search_teacher_get),
    path("apply", CreateApplicationView.as_view()),
    path("apps", get_applications),
    path("apps_withdraw/<int:pk>", DeleteApplicationView.as_view()),
    path("accept", CreateInterviewView.as_view()),
    path("interviews", get_interviews),
    path("interviews_delete", delete_interview_teacher)
]
