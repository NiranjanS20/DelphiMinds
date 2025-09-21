from rest_framework import serializers
from .models import CareerTest, PsychometricTest, Question, TestResponse, Answer, TestResult, TestRecommendation


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'text', 'question_type', 'options', 'correct_answer', 'points', 'order', 'is_required', 'explanation')
        extra_kwargs = {
            'correct_answer': {'write_only': True}  # Don't expose correct answers to frontend
        }


class CareerTestSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    total_questions = serializers.ReadOnlyField()
    average_score = serializers.ReadOnlyField()
    
    class Meta:
        model = CareerTest
        fields = ('id', 'name', 'description', 'category', 'difficulty', 'estimated_time',
                 'is_active', 'is_featured', 'instructions', 'created_at', 'questions',
                 'total_questions', 'average_score')


class CareerTestSummarySerializer(serializers.ModelSerializer):
    """Simplified serializer for test listings"""
    total_questions = serializers.ReadOnlyField()
    
    class Meta:
        model = CareerTest
        fields = ('id', 'name', 'description', 'category', 'difficulty', 'estimated_time',
                 'is_featured', 'total_questions')


class PsychometricTestSerializer(CareerTestSerializer):
    """Proxy serializer for backward compatibility"""
    class Meta(CareerTestSerializer.Meta):
        model = PsychometricTest


class AnswerSerializer(serializers.ModelSerializer):
    question_text = serializers.CharField(source='question.text', read_only=True)
    
    class Meta:
        model = Answer
        fields = ('question', 'question_text', 'answer_text', 'answer_value', 'is_correct', 'points_earned', 'answered_at')
        extra_kwargs = {
            'is_correct': {'read_only': True},
            'points_earned': {'read_only': True},
        }


class TestResponseSerializer(serializers.ModelSerializer):
    test_name = serializers.CharField(source='test.name', read_only=True)
    test_category = serializers.CharField(source='test.category', read_only=True)
    progress_percentage = serializers.ReadOnlyField()
    answers = AnswerSerializer(many=True, read_only=True)
    
    class Meta:
        model = TestResponse
        fields = ('id', 'test', 'test_name', 'test_category', 'started_at', 'completed_at', 
                 'is_completed', 'time_spent', 'attempt_number', 'progress_percentage', 'answers')


class TestRecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestRecommendation
        fields = ('recommendation_type', 'title', 'description', 'priority', 'url', 
                 'estimated_time', 'difficulty')


class TestResultSerializer(serializers.ModelSerializer):
    test_name = serializers.CharField(source='response.test.name', read_only=True)
    test_category = serializers.CharField(source='response.test.category', read_only=True)
    user_name = serializers.CharField(source='response.user.username', read_only=True)
    recommendations = TestRecommendationSerializer(many=True, read_only=True)
    
    class Meta:
        model = TestResult
        fields = ('test_name', 'test_category', 'user_name', 'personality_type', 
                 'skills_assessment', 'interests_profile', 'aptitude_scores',
                 'career_recommendations', 'strengths', 'areas_for_improvement', 
                 'skill_gaps', 'learning_suggestions', 'overall_score', 
                 'percentile_rank', 'passed', 'badge_earned', 'created_at', 'recommendations')


class TestResponseWithResultSerializer(serializers.ModelSerializer):
    test = CareerTestSummarySerializer(read_only=True)
    answers = AnswerSerializer(many=True, read_only=True)
    result = TestResultSerializer(read_only=True)
    progress_percentage = serializers.ReadOnlyField()
    
    class Meta:
        model = TestResponse
        fields = ('id', 'test', 'started_at', 'completed_at', 'is_completed', 
                 'time_spent', 'attempt_number', 'progress_percentage', 'answers', 'result')


class TestHistorySerializer(serializers.ModelSerializer):
    """Serializer for test history display"""
    test = CareerTestSummarySerializer(read_only=True)
    result = TestResultSerializer(read_only=True)
    
    class Meta:
        model = TestResponse
        fields = ('id', 'test', 'started_at', 'completed_at', 'is_completed', 
                 'time_spent', 'attempt_number', 'result')
