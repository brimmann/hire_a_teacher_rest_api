from rest_framework import permissions

from resume.models import Experience


class IsMyResume(permissions.BasePermission):
    def has_permission(self, request, view):
        print(request.user.id)
        return (
            request.user.type == "teacher"
            and request.user.is_authenticated
            and request.user.id == request.data["resume"]
        )


class IsMyResumeUpdate(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            is_compat(view, request.user.id)
            and request.user.type == "teacher"
            and request.user.is_authenticated
            and request.user.id == request.data["resume"]
        )


def is_compat(view, req_id):
    pk = view.kwargs["pk"]
    exp = Experience.objects.get(id=pk)
    return exp.resume_id == req_id
