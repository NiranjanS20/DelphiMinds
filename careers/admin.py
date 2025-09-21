from django.contrib import admin
from .models import CareerPath, CareerRecommendation

@admin.register(CareerPath)
class CareerPathAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)
    filter_horizontal = ('required_skills',)

@admin.register(CareerRecommendation)
class CareerRecommendationAdmin(admin.ModelAdmin):
    list_display = ('user', 'career_path', 'score', 'created_at')
    list_filter = ('career_path',)
    search_fields = ('user__username', 'career_path__title')
