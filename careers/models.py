from django.db import models
from django.conf import settings
from skills.models import Skill
import json

# Create your models here.


class CareerPath(models.Model):
    title = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True)
    required_skills = models.ManyToManyField(Skill, related_name='career_paths')
    entry_level_salary = models.IntegerField(null=True, blank=True)
    mid_level_salary = models.IntegerField(null=True, blank=True)
    senior_level_salary = models.IntegerField(null=True, blank=True)
    growth_rate = models.CharField(max_length=10, blank=True, help_text="e.g., +15%")
    demand_level = models.CharField(max_length=20, default='Medium', choices=[
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Very High', 'Very High')
    ])

    def __str__(self):
        return self.title


class PersonalizedRoadmap(models.Model):
    """Main roadmap for a user targeting a specific career"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='roadmaps')
    target_career = models.ForeignKey(CareerPath, on_delete=models.CASCADE, related_name='user_roadmaps')
    title = models.CharField(max_length=200)
    learning_style = models.CharField(max_length=50, choices=[
        ('self_paced', 'Self-Paced Courses'),
        ('bootcamp', 'Bootcamps'),
        ('certification', 'Certifications'),
        ('mixed', 'Mixed Approach')
    ], default='mixed')
    hours_per_week = models.IntegerField(default=10, help_text="Available study hours per week")
    estimated_completion_weeks = models.IntegerField(null=True, blank=True)
    start_date = models.DateTimeField(auto_now_add=True)
    target_completion_date = models.DateTimeField(null=True, blank=True)
    current_phase = models.CharField(max_length=100, default='Foundation')
    overall_progress_percentage = models.FloatField(default=0.0)
    job_readiness_score = models.IntegerField(default=0, help_text="Score 0-100 for job readiness")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['user', 'target_career']

    def __str__(self):
        return f"{self.user.username} -> {self.target_career.title}"

    def update_progress(self):
        """Calculate and update overall progress"""
        milestones = self.milestones.all()
        if milestones.exists():
            completed = milestones.filter(status='completed').count()
            self.overall_progress_percentage = (completed / milestones.count()) * 100
        else:
            self.overall_progress_percentage = 0
        
        # Update job readiness score based on completed milestones
        self.job_readiness_score = min(int(self.overall_progress_percentage * 0.9), 100)
        self.save()


class RoadmapMilestone(models.Model):
    """Individual milestones within a roadmap"""
    roadmap = models.ForeignKey(PersonalizedRoadmap, on_delete=models.CASCADE, related_name='milestones')
    title = models.CharField(max_length=200)
    description = models.TextField()
    phase = models.CharField(max_length=100, choices=[
        ('Foundation', 'Foundation (0-3 months)'),
        ('Intermediate', 'Intermediate (3-6 months)'),
        ('Advanced', 'Advanced (6-12 months)'),
        ('Specialization', 'Specialization (12+ months)')
    ])
    order_in_phase = models.IntegerField(default=0)
    estimated_hours = models.IntegerField(default=10)
    estimated_weeks = models.IntegerField(default=2)
    prerequisites = models.ManyToManyField('self', blank=True, symmetrical=False)
    related_skills = models.ManyToManyField(Skill, blank=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('skipped', 'Skipped')
    ], default='pending')
    priority = models.CharField(max_length=10, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical')
    ], default='medium')
    start_date = models.DateTimeField(null=True, blank=True)
    completion_date = models.DateTimeField(null=True, blank=True)
    user_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['phase', 'order_in_phase']

    def __str__(self):
        return f"{self.roadmap.title} - {self.title}"


class LearningResource(models.Model):
    """Learning resources for milestones"""
    milestone = models.ForeignKey(RoadmapMilestone, on_delete=models.CASCADE, related_name='resources')
    title = models.CharField(max_length=200)
    resource_type = models.CharField(max_length=50, choices=[
        ('course', 'Online Course'),
        ('book', 'Book'),
        ('tutorial', 'Tutorial'),
        ('documentation', 'Documentation'),
        ('video', 'Video'),
        ('practice', 'Practice Platform'),
        ('project', 'Project Template'),
        ('certification', 'Certification'),
        ('bootcamp', 'Bootcamp')
    ])
    url = models.URLField(blank=True)
    provider = models.CharField(max_length=100, blank=True, help_text="e.g., Coursera, Udemy, YouTube")
    cost_type = models.CharField(max_length=20, choices=[
        ('free', 'Free'),
        ('paid', 'Paid'),
        ('freemium', 'Freemium')
    ], default='free')
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    difficulty_level = models.CharField(max_length=20, choices=[
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced')
    ], default='beginner')
    rating = models.FloatField(null=True, blank=True, help_text="User rating 0-5")
    is_recommended = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.resource_type})"


class SkillGapAnalysis(models.Model):
    """Analysis of skill gaps for a user's target career"""
    roadmap = models.OneToOneField(PersonalizedRoadmap, on_delete=models.CASCADE, related_name='skill_gap_analysis')
    current_skills = models.JSONField(default=dict, help_text="Current skills with levels")
    required_skills = models.JSONField(default=dict, help_text="Required skills for target career")
    missing_skills = models.JSONField(default=list, help_text="List of missing skills")
    weak_skills = models.JSONField(default=list, help_text="Skills below required level")
    strong_skills = models.JSONField(default=list, help_text="Skills above required level")
    skill_match_percentage = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Skill Gap Analysis - {self.roadmap.title}"


class CareerProgressTracker(models.Model):
    """Track user's progress over time"""
    roadmap = models.ForeignKey(PersonalizedRoadmap, on_delete=models.CASCADE, related_name='progress_snapshots')
    completed_milestones = models.IntegerField(default=0)
    total_milestones = models.IntegerField(default=0)
    progress_percentage = models.FloatField(default=0.0)
    job_readiness_score = models.IntegerField(default=0)
    skills_acquired = models.JSONField(default=list)
    time_spent_hours = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.roadmap.title} Progress - {self.progress_percentage}%"


class CareerRecommendation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='career_recommendations')
    career_path = models.ForeignKey(CareerPath, on_delete=models.CASCADE, related_name='recommendations')
    score = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-score', '-created_at']

    def __str__(self):
        return f"{self.user.username} -> {self.career_path.title} ({self.score:.2f})"


class RoadmapStep(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='roadmap_steps')
    career_path = models.ForeignKey('CareerPath', on_delete=models.CASCADE, related_name='roadmaps')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='roadmap_steps')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    estimated_hours = models.PositiveIntegerField(default=4)
    resource_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']


class ProjectRecommendation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='project_recommendations')
    career_path = models.ForeignKey('CareerPath', on_delete=models.CASCADE, related_name='project_recommendations')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    difficulty = models.CharField(max_length=50, default='intermediate')
    repo_template_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
