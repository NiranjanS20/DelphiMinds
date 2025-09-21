from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ChatHistory
from .serializers import ChatHistorySerializer
from .services import ChatbotService


# Create your views here.

def simple_chatbot_reply(message: str) -> str:
    text = message.lower()
    if 'resume' in text:
        return 'Tip: Tailor your resume with quantifiable achievements and relevant keywords.'
    if 'interview' in text:
        return 'Practice common STAR-format answers and research the company thoroughly.'
    if 'skills' in text:
        return 'Focus on in-demand skills like Python, SQL, cloud, and data analysis.'
    return 'I can help with careers, skills, resumes, and interviews. Ask me anything!'


class ChatbotMessageView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        message = request.data.get('message', '')
        
        if not message.strip():
            return Response(
                {'error': 'Message cannot be empty'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get user context for personalized responses
        user_context = {}
        if hasattr(request.user, 'profile'):
            profile = request.user.profile
            user_context = {
                'current_role': profile.current_role,
                'industry_interest': profile.industry_interest,
                'experience_years': profile.experience_years,
                'career_goals': profile.career_goals,
            }
        
        # Use the enhanced chatbot service
        chatbot_service = ChatbotService()
        reply = chatbot_service.get_career_focused_response(message, user_context)
        
        # Save to chat history
        entry = ChatHistory.objects.create(
            user=request.user, 
            message=message, 
            response=reply
        )
        
        return Response(ChatHistorySerializer(entry).data)


class ChatHistoryListView(generics.ListAPIView):
    serializer_class = ChatHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ChatHistory.objects.filter(user=self.request.user).order_by('-created_at')


class ChatbotStatusView(APIView):
    """Check chatbot service status and available features"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        chatbot_service = ChatbotService()
        status_info = {
            'huggingface_available': bool(chatbot_service.huggingface_api_key),
            'openai_available': bool(chatbot_service.openai_api_key),
            'fallback_mode': not (chatbot_service.huggingface_api_key or chatbot_service.openai_api_key),
            'features': [
                'Career advice and guidance',
                'Resume writing tips',
                'Interview preparation',
                'Skill development recommendations',
                'Job search strategies',
                'Salary negotiation tips',
                'Professional networking advice'
            ]
        }
        return Response(status_info)
