from rest_framework import serializers
from .models import ChatHistory


class ChatHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatHistory
        fields = ('id', 'message', 'response', 'created_at')
        read_only_fields = ('id', 'response', 'created_at')
