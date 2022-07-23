from rest_framework import permissions

from jobs.models import Job


class IsOrg(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and user.type == "org"


class IsOrgSelf(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and is_compat(view, user.id)


def is_compat(view, req_id):
    pk = view.kwargs["pk"]
    record = Job.objects.get(id=pk)
    return record.org_id == req_id

