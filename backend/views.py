from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse


@api_view(['GET'])
@permission_classes([AllowAny])
def auth_status(request):
    """Check if user is authenticated and return user info"""
    if request.user.is_authenticated:
        return Response({
            'authenticated': True,
            'user': {
                'id': request.user.id,
                'username': request.user.username,
                'email': request.user.email,
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
            }
        })
    else:
        return Response({
            'authenticated': False,
            'user': None
        })


@api_view(['POST'])
@permission_classes([AllowAny])
def quick_login(request):
    """Simple login endpoint for homepage integration"""
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response({
            'error': 'Username and password required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    user = authenticate(username=username, password=password)
    
    if user:
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            }
        })
    else:
        return Response({
            'error': 'Invalid credentials'
        }, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_data(request):
    """Get dashboard data for authenticated users"""
    from skills.models import UserSkill
    from gamification.models import UserBadge, Streak
    from careers.models import CareerRecommendation
    
    user = request.user
    
    # Get user stats
    skills_count = UserSkill.objects.filter(user=user).count()
    badges_count = UserBadge.objects.filter(user=user).count()
    
    try:
        streak = Streak.objects.get(user=user)
        streak_count = streak.current_streak
    except Streak.DoesNotExist:
        streak_count = 0
    
    recommendations_count = CareerRecommendation.objects.filter(user=user).count()
    
    return Response({
        'stats': {
            'skills_count': skills_count,
            'badges_count': badges_count,
            'streak_count': streak_count,
            'recommendations_count': recommendations_count,
        },
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }
    })