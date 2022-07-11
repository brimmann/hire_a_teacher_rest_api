from django.core.exceptions import ObjectDoesNotExist
from rest_framework import permissions

from users.models import User


class IsTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.id == request.data["user"]
            and request.user.type == "teacher"
        )


class IsOrg(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.type == "org" and request.user.id == request.data["user"]


class TypeMatches(permissions.BasePermission):
    message = "not_match"

    def has_permission(self, request, view):
        # print("obj called", request.data)

        if bool(request.data):
            try:
                user = User.objects.get(email=request.data["email"])
                # if user.type == request.POST['type']:
                #     return True
                print(user.type == request.data["type"])
                return user.type == request.data["type"]
            except ObjectDoesNotExist as e:
                pass
        else:
            return True

    def has_object_permission(self, request, view, obj):
        print("it is called")
