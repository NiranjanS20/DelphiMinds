from django.urls import path
from . import views

urlpatterns = [
    path('', views.ResumeListCreateView.as_view(), name='resume-list'),
    path('<int:pk>/', views.ResumeDetailView.as_view(), name='resume-detail'),
    path('analyze/', views.analyze_resume_enhanced, name='analyze-resume-enhanced'),
    path('analyze/advanced/', views.analyze_resume_advanced_insights, name='analyze-resume-advanced'),
    path('<int:resume_id>/analysis/', views.get_analysis, name='get-analysis'),
    path('debug/', views.debug_auth, name='debug-auth'),
]
