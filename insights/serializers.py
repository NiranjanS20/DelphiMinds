from rest_framework import serializers
from .models import JobMarketData, IndustryTrend
from skills.models import Skill


class JobMarketDataSerializer(serializers.ModelSerializer):
    skill_name = serializers.CharField(source='skill.name', read_only=True)

    class Meta:
        model = JobMarketData
        fields = ('id', 'skill', 'skill_name', 'demand_score', 'salary_range_min', 'salary_range_max', 'job_openings', 'growth_rate', 'last_updated')


class IndustryTrendSerializer(serializers.ModelSerializer):
    skills_in_demand = serializers.PrimaryKeyRelatedField(many=True, read_only=False, queryset=Skill.objects.all())

    class Meta:
        model = IndustryTrend
        fields = ('id', 'name', 'description', 'growth_rate', 'avg_salary', 'skills_in_demand', 'last_updated')


