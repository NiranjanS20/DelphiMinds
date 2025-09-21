from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

User = get_user_model()


class CareerTest(models.Model):
    """Enhanced test model for multiple test types"""
    TEST_CATEGORIES = [
        ('psychometric', 'Psychometric Test'),
        ('skills', 'Skills Assessment'),
        ('aptitude', 'Aptitude Test'),
        ('interests', 'Career Interest Test'),
        ('custom', 'Custom DelphiMinds Test'),
    ]
    
    DIFFICULTY_LEVELS = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=TEST_CATEGORIES)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_LEVELS, default='medium')
    estimated_time = models.IntegerField(help_text="Estimated time in minutes")
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    instructions = models.TextField(blank=True)
    passing_score = models.FloatField(default=70.0)
    max_attempts = models.IntegerField(default=3)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-is_featured', '-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"
    
    @property
    def total_questions(self):
        return self.questions.count()
    
    @property
    def average_score(self):
        completed_results = self.test_results.filter(is_completed=True)
        if completed_results.exists():
            return completed_results.aggregate(avg_score=models.Avg('overall_score'))['avg_score']
        return 0.0


class PsychometricTest(CareerTest):
    """Proxy model for backward compatibility"""
    class Meta:
        proxy = True


class Question(models.Model):
    """Enhanced question model with multiple question types"""
    QUESTION_TYPES = [
        ('multiple_choice', 'Multiple Choice'),
        ('scale', 'Rating Scale'),
        ('text', 'Text Response'),
        ('boolean', 'Yes/No'),
        ('ranking', 'Ranking'),
    ]
    
    test = models.ForeignKey(CareerTest, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES, default='multiple_choice')
    options = models.JSONField(default=list, blank=True)  # For multiple choice
    correct_answer = models.TextField(blank=True)  # For aptitude/skills tests
    points = models.IntegerField(default=1)
    order = models.IntegerField(default=0)
    is_required = models.BooleanField(default=True)
    explanation = models.TextField(blank=True)  # Explanation for correct answer
    
    class Meta:
        ordering = ['order']
        unique_together = ('test', 'order')
    
    def __str__(self):
        return f"{self.test.name} - Q{self.order}: {self.text[:50]}"


class TestResponse(models.Model):
    """Enhanced test response model"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='test_responses')
    test = models.ForeignKey(CareerTest, on_delete=models.CASCADE, related_name='responses')
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    time_spent = models.DurationField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    attempt_number = models.IntegerField(default=1)
    
    class Meta:
        ordering = ['-started_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.test.name} (Attempt #{self.attempt_number})"
    
    def complete_test(self):
        """Mark test as completed and calculate time spent"""
        self.completed_at = timezone.now()
        self.is_completed = True
        self.time_spent = self.completed_at - self.started_at
        self.save()
    
    @property
    def progress_percentage(self):
        total_questions = self.test.questions.count()
        answered_questions = self.answers.count()
        if total_questions > 0:
            return (answered_questions / total_questions) * 100
        return 0


class Answer(models.Model):
    """Enhanced answer model"""
    response = models.ForeignKey(TestResponse, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.TextField()
    answer_value = models.FloatField(null=True, blank=True)  # For numeric answers
    is_correct = models.BooleanField(null=True, blank=True)  # For aptitude/skills tests
    points_earned = models.IntegerField(default=0)
    answered_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('response', 'question')
    
    def __str__(self):
        return f"{self.response.user.username} - {self.question.text[:30]}..."
    
    def save(self, *args, **kwargs):
        # Auto-calculate correctness for aptitude/skills tests
        if self.question.correct_answer and self.answer_text:
            self.is_correct = self.answer_text.strip().lower() == self.question.correct_answer.strip().lower()
            if self.is_correct:
                self.points_earned = self.question.points
        super().save(*args, **kwargs)


class TestResult(models.Model):
    """Enhanced test result model"""
    response = models.OneToOneField(TestResponse, on_delete=models.CASCADE, related_name='result')
    personality_type = models.CharField(max_length=100, blank=True)  # MBTI, Big Five, etc.
    skills_assessment = models.JSONField(default=dict)  # {skill: score}
    interests_profile = models.JSONField(default=dict)  # RIASEC scores
    aptitude_scores = models.JSONField(default=dict)  # logical, numerical, verbal
    career_recommendations = models.JSONField(default=list)
    strengths = models.JSONField(default=list)
    areas_for_improvement = models.JSONField(default=list)
    skill_gaps = models.JSONField(default=list)
    learning_suggestions = models.JSONField(default=list)
    overall_score = models.FloatField(default=0.0)
    percentile_rank = models.FloatField(default=0.0)
    passed = models.BooleanField(default=False)
    badge_earned = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Result: {self.response.user.username} - {self.response.test.name} ({self.overall_score:.1f}%)"
    
    def calculate_score(self):
        """Calculate overall score based on answers"""
        if self.response.test.category in ['aptitude', 'skills']:
            # For aptitude/skills tests, use correct answers
            total_points = self.response.answers.aggregate(total=models.Sum('points_earned'))['total'] or 0
            max_points = self.response.test.questions.aggregate(total=models.Sum('points'))['total'] or 1
            self.overall_score = (total_points / max_points) * 100
        else:
            # For personality/interest tests, use custom scoring logic
            self._calculate_personality_score()
        
        self.passed = self.overall_score >= self.response.test.passing_score
        self.save()
    
    def _calculate_personality_score(self):
        """Custom scoring for personality and interest tests"""
        # Implement specific scoring logic based on test type
        answers = self.response.answers.all()
        if answers.exists():
            # Simple average for now - can be enhanced with specific algorithms
            avg_value = answers.aggregate(avg=models.Avg('answer_value'))['avg'] or 0
            self.overall_score = min(avg_value * 20, 100)  # Convert to percentage


class TestRecommendation(models.Model):
    """AI-generated recommendations based on test results"""
    test_result = models.ForeignKey(TestResult, on_delete=models.CASCADE, related_name='recommendations')
    recommendation_type = models.CharField(max_length=50)  # career, course, skill, project
    title = models.CharField(max_length=200)
    description = models.TextField()
    priority = models.CharField(max_length=10, choices=[
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low')
    ], default='medium')
    url = models.URLField(blank=True)
    estimated_time = models.CharField(max_length=50, blank=True)
    difficulty = models.CharField(max_length=10, blank=True)
    
    class Meta:
        ordering = ['priority', '-id']
    
    def __str__(self):
        return f"{self.recommendation_type}: {self.title}"
