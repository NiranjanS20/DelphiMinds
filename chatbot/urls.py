from django.urls import path
from .views import ChatbotMessageView, ChatHistoryListView, ChatbotStatusView

urlpatterns = [
    path('', ChatbotMessageView.as_view(), name='chatbot'),
    path('history/', ChatHistoryListView.as_view(), name='chat-history'),
    path('status/', ChatbotStatusView.as_view(), name='chatbot-status'),
]
