from rest_framework import serializers
from .models import (
    CareerPath, CareerRecommendation, RoadmapStep, ProjectRecommendation,
    PersonalizedRoadmap, RoadmapMilestone, LearningResource, SkillGapAnalysis, CareerProgressTracker
)
from skills.serializers import SkillSerializer
from skills.models import Skill


class CareerPathSerializer(serializers.ModelSerializer):
    required_skills = SkillSerializer(many=True, read_only=True)
    required_skill_ids = serializers.PrimaryKeyRelatedField(many=True, write_only=True, queryset=Skill.objects.all(), source='required_skills')
    salary_range = serializers.SerializerMethodField()

    class Meta:
        model = CareerPath
        fields = ('id', 'title', 'description', 'required_skills', 'required_skill_ids', 
                 'entry_level_salary', 'mid_level_salary', 'senior_level_salary', 
                 'growth_rate', 'demand_level', 'salary_range')
    
    def get_salary_range(self, obj):
        return {
            'entry': obj.entry_level_salary,
            'mid': obj.mid_level_salary,
            'senior': obj.senior_level_salary,
            'growth_rate': obj.growth_rate
        }


class CareerRecommendationSerializer(serializers.ModelSerializer):
    career_path = CareerPathSerializer(read_only=True)

    class Meta:
        model = CareerRecommendation
        fields = ('id', 'career_path', 'score', 'created_at')


class RoadmapStepSerializer(serializers.ModelSerializer):
    skill_name = serializers.CharField(source='skill.name', read_only=True)
    career_title = serializers.CharField(source='career_path.title', read_only=True)

    class Meta:
        model = RoadmapStep
        fields = ('id', 'user', 'career_path', 'career_title', 'skill', 'skill_name', 'title', 'description', 'order', 'estimated_hours', 'resource_url', 'created_at')
        read_only_fields = ('id', 'created_at', 'user', 'career_title', 'skill_name')


class ProjectRecommendationSerializer(serializers.ModelSerializer):
    career_title = serializers.CharField(source='career_path.title', read_only=True)

    class Meta:
        model = ProjectRecommendation
        fields = ('id', 'user', 'career_path', 'career_title', 'title', 'description', 'difficulty', 'repo_template_url', 'created_at')
        read_only_fields = ('id', 'created_at', 'user', 'career_title')


class LearningResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningResource
        fields = '__all__'
        read_only_fields = ('id', 'created_at')


class RoadmapMilestoneSerializer(serializers.ModelSerializer):
    resources = LearningResourceSerializer(many=True, read_only=True)
    related_skills = SkillSerializer(many=True, read_only=True)
    prerequisites_info = serializers.SerializerMethodField()
    
    class Meta:
        model = RoadmapMilestone
        fields = '__all__'
        read_only_fields = ('id', 'created_at')
    
    def get_prerequisites_info(self, obj):
        return [{'id': p.id, 'title': p.title, 'status': p.status} for p in obj.prerequisites.all()]


class SkillGapAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillGapAnalysis
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')


class CareerProgressTrackerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CareerProgressTracker
        fields = '__all__'
        read_only_fields = ('id', 'created_at')


class PersonalizedRoadmapSerializer(serializers.ModelSerializer):
    target_career = CareerPathSerializer(read_only=True)
    target_career_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=CareerPath.objects.all(), source='target_career')
    milestones = RoadmapMilestoneSerializer(many=True, read_only=True)
    skill_gap_analysis = SkillGapAnalysisSerializer(read_only=True)
    progress_snapshots = CareerProgressTrackerSerializer(many=True, read_only=True)
    milestone_summary = serializers.SerializerMethodField()
    
    class Meta:
        model = PersonalizedRoadmap
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at', 'overall_progress_percentage', 'job_readiness_score')
    
    def get_milestone_summary(self, obj):
        milestones = obj.milestones.all()
        total = milestones.count()
        completed = milestones.filter(status='completed').count()
        in_progress = milestones.filter(status='in_progress').count()
        pending = milestones.filter(status='pending').count()
        
        return {
            'total': total,
            'completed': completed,
            'in_progress': in_progress,
            'pending': pending,
            'completion_rate': round((completed / total * 100) if total > 0 else 0, 1)
        }
