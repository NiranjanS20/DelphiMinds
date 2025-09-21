from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

# Create your models here.

class User(AbstractUser):
    class Role(models.TextChoices):
        STUDENT = 'student', 'Student'
        ADMIN = 'admin', 'Admin'

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.STUDENT)

    objects = UserManager()

    def __str__(self):
        return f"{self.username} ({self.role})"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=100, blank=True)
    current_role = models.CharField(max_length=100, blank=True)
    experience_years = models.PositiveIntegerField(default=0)
    education_level = models.CharField(max_length=50, blank=True)
    industry_interest = models.CharField(max_length=100, blank=True)
    career_goals = models.TextField(blank=True)
    skills_json = models.JSONField(default=list, blank=True)  # User's self-assessed skills
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    portfolio_url = models.URLField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    is_profile_complete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    @property
    def completion_percentage(self):
        """Calculate profile completion percentage"""
        fields = ['bio', 'phone', 'location', 'current_role', 'education_level', 'industry_interest']
        completed = sum(1 for field in fields if getattr(self, field))
        return int((completed / len(fields)) * 100)
