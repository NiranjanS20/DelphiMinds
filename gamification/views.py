from rest_framework import generics, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status, filters
from django.contrib.auth import get_user_model
from django.db.models import Q, Count, Sum, Avg
from django.utils import timezone
try:
    from django_filters.rest_framework import DjangoFilterBackend
except ImportError:
    DjangoFilterBackend = None
from .models import (
    BadgeCategory, Badge, UserBadge, UserCertification, Streak,
    Leaderboard, Achievement, UserProfile
)
from .serializers import (
    BadgeCategorySerializer, BadgeSerializer, UserBadgeSerializer, UserCertificationSerializer,
    StreakSerializer, LeaderboardSerializer, AchievementSerializer, UserProfileSerializer
)

User = get_user_model()


class BadgeCategoryListView(generics.ListAPIView):
    """List all badge categories"""
    queryset = BadgeCategory.objects.all()
    serializer_class = BadgeCategorySerializer
    permission_classes = [IsAuthenticated]


class BadgeListView(generics.ListAPIView):
    """Enhanced badge listing with filtering"""
    serializer_class = BadgeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter] if DjangoFilterBackend is None else [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['badge_type', 'difficulty', 'category', 'skill_category'] if DjangoFilterBackend else []
    search_fields = ['name', 'description']
    
    def get_queryset(self):
        return Badge.objects.filter(is_active=True)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class UserBadgeListView(generics.ListAPIView):
    """User's earned badges"""
    serializer_class = UserBadgeSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return UserBadge.objects.filter(user=self.request.user).order_by('-earned_at')


class StreakView(generics.RetrieveAPIView):
    serializer_class = StreakSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        streak, created = Streak.objects.get_or_create(user=self.request.user)
        return streak


class LeaderboardView(generics.ListAPIView):
    queryset = Leaderboard.objects.all()[:10]
    serializer_class = LeaderboardSerializer
    permission_classes = [IsAuthenticated]


class AchievementListView(generics.ListAPIView):
    serializer_class = AchievementSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Achievement.objects.filter(user=self.request.user)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_streak(request):
    """Update user's learning streak"""
    streak, created = Streak.objects.get_or_create(user=request.user)
    
    # Simple streak logic - update if user was active today
    from django.utils import timezone
    today = timezone.now().date()
    last_activity = streak.last_activity.date()
    
    if last_activity < today:
        if last_activity == today - timezone.timedelta(days=1):
            # Consecutive day
            streak.current_streak += 1
        else:
            # Reset streak
            streak.current_streak = 1
        
        if streak.current_streak > streak.longest_streak:
            streak.longest_streak = streak.current_streak
        
        streak.save()
    
    return Response(StreakSerializer(streak).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def award_badge(request, badge_id):
    """Award a badge to the current user"""
    try:
        badge = Badge.objects.get(id=badge_id)
        user_badge, created = UserBadge.objects.get_or_create(
            user=request.user,
            badge=badge
        )
        
        if created:
            # Award points
            leaderboard, _ = Leaderboard.objects.get_or_create(user=request.user)
            leaderboard.total_points += badge.points_required
            leaderboard.save()
            
            # Create achievement
            Achievement.objects.create(
                user=request.user,
                title=f"Earned {badge.name}",
                description=f"Congratulations! You earned the {badge.name} badge.",
                points_earned=badge.points_required
            )
            
            return Response({'message': 'Badge awarded!'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Badge already earned'}, status=status.HTTP_200_OK)
            
    except Badge.DoesNotExist:
        return Response({'error': 'Badge not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def user_certifications(request):
    """Handle user certifications"""
    if request.method == 'GET':
        certifications = UserCertification.objects.filter(user=request.user)
        return Response(UserCertificationSerializer(certifications, many=True).data)
    
    elif request.method == 'POST':
        try:
            # Handle file upload if present
            certificate_file = request.FILES.get('certificate_file')
            
            # Create certification
            certification_data = {
                'user': request.user.id,
                'title': request.data.get('title'),
                'description': request.data.get('description', ''),
                'issuing_organization': request.data.get('issuer', ''),
                'issue_date': request.data.get('issue_date'),
                'expiry_date': request.data.get('expiry_date'),
                'credential_id': request.data.get('credential_id', ''),
                'verification_url': request.data.get('verification_url', ''),
                'certification_type': 'technical',  # Default
                'points_earned': 50  # Default points
            }
            
            serializer = UserCertificationSerializer(data=certification_data)
            if serializer.is_valid():
                certification = serializer.save()
                
                # Award points to user profile
                profile, created = UserProfile.objects.get_or_create(user=request.user)
                profile.add_points(50)
                
                # Create achievement record
                Achievement.objects.create(
                    user=request.user,
                    title=f"Added Certification: {certification.title}",
                    description=f"Added certification from {certification.issuing_organization}",
                    achievement_type='certification',
                    points_earned=50,
                    metadata={
                        'certification_id': certification.id,
                        'issuer': certification.issuing_organization
                    }
                )
                
                return Response({
                    'message': 'Certification added successfully!',
                    'certification': UserCertificationSerializer(certification).data
                }, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def user_achievements(request):
    """Handle user achievements"""
    if request.method == 'GET':
        achievements = Achievement.objects.filter(user=request.user)
        return Response(AchievementSerializer(achievements, many=True).data)
    
    elif request.method == 'POST':
        try:
            achievement_data = request.data.copy()
            achievement_data['user'] = request.user.id
            
            # Store additional fields in metadata
            metadata = {}
            achievement_type = achievement_data.get('achievement_type')
            
            # Extract type-specific fields into metadata
            type_fields = {
                'competition': ['event_name', 'role', 'rank', 'achievement_date'],
                'project': ['project_title', 'project_link', 'technologies', 'start_date', 'end_date'],
                'internship': ['role', 'company', 'start_date', 'end_date', 'key_achievement'],
                'workshop': ['workshop_title', 'provider', 'completion_date', 'duration', 'certificate_url'],
                'publication': ['publication_title', 'journal', 'publication_date', 'doi', 'publication_link', 'authors']
            }
            
            if achievement_type in type_fields:
                for field in type_fields[achievement_type]:
                    if field in achievement_data:
                        metadata[field] = achievement_data[field]
            
            # Create achievement with cleaned data
            clean_data = {
                'user': request.user.id,
                'title': achievement_data.get('title'),
                'description': achievement_data.get('description', ''),
                'achievement_type': achievement_type,
                'points_earned': achievement_data.get('points_earned', 50),
                'metadata': metadata
            }
            
            serializer = AchievementSerializer(data=clean_data)
            if serializer.is_valid():
                achievement = serializer.save()
                
                # Award points to user profile
                profile, created = UserProfile.objects.get_or_create(user=request.user)
                profile.add_points(achievement.points_earned)
                
                # Check for relevant badges
                check_and_award_badges(request.user, achievement_type, achievement.points_earned)
                
                return Response({
                    'message': 'Achievement added successfully!',
                    'achievement': AchievementSerializer(achievement).data
                }, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


def check_and_award_badges(user, achievement_type, points):
    """Check and award relevant badges based on achievement"""
    # Get user's total achievements of this type
    type_count = Achievement.objects.filter(user=user, achievement_type=achievement_type).count()
    
    # Award badges based on milestones
    badge_criteria = {
        'competition': [(1, 'First Competition'), (5, 'Competition Veteran'), (10, 'Competition Master')],
        'project': [(1, 'First Project'), (5, 'Project Builder'), (10, 'Project Master')],
        'internship': [(1, 'Professional Experience'), (3, 'Industry Veteran')],
        'workshop': [(1, 'Continuous Learner'), (10, 'Workshop Expert')],
        'publication': [(1, 'Published Author'), (5, 'Research Scholar')]
    }
    
    if achievement_type in badge_criteria:
        # Ensure default category exists
        default_category, created = BadgeCategory.objects.get_or_create(
            name='Achievements',
            defaults={
                'description': 'General achievement badges',
                'icon': '🏆',
                'color': '#3B82F6'
            }
        )
        
        for count, badge_name in badge_criteria[achievement_type]:
            if type_count >= count:
                # Try to award badge (create if doesn't exist)
                badge, created = Badge.objects.get_or_create(
                    name=badge_name,
                    defaults={
                        'description': f'Earned for {count} {achievement_type} achievements',
                        'badge_type': 'achievement',
                        'difficulty': 'bronze' if count == 1 else 'silver' if count <= 5 else 'gold',
                        'points_required': count * 10,
                        'category': default_category
                    }
                )
                
                # Award badge to user if not already earned
                UserBadge.objects.get_or_create(user=user, badge=badge)
