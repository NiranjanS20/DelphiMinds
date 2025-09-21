from django.contrib import admin
from .models import PsychometricTest, Question, TestResponse, Answer, TestResult


@admin.register(PsychometricTest)
class PsychometricTestAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'is_active', 'created_at')
    list_filter = ('category', 'is_active', 'created_at')
    search_fields = ('name', 'description')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('test', 'text', 'question_type', 'order')
    list_filter = ('test', 'question_type')
    search_fields = ('text',)
    ordering = ('test', 'order')


@admin.register(TestResponse)
class TestResponseAdmin(admin.ModelAdmin):
    list_display = ('user', 'test', 'started_at', 'is_completed')
    list_filter = ('is_completed', 'started_at', 'test')
    search_fields = ('user__username', 'test__name')


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('response', 'question', 'answer_text')
    list_filter = ('response__test',)
    search_fields = ('answer_text', 'response__user__username')


@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ('response', 'personality_type', 'overall_score', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('response__user__username', 'personality_type')
