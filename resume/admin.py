from django.contrib import admin

# Register your models here.
from resume.models import Resume, Experience, Education, Language, Skill

admin.site.register(Resume)
admin.site.register(Experience)
admin.site.register(Education)
admin.site.register(Language)
admin.site.register(Skill)

