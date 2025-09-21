from django.contrib import admin
from .models import Skill, UserSkill

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    search_fields = ('name', 'category')

@admin.register(UserSkill)
class UserSkillAdmin(admin.ModelAdmin):
    list_display = ('user', 'skill', 'level', 'updated_at')
    list_filter = ('skill',)
    search_fields = ('user__username', 'skill__name')
