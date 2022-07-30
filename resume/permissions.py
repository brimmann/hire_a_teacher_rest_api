from rest_framework import permissions

from resume.models import Experience, Education, Skill, Language


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




class DeleteResume(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            is_compat_del(view, request.user.id)
            and request.user.type == "teacher"
            and request.user.is_authenticated
        )


def is_compat(view, req_id):
    pk = view.kwargs["pk"]
    if type(view).__name__ == "ExperienceUpdate":
        record = Experience.objects.get(id=pk)

    elif type(view).__name__ == "EducationUpdate":
        record = Education.objects.get(id=pk)

    elif type(view).__name__ == "SkillUpdate":
        record = Skill.objects.get(id=pk)

    elif type(view).__name__ == "LangUpdate":
        record = Language.objects.get(id=pk)

    return record.resume_id == req_id


def is_compat_del(view, req_id):
    pk = view.kwargs["pk"]
    if type(view).__name__ == "ExperienceDelete":
        record = Experience.objects.get(id=pk)

    elif type(view).__name__ == "EducationDelete":
        record = Education.objects.get(id=pk)

    elif type(view).__name__ == "SkillDelete":
        record = Skill.objects.get(id=pk)

    elif type(view).__name__ == "LangDelete":
        record = Language.objects.get(id=pk)

    return record.resume_id == req_id
