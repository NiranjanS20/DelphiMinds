from django.urls import path
from .views import SkillListCreateView, UserSkillListCreateView, UserSkillDetailView

urlpatterns = [
    path('', SkillListCreateView.as_view(), name='skills-list-create'),
    path('my/', UserSkillListCreateView.as_view(), name='user-skills'),
    path('my/<int:pk>/', UserSkillDetailView.as_view(), name='user-skill-detail'),
]
