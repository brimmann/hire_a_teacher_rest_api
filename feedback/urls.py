from feedback.views import select_applicant, get_tokens_endpoint, get_info_endpoint, submit_feedback_endpoint
from django.urls import path

urlpatterns = [
    path("select", select_applicant),
    path("get_tokens", get_tokens_endpoint),
    path("get_info", get_info_endpoint),
    path("submit", submit_feedback_endpoint)
]
