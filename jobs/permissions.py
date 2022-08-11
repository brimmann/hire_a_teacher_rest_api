from rest_framework import permissions

from jobs.models import Job

from jobs.models import Application


class IsOrg(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and user.type == "org"


class IsTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and user.type == "teacher"


class IsOrgSelf(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and is_compat(view, user.id)


class AllowWithdraw(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.type == "teacher":
            app_exist = (
                Application.objects.filter(id=view.kwargs["pk"])
                .filter(teacher_id=user.id)
                .exists()
            )
        else:
            app_exist = (
                Application.objects.filter(id=view.kwargs["pk"])
                .filter(job__org_id=user.id)
                .exists()
            )
        return user.is_authenticated and app_exist


def is_compat(view, req_id):
    pk = view.kwargs["pk"]
    record = Job.objects.get(id=pk)
    return record.org_id == req_id
