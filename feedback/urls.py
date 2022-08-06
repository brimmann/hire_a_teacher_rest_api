from feedback.views import select_applicant, get_tokens_endpoint
from django.urls import path

urlpatterns = [
    path("select", select_applicant),
    path("get_tokens", get_tokens_endpoint)
]
