from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User, TeacherDetail


class UserAdminCustomized(UserAdmin):
    model = User
    list_display = ('email', 'type', 'is_staff')
    ordering = ('email', )


admin.site.register(User, UserAdminCustomized)
admin.site.register(TeacherDetail)
