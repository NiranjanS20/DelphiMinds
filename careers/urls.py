from django.urls import path
from .views import (
    CareerPathListCreateView, CareerPathDetailView, RecommendationListView, 
    RoadmapGenerateView, ProjectRecommendationView, SimulationView, CareerRoadmapView,
    PersonalizedRoadmapView, RoadmapMilestoneView, JobReadinessScoreView
)

urlpatterns = [
    path('', RecommendationListView.as_view(), name='recommendations'),
    path('paths/', CareerPathListCreateView.as_view(), name='career-paths'),
    path('paths/<int:pk>/', CareerPathDetailView.as_view(), name='career-path-detail'),
    path('roadmap/', RoadmapGenerateView.as_view(), name='roadmap-generate'),
    path('career-roadmap/', CareerRoadmapView.as_view(), name='career-roadmap'),
    path('projects/', ProjectRecommendationView.as_view(), name='project-recommendations'),
    path('simulate/', SimulationView.as_view(), name='simulate-recommendations'),
    
    # New personalized roadmap endpoints
    path('personalized-roadmap/', PersonalizedRoadmapView.as_view(), name='personalized-roadmap'),
    path('roadmap/<int:roadmap_id>/milestones/', RoadmapMilestoneView.as_view(), name='roadmap-milestones'),
    path('roadmap/<int:roadmap_id>/milestones/<int:milestone_id>/', RoadmapMilestoneView.as_view(), name='milestone-update'),
    path('roadmap/<int:roadmap_id>/job-readiness/', JobReadinessScoreView.as_view(), name='job-readiness-score'),
]
