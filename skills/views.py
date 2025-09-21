from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import Skill, UserSkill
from .serializers import SkillSerializer, UserSkillSerializer
from accounts.permissions import IsAdminOrReadOnly


class SkillListCreateView(generics.ListCreateAPIView):
    queryset = Skill.objects.all().order_by('name')
    serializer_class = SkillSerializer
    permission_classes = [IsAdminOrReadOnly]


class UserSkillListCreateView(generics.ListCreateAPIView):
    serializer_class = UserSkillSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserSkill.objects.filter(user=self.request.user).select_related('skill').order_by('-updated_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserSkillDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSkillSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserSkill.objects.filter(user=self.request.user)
