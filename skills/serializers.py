from rest_framework import serializers
from .models import Skill, UserSkill


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ('id', 'name', 'category')


class UserSkillSerializer(serializers.ModelSerializer):
    skill = SkillSerializer(read_only=True)
    skill_id = serializers.PrimaryKeyRelatedField(queryset=Skill.objects.all(), source='skill', write_only=True)

    class Meta:
        model = UserSkill
        fields = ('id', 'skill', 'skill_id', 'level', 'updated_at')
        read_only_fields = ('id', 'updated_at', 'skill')
