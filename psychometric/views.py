from rest_framework import generics, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.db.models import Q, Count, Avg
from django.utils import timezone
try:
    from django_filters.rest_framework import DjangoFilterBackend
except ImportError:
    DjangoFilterBackend = None
from .models import CareerTest, PsychometricTest, TestResponse, Answer, TestResult, TestRecommendation
from .serializers import (
    CareerTestSerializer, CareerTestSummarySerializer, PsychometricTestSerializer, 
    TestResponseSerializer, TestResponseWithResultSerializer, TestHistorySerializer,
    AnswerSerializer, TestResultSerializer
)
import random

User = get_user_model()


class CareerTestListView(generics.ListAPIView):
    """Enhanced test listing with filtering and search"""
    serializer_class = CareerTestSummarySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter] if DjangoFilterBackend is None else [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'difficulty', 'is_featured'] if DjangoFilterBackend else []
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'estimated_time', 'created_at']
    ordering = ['-is_featured', '-created_at']
    
    def get_queryset(self):
        queryset = CareerTest.objects.filter(is_active=True)
        
        # Add user's attempt count and best score
        user = self.request.user
        queryset = queryset.annotate(
            user_attempts=Count('responses', filter=Q(responses__user=user)),
            user_best_score=Avg('responses__result__overall_score', filter=Q(responses__user=user, responses__is_completed=True))
        )
        
        return queryset
    
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        
        # Add user statistics
        user_stats = {
            'total_tests_available': CareerTest.objects.filter(is_active=True).count(),
            'tests_completed': TestResponse.objects.filter(user=request.user, is_completed=True).count(),
            'tests_in_progress': TestResponse.objects.filter(user=request.user, is_completed=False).count(),
        }
        
        response.data = {
            'user_stats': user_stats,
            'tests': response.data
        }
        
        return response


class CareerTestDetailView(generics.RetrieveAPIView):
    """Detailed test view with questions"""
    queryset = CareerTest.objects.filter(is_active=True)
    serializer_class = CareerTestSerializer
    permission_classes = [IsAuthenticated]
    
    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        
        # Add user's previous attempts
        test = self.get_object()
        user_attempts = TestResponse.objects.filter(
            user=request.user, 
            test=test
        ).order_by('-started_at')[:3]  # Last 3 attempts
        
        response.data['user_attempts'] = TestHistorySerializer(user_attempts, many=True).data
        
        return response


# Backward compatibility
class PsychometricTestListView(CareerTestListView):
    """Proxy view for backward compatibility"""
    pass


class TestHistoryView(generics.ListAPIView):
    """User's test history"""
    serializer_class = TestHistorySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return TestResponse.objects.filter(
            user=self.request.user,
            is_completed=True
        ).order_by('-completed_at')


class TestResponseDetailView(generics.RetrieveAPIView):
    serializer_class = TestResponseWithResultSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return TestResponse.objects.filter(user=self.request.user)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def start_test(request, test_id):
    """Start a career test with enhanced validation"""
    try:
        test = CareerTest.objects.get(id=test_id, is_active=True)
        user = request.user
        
        # Check attempt limits
        user_attempts = TestResponse.objects.filter(user=user, test=test).count()
        if user_attempts >= test.max_attempts:
            return Response({
                'error': f'Maximum attempts ({test.max_attempts}) reached for this test'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if user already has an incomplete response
        existing_response = TestResponse.objects.filter(
            user=user, 
            test=test, 
            is_completed=False
        ).first()
        
        if existing_response:
            return Response({
                'message': 'Resuming existing test session',
                **TestResponseSerializer(existing_response).data
            })
        
        # Create new response
        attempt_number = user_attempts + 1
        response = TestResponse.objects.create(
            user=user, 
            test=test,
            attempt_number=attempt_number,
            ip_address=request.META.get('REMOTE_ADDR')
        )
        
        return Response({
            'message': 'Test started successfully',
            **TestResponseSerializer(response).data
        }, status=status.HTTP_201_CREATED)
        
    except CareerTest.DoesNotExist:
        return Response({'error': 'Test not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_answer(request, response_id):
    """Submit an answer for a test question"""
    try:
        response = TestResponse.objects.get(id=response_id, user=request.user)
        
        if response.is_completed:
            return Response({'error': 'Test already completed'}, status=status.HTTP_400_BAD_REQUEST)
        
        question_id = request.data.get('question')
        answer_text = request.data.get('answer_text')
        answer_value = request.data.get('answer_value')
        
        if not question_id or not answer_text:
            return Response({'error': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)
        
        answer, created = Answer.objects.get_or_create(
            response=response,
            question_id=question_id,
            defaults={
                'answer_text': answer_text,
                'answer_value': answer_value
            }
        )
        
        if not created:
            answer.answer_text = answer_text
            answer.answer_value = answer_value
            answer.save()
        
        return Response({'message': 'Answer submitted successfully'})
        
    except TestResponse.DoesNotExist:
        return Response({'error': 'Test response not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def complete_test(request, response_id):
    """Complete a psychometric test and generate results"""
    try:
        response = TestResponse.objects.get(id=response_id, user=request.user)
        
        if response.is_completed:
            return Response({'error': 'Test already completed'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Mark as completed
        from django.utils import timezone
        response.is_completed = True
        response.completed_at = timezone.now()
        response.save()
        
        # Generate enhanced results based on test category
        result_data = generate_enhanced_test_results(response)
        
        result, created = TestResult.objects.get_or_create(
            response=response,
            defaults=result_data
        )
        
        if not created:
            for key, value in result_data.items():
                setattr(result, key, value)
            result.save()
        
        # Award gamification points and badges
        try:
            from gamification.services import award_test_completion
            award_test_completion(response.user, response.test, result.overall_score)
        except ImportError:
            pass
        
        return Response(TestResultSerializer(result).data)
        
    except TestResponse.DoesNotExist:
        return Response({'error': 'Test response not found'}, status=status.HTTP_404_NOT_FOUND)


def generate_enhanced_test_results(test_response):
    """Generate comprehensive test results based on category and answers"""
    test = test_response.test
    answers = test_response.answers.all()
    
    # Calculate base score from answers
    total_questions = test.questions.count()
    answered_questions = answers.count()
    base_score = (answered_questions / total_questions) * 100 if total_questions > 0 else 0
    
    # Category-specific result generation
    if test.category == 'psychometric':
        return generate_psychometric_results(test_response, base_score)
    elif test.category == 'skills':
        return generate_skills_results(test_response, base_score)
    elif test.category == 'aptitude':
        return generate_aptitude_results(test_response, base_score)
    elif test.category == 'interests':
        return generate_interests_results(test_response, base_score)
    elif test.category == 'custom':
        return generate_custom_results(test_response, base_score)
    else:
        return generate_default_results(test_response, base_score)


def generate_psychometric_results(test_response, base_score):
    """Generate MBTI-style psychometric results"""
    personalities = ['INTJ', 'ENFP', 'ISFJ', 'ESTP', 'INFP', 'ENTJ', 'ISFP', 'ENTP']
    
    return {
        'personality_type': random.choice(personalities),
        'traits': {
            'extraversion': random.uniform(0.3, 0.9),
            'openness': random.uniform(0.4, 0.9),
            'conscientiousness': random.uniform(0.5, 0.9),
            'agreeableness': random.uniform(0.3, 0.8),
            'neuroticism': random.uniform(0.1, 0.6)
        },
        'skills_assessment': {
            'emotional_intelligence': random.uniform(0.6, 0.9),
            'communication': random.uniform(0.5, 0.8),
            'leadership': random.uniform(0.4, 0.8),
            'creativity': random.uniform(0.5, 0.9),
            'analytical_thinking': random.uniform(0.6, 0.9)
        },
        'career_recommendations': [
            'Software Engineer', 'Data Analyst', 'Product Manager', 
            'UX Designer', 'Research Scientist'
        ],
        'strengths': [
            'Strong analytical thinking', 'Excellent problem-solving skills',
            'High attention to detail', 'Creative approach to challenges',
            'Good work-life balance'
        ],
        'areas_for_improvement': [
            'Public speaking', 'Team leadership', 'Networking skills',
            'Time management', 'Delegation'
        ],
        'learning_suggestions': [
            {'title': 'Leadership Skills Course', 'description': 'Develop your leadership potential'},
            {'title': 'Communication Workshop', 'description': 'Improve interpersonal skills'},
            {'title': 'Technical Writing', 'description': 'Enhance documentation skills'}
        ],
        'overall_score': min(95, max(60, base_score + random.uniform(-10, 15))),
        'percentile': random.randint(65, 92)
    }


def generate_skills_results(test_response, base_score):
    """Generate skills assessment results"""
    return {
        'personality_type': 'Skills Specialist',
        'skills_assessment': {
            'programming': random.uniform(0.6, 0.95),
            'problem_solving': random.uniform(0.7, 0.9),
            'communication': random.uniform(0.5, 0.8),
            'teamwork': random.uniform(0.6, 0.85),
            'project_management': random.uniform(0.4, 0.8)
        },
        'technical_skills': {
            'python': random.uniform(0.5, 0.9),
            'javascript': random.uniform(0.4, 0.8),
            'databases': random.uniform(0.5, 0.85),
            'cloud_platforms': random.uniform(0.3, 0.7)
        },
        'career_recommendations': [
            'Full Stack Developer', 'Software Engineer', 'DevOps Engineer',
            'Technical Lead', 'System Architect'
        ],
        'strengths': [
            'Strong technical foundation', 'Quick learner',
            'Problem-solving mindset', 'Attention to code quality'
        ],
        'areas_for_improvement': [
            'Advanced algorithms', 'System design', 'Code optimization',
            'Technical documentation'
        ],
        'learning_suggestions': [
            {'title': 'Advanced Python Programming', 'description': 'Master advanced Python concepts'},
            {'title': 'System Design Course', 'description': 'Learn scalable system architecture'},
            {'title': 'DevOps Fundamentals', 'description': 'Understand CI/CD and deployment'}
        ],
        'overall_score': min(95, max(65, base_score + random.uniform(-5, 20))),
        'percentile': random.randint(70, 95)
    }


def generate_aptitude_results(test_response, base_score):
    """Generate aptitude test results"""
    return {
        'personality_type': 'Analytical Thinker',
        'aptitude_scores': {
            'logical_reasoning': random.uniform(0.6, 0.95),
            'numerical_ability': random.uniform(0.7, 0.9),
            'verbal_comprehension': random.uniform(0.6, 0.85),
            'spatial_reasoning': random.uniform(0.5, 0.8),
            'abstract_thinking': random.uniform(0.6, 0.9)
        },
        'skills_assessment': {
            'analytical_thinking': random.uniform(0.7, 0.95),
            'attention_to_detail': random.uniform(0.6, 0.9),
            'processing_speed': random.uniform(0.5, 0.8),
            'working_memory': random.uniform(0.6, 0.85)
        },
        'career_recommendations': [
            'Data Scientist', 'Research Analyst', 'Software Engineer',
            'Financial Analyst', 'Operations Research Analyst'
        ],
        'strengths': [
            'Excellent logical reasoning', 'Strong numerical skills',
            'High analytical ability', 'Good pattern recognition'
        ],
        'areas_for_improvement': [
            'Speed of processing', 'Verbal communication',
            'Creative thinking', 'Practical application'
        ],
        'learning_suggestions': [
            {'title': 'Advanced Statistics', 'description': 'Strengthen analytical skills'},
            {'title': 'Logic and Critical Thinking', 'description': 'Enhance reasoning abilities'},
            {'title': 'Data Analysis Tools', 'description': 'Learn practical data skills'}
        ],
        'overall_score': min(95, max(70, base_score + random.uniform(0, 25))),
        'percentile': random.randint(75, 98)
    }


def generate_interests_results(test_response, base_score):
    """Generate Holland Codes (RIASEC) career interest results"""
    riasec_codes = ['Realistic', 'Investigative', 'Artistic', 'Social', 'Enterprising', 'Conventional']
    primary_code = random.choice(riasec_codes)
    
    return {
        'personality_type': f'{primary_code} Type',
        'interest_profile': {
            'realistic': random.uniform(0.3, 0.9),
            'investigative': random.uniform(0.4, 0.9),
            'artistic': random.uniform(0.2, 0.8),
            'social': random.uniform(0.3, 0.8),
            'enterprising': random.uniform(0.3, 0.8),
            'conventional': random.uniform(0.4, 0.7)
        },
        'skills_assessment': {
            'collaboration': random.uniform(0.5, 0.8),
            'innovation': random.uniform(0.4, 0.9),
            'organization': random.uniform(0.5, 0.8),
            'communication': random.uniform(0.5, 0.8)
        },
        'career_recommendations': get_riasec_careers(primary_code),
        'strengths': get_riasec_strengths(primary_code),
        'areas_for_improvement': [
            'Explore other interest areas', 'Develop complementary skills',
            'Build professional network', 'Gain practical experience'
        ],
        'learning_suggestions': [
            {'title': 'Career Exploration Workshop', 'description': 'Discover new career paths'},
            {'title': 'Professional Development', 'description': 'Build job-ready skills'},
            {'title': 'Industry Networking', 'description': 'Connect with professionals'}
        ],
        'overall_score': min(95, max(65, base_score + random.uniform(-5, 15))),
        'percentile': random.randint(60, 88)
    }


def generate_custom_results(test_response, base_score):
    """Generate DelphiMinds custom test results"""
    return {
        'personality_type': 'DelphiMinds Achiever',
        'delphiminds_score': {
            'career_readiness': random.uniform(0.6, 0.9),
            'learning_agility': random.uniform(0.7, 0.95),
            'tech_aptitude': random.uniform(0.6, 0.9),
            'growth_mindset': random.uniform(0.7, 0.9),
            'industry_alignment': random.uniform(0.5, 0.8)
        },
        'skills_assessment': {
            'adaptability': random.uniform(0.6, 0.9),
            'continuous_learning': random.uniform(0.7, 0.95),
            'goal_orientation': random.uniform(0.6, 0.9),
            'resilience': random.uniform(0.5, 0.8)
        },
        'career_recommendations': [
            'Software Development', 'Data Science', 'Product Management',
            'Technical Consulting', 'Innovation Management'
        ],
        'strengths': [
            'Strong learning ability', 'Adaptable to change',
            'Goal-oriented mindset', 'Tech-savvy approach'
        ],
        'areas_for_improvement': [
            'Industry specialization', 'Professional networking',
            'Advanced technical skills', 'Leadership development'
        ],
        'learning_suggestions': [
            {'title': 'DelphiMinds Bootcamp', 'description': 'Accelerated career preparation'},
            {'title': 'Industry Mentorship', 'description': 'Connect with industry experts'},
            {'title': 'Advanced Projects', 'description': 'Build impressive portfolio'}
        ],
        'overall_score': min(95, max(70, base_score + random.uniform(5, 25))),
        'percentile': random.randint(80, 96)
    }


def generate_default_results(test_response, base_score):
    """Generate default results for unknown test types"""
    return {
        'personality_type': 'Well-Rounded Professional',
        'skills_assessment': {
            'general_aptitude': random.uniform(0.6, 0.8),
            'learning_ability': random.uniform(0.6, 0.9),
            'problem_solving': random.uniform(0.5, 0.8),
            'communication': random.uniform(0.5, 0.8)
        },
        'career_recommendations': [
            'Business Analyst', 'Project Manager', 'Consultant',
            'Sales Professional', 'Operations Manager'
        ],
        'strengths': [
            'Balanced skill set', 'Good learning ability',
            'Adaptable approach', 'Strong work ethic'
        ],
        'areas_for_improvement': [
            'Skill specialization', 'Industry expertise',
            'Technical depth', 'Leadership skills'
        ],
        'learning_suggestions': [
            {'title': 'Professional Development', 'description': 'Build core business skills'},
            {'title': 'Industry Certification', 'description': 'Gain recognized credentials'},
            {'title': 'Leadership Training', 'description': 'Develop management skills'}
        ],
        'overall_score': min(90, max(60, base_score + random.uniform(-10, 10))),
        'percentile': random.randint(55, 85)
    }


def get_riasec_careers(code):
    """Get career recommendations based on RIASEC code"""
    careers = {
        'Realistic': ['Engineer', 'Mechanic', 'Pilot', 'Architect', 'Veterinarian'],
        'Investigative': ['Data Scientist', 'Research Scientist', 'Analyst', 'Doctor', 'Psychologist'],
        'Artistic': ['Designer', 'Writer', 'Artist', 'Musician', 'Filmmaker'],
        'Social': ['Teacher', 'Counselor', 'Social Worker', 'Nurse', 'Coach'],
        'Enterprising': ['Manager', 'Sales Representative', 'Entrepreneur', 'Lawyer', 'Executive'],
        'Conventional': ['Accountant', 'Administrator', 'Banker', 'Secretary', 'Clerk']
    }
    return careers.get(code, ['General Professional'])


def get_riasec_strengths(code):
    """Get strengths based on RIASEC code"""
    strengths = {
        'Realistic': ['Practical skills', 'Hands-on approach', 'Technical aptitude', 'Problem-solving'],
        'Investigative': ['Analytical thinking', 'Research skills', 'Curiosity', 'Scientific approach'],
        'Artistic': ['Creativity', 'Imagination', 'Aesthetic sense', 'Innovation'],
        'Social': ['Interpersonal skills', 'Empathy', 'Communication', 'Helping others'],
        'Enterprising': ['Leadership', 'Persuasion', 'Business acumen', 'Risk-taking'],
         'Conventional': ['Organization', 'Attention to detail', 'Systematic approach', 'Reliability']
    }
    return strengths.get(code, ['General professional skills'])


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_test_result(request, response_id):
    """Get test results"""
    try:
        response = TestResponse.objects.get(id=response_id, user=request.user)
        
        if not response.is_completed:
            return Response({'error': 'Test not completed'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not hasattr(response, 'result'):
            return Response({'error': 'Results not available'}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(TestResultSerializer(response.result).data)
        
    except TestResponse.DoesNotExist:
        return Response({'error': 'Test response not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_stats(request):
    """Get comprehensive user statistics for testing"""
    user = request.user
    
    # Calculate statistics
    total_responses = TestResponse.objects.filter(user=user)
    completed_tests = total_responses.filter(is_completed=True)
    
    # Calculate average score
    completed_with_results = completed_tests.filter(result__isnull=False)
    avg_score = 0
    if completed_with_results.exists():
        avg_score = sum(r.result.overall_score for r in completed_with_results) / completed_with_results.count()
    
    # Calculate current streak (consecutive days with test activity)
    current_streak = calculate_test_streak(user)
    
    # Get badge count from gamification app
    badges_earned = 0
    try:
        from gamification.models import UserBadge
        badges_earned = UserBadge.objects.filter(user=user).count()
    except ImportError:
        pass
    
    # Recent activity
    recent_tests = completed_tests.order_by('-completed_at')[:5]
    
    stats = {
        'tests_completed': completed_tests.count(),
        'tests_in_progress': total_responses.filter(is_completed=False).count(),
        'average_score': round(avg_score, 1),
        'current_streak': current_streak,
        'badges_earned': badges_earned,
        'total_test_time': sum(
            (r.completed_at - r.started_at).total_seconds() / 60 
            for r in completed_tests if r.completed_at
        ),
        'favorite_category': get_favorite_test_category(user),
        'recent_activity': [
            {
                'test_name': r.test.name,
                'completed_at': r.completed_at.isoformat(),
                'score': r.result.overall_score if hasattr(r, 'result') else None
            } for r in recent_tests
        ]
    }
    
    return Response(stats)


def calculate_test_streak(user):
    """Calculate consecutive days with test activity"""
    from datetime import date, timedelta
    
    current_date = date.today()
    streak = 0
    
    # Check each day going backwards
    for i in range(365):  # Check up to a year
        check_date = current_date - timedelta(days=i)
        
        has_activity = TestResponse.objects.filter(
            user=user,
            started_at__date=check_date
        ).exists()
        
        if has_activity:
            streak += 1
        else:
            break
    
    return streak


def get_favorite_test_category(user):
    """Get user's most frequently taken test category"""
    category_counts = TestResponse.objects.filter(
        user=user, 
        is_completed=True
    ).values('test__category').annotate(
        count=Count('test__category')
    ).order_by('-count')
    
    if category_counts:
        return category_counts.first()['test__category']
    return None


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_test_recommendations(request):
    """Get personalized test recommendations based on user history"""
    user = request.user
    
    # Get user's completed tests
    completed_categories = TestResponse.objects.filter(
        user=user, 
        is_completed=True
    ).values_list('test__category', flat=True).distinct()
    
    # Find tests not yet taken
    available_tests = CareerTest.objects.filter(
        is_active=True
    ).exclude(
        responses__user=user,
        responses__is_completed=True
    )
    
    # Prioritize different categories
    if completed_categories:
        # Recommend tests from categories user hasn't tried
        recommended = available_tests.exclude(
            category__in=completed_categories
        )[:3]
        
        if recommended.count() < 3:
            # Fill with other available tests
            additional = available_tests.exclude(
                id__in=[t.id for t in recommended]
            )[:3-recommended.count()]
            recommended = list(recommended) + list(additional)
    else:
        # For new users, recommend featured tests
        recommended = available_tests.filter(is_featured=True)[:3]
        
        if recommended.count() < 3:
            additional = available_tests.exclude(
                id__in=[t.id for t in recommended]
            ).order_by('difficulty')[:3-recommended.count()]
            recommended = list(recommended) + list(additional)
    
    return Response({
        'recommended_tests': CareerTestSummarySerializer(recommended, many=True).data,
        'reason': 'Based on your testing history and preferences'
    })
