from rest_framework import serializers
from .models import Resume, ResumeAnalysis, JobMatch


class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ('id', 'title', 'file', 'uploaded_at', 'analysis_completed')
        read_only_fields = ('id', 'uploaded_at', 'analysis_completed')


class ResumeAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumeAnalysis
        fields = ('overall_score', 'keyword_matches', 'missing_skills', 'suggestions', 
                 'strengths', 'weaknesses', 'created_at')


class JobMatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobMatch
        fields = ('id', 'job_title', 'match_percentage', 'missing_requirements', 'recommendations')


class ResumeWithAnalysisSerializer(serializers.ModelSerializer):
    analysis = ResumeAnalysisSerializer(read_only=True)
    job_matches = JobMatchSerializer(many=True, read_only=True)
    
    class Meta:
        model = Resume
        fields = ('id', 'title', 'file', 'uploaded_at', 'analysis_completed', 'analysis', 'job_matches')
