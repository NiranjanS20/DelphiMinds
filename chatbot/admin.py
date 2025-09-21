from django.contrib import admin
from .models import ChatHistory

# Register your models here.

@admin.register(ChatHistory)
class ChatHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    search_fields = ('user__username', 'message', 'response')
