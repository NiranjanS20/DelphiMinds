from rest_framework import serializers
from .models import (
    BadgeCategory, Badge, UserBadge, UserCertification, Streak, 
    Leaderboard, Achievement, UserProfile
)


class BadgeCategorySerializer(serializers.ModelSerializer):
    badge_count = serializers.SerializerMethodField()
    
    class Meta:
        model = BadgeCategory
        fields = ('id', 'name', 'description', 'icon', 'color', 'badge_count')
    
    def get_badge_count(self, obj):
        return obj.badges.filter(is_active=True).count()


class BadgeSerializer(serializers.ModelSerializer):
    category = BadgeCategorySerializer(read_only=True)
    earned_count = serializers.ReadOnlyField()
    is_earned = serializers.SerializerMethodField()
    progress = serializers.SerializerMethodField()
    
    class Meta:
        model = Badge
        fields = ('id', 'name', 'description', 'category', 'badge_type', 'difficulty', 
                 'icon', 'points_required', 'skill_category', 'criteria', 'is_active',
                 'earned_count', 'is_earned', 'progress')
    
    def get_is_earned(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.user_badges.filter(user=request.user).exists()
        return False
    
    def get_progress(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            user_badge = obj.user_badges.filter(user=request.user).first()
            return user_badge.progress if user_badge else 0.0
        return 0.0


class UserBadgeSerializer(serializers.ModelSerializer):
    badge = BadgeSerializer(read_only=True)
    
    class Meta:
        model = UserBadge
        fields = ('id', 'badge', 'earned_at', 'progress', 'is_featured')


class UserCertificationSerializer(serializers.ModelSerializer):
    is_expired = serializers.ReadOnlyField()
    
    class Meta:
        model = UserCertification
        fields = ('id', 'title', 'description', 'certification_type', 'issuing_organization',
                 'issue_date', 'expiry_date', 'certificate_url', 'verification_url',
                 'points_earned', 'is_verified', 'is_expired', 'created_at')


class StreakSerializer(serializers.ModelSerializer):
    class Meta:
        model = Streak
        fields = ('streak_type', 'current_streak', 'longest_streak', 'last_activity', 'streak_start_date')


class LeaderboardSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    user_level = serializers.IntegerField(source='user.gamification_profile.level', read_only=True)
    
    class Meta:
        model = Leaderboard
        fields = ('username', 'user_level', 'leaderboard_type', 'total_points', 'rank', 
                 'category', 'updated_at')


class AchievementSerializer(serializers.ModelSerializer):
    badge_awarded = BadgeSerializer(read_only=True)
    
    class Meta:
        model = Achievement
        fields = ('id', 'title', 'description', 'achievement_type', 'points_earned', 
                 'badge_awarded', 'metadata', 'achieved_at')


class UserProfileSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    favorite_badge = BadgeSerializer(read_only=True)
    recent_achievements = serializers.SerializerMethodField()
    active_streaks = serializers.SerializerMethodField()
    
    class Meta:
        model = UserProfile
        fields = ('user_name', 'total_points', 'level', 'experience_points', 'next_level_points',
                 'favorite_badge', 'public_profile', 'join_date', 'last_activity',
                 'recent_achievements', 'active_streaks')
    
    def get_recent_achievements(self, obj):
        recent = obj.user.achievements.order_by('-achieved_at')[:5]
        return AchievementSerializer(recent, many=True).data
    
    def get_active_streaks(self, obj):
        streaks = obj.user.streaks.filter(current_streak__gt=0)
        return StreakSerializer(streaks, many=True).data
