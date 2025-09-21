from django.contrib import admin
from .models import Resume, ResumeAnalysis, JobMatch


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'uploaded_at', 'analysis_completed')
    list_filter = ('analysis_completed', 'uploaded_at')
    search_fields = ('user__username', 'title')


@admin.register(ResumeAnalysis)
class ResumeAnalysisAdmin(admin.ModelAdmin):
    list_display = ('resume', 'overall_score', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('resume__title', 'resume__user__username')


@admin.register(JobMatch)
class JobMatchAdmin(admin.ModelAdmin):
    list_display = ('resume_analysis', 'job_title', 'match_percentage')
    list_filter = ('match_percentage',)
    search_fields = ('job_title', 'resume_analysis__resume__title')
