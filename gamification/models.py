from django.db import models
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

User = get_user_model()


class BadgeCategory(models.Model):
    """Categories for organizing badges"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50, default='🏆')
    color = models.CharField(max_length=7, default='#3B82F6')  # Hex color
    
    class Meta:
        verbose_name_plural = 'Badge Categories'
    
    def __str__(self):
        return self.name


class Badge(models.Model):
    """Enhanced badge system with categories and difficulty levels"""
    DIFFICULTY_LEVELS = [
        ('bronze', 'Bronze'),
        ('silver', 'Silver'),
        ('gold', 'Gold'),
        ('platinum', 'Platinum'),
    ]
    
    BADGE_TYPES = [
        ('skill', 'Skill Category'),
        ('roadmap', 'Career Roadmap Stage'),
        ('achievement', 'Achievement Type'),
        ('streak', 'Time-Based Streak'),
        ('community', 'Community Engagement'),
        ('certification', 'Certification'),
    ]
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(BadgeCategory, on_delete=models.CASCADE, related_name='badges')
    badge_type = models.CharField(max_length=20, choices=BADGE_TYPES, default='achievement')
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_LEVELS, default='bronze')
    icon = models.CharField(max_length=50, default='🏆')
    points_required = models.IntegerField(default=0)
    skill_category = models.CharField(max_length=50, blank=True, null=True)
    criteria = models.JSONField(default=dict, help_text="Criteria for earning this badge")
    is_active = models.BooleanField(default=True)
    is_hidden = models.BooleanField(default=False, help_text="Hidden until earned")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['difficulty', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.get_difficulty_display()})"
    
    @property
    def earned_count(self):
        return self.user_badges.count()


class UserBadge(models.Model):
    """Enhanced user badge tracking"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, related_name='user_badges')
    earned_at = models.DateTimeField(auto_now_add=True)
    progress = models.FloatField(default=0.0, help_text="Progress towards earning (0-100)")
    is_featured = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('user', 'badge')
        ordering = ['-earned_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.badge.name}"


class UserCertification(models.Model):
    """User certifications and achievements"""
    CERTIFICATION_TYPES = [
        ('technical', 'Technical Certification'),
        ('professional', 'Professional Certification'),
        ('course', 'Course Completion'),
        ('achievement', 'Personal Achievement'),
        ('project', 'Project Achievement'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='certifications')
    title = models.CharField(max_length=200)
    description = models.TextField()
    certification_type = models.CharField(max_length=20, choices=CERTIFICATION_TYPES)
    issuing_organization = models.CharField(max_length=200, blank=True)
    issue_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    certificate_url = models.URLField(blank=True)
    verification_url = models.URLField(blank=True)
    points_earned = models.IntegerField(default=0)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-issue_date']
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"
    
    @property
    def is_expired(self):
        if self.expiry_date:
            return timezone.now().date() > self.expiry_date
        return False


class Streak(models.Model):
    """Enhanced streak tracking"""
    STREAK_TYPES = [
        ('login', 'Daily Login'),
        ('learning', 'Daily Learning'),
        ('testing', 'Regular Testing'),
        ('roadmap', 'Roadmap Progress'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='streaks')
    streak_type = models.CharField(max_length=20, choices=STREAK_TYPES, default='login')
    current_streak = models.IntegerField(default=0)
    longest_streak = models.IntegerField(default=0)
    last_activity = models.DateTimeField(auto_now=True)
    streak_start_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'streak_type')
    
    def __str__(self):
        return f"{self.user.username}'s {self.get_streak_type_display()}: {self.current_streak}"
    
    def update_streak(self):
        """Update streak based on activity"""
        now = timezone.now()
        last_activity_date = self.last_activity.date()
        today = now.date()
        yesterday = today - timedelta(days=1)
        
        if last_activity_date == today:
            # Already updated today
            return
        elif last_activity_date == yesterday:
            # Continuing streak
            self.current_streak += 1
            if self.current_streak > self.longest_streak:
                self.longest_streak = self.current_streak
        else:
            # Streak broken
            self.current_streak = 1
            self.streak_start_date = now
        
        self.last_activity = now
        self.save()


class Leaderboard(models.Model):
    """Enhanced leaderboard with categories"""
    LEADERBOARD_TYPES = [
        ('overall', 'Overall Points'),
        ('monthly', 'Monthly Points'),
        ('skill', 'Skill Category'),
        ('tests', 'Test Scores'),
        ('streaks', 'Longest Streaks'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leaderboard_entries')
    leaderboard_type = models.CharField(max_length=20, choices=LEADERBOARD_TYPES, default='overall')
    total_points = models.IntegerField(default=0)
    rank = models.IntegerField(default=0)
    category = models.CharField(max_length=50, blank=True)  # For skill-specific leaderboards
    period_start = models.DateTimeField(null=True, blank=True)  # For time-based leaderboards
    period_end = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-total_points', 'updated_at']
        unique_together = ('user', 'leaderboard_type', 'category')
    
    def __str__(self):
        return f"{self.user.username} - {self.get_leaderboard_type_display()}: #{self.rank}"


class Achievement(models.Model):
    """Enhanced achievement tracking"""
    ACHIEVEMENT_TYPES = [
        ('learning', 'Learning Milestone'),
        ('project', 'Project Milestone'),
        ('assessment', 'Assessment Milestone'),
        ('community', 'Community Engagement'),
        ('roadmap', 'Roadmap Progress'),
        ('certification', 'Certification Achievement'),
        ('competition', 'Competition & Hackathon'),
        ('internship', 'Internship & Work Experience'),
        ('workshop', 'Workshop & Training'),
        ('publication', 'Publication & Research'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='achievements')
    title = models.CharField(max_length=100)
    description = models.TextField()
    achievement_type = models.CharField(max_length=20, choices=ACHIEVEMENT_TYPES)
    points_earned = models.IntegerField(default=0)
    badge_awarded = models.ForeignKey(Badge, on_delete=models.SET_NULL, null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)  # Additional achievement data
    achieved_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-achieved_at']
    
    def __str__(self):
        return f"{self.user.username}: {self.title}"


class UserProfile(models.Model):
    """Extended user profile for gamification"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='gamification_profile')
    total_points = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    experience_points = models.IntegerField(default=0)
    next_level_points = models.IntegerField(default=100)
    favorite_badge = models.ForeignKey(Badge, on_delete=models.SET_NULL, null=True, blank=True)
    public_profile = models.BooleanField(default=True)
    join_date = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - Level {self.level}"
    
    def add_points(self, points):
        """Add points and check for level up"""
        self.total_points += points
        self.experience_points += points
        
        # Check for level up
        while self.experience_points >= self.next_level_points:
            self.experience_points -= self.next_level_points
            self.level += 1
            self.next_level_points = self.level * 100  # Progressive difficulty
        
        self.save()
        return self.level
