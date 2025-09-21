from django.urls import path
from . import views

urlpatterns = [
    # Test listing and details
    path('tests/', views.CareerTestListView.as_view(), name='test-list'),
    path('tests/<int:pk>/', views.CareerTestDetailView.as_view(), name='test-detail'),
    
    # Test responses and history
    path('responses/', views.TestHistoryView.as_view(), name='response-list'),
    path('responses/<int:pk>/', views.TestResponseDetailView.as_view(), name='response-detail'),
    
    # Test execution
    path('start/<int:test_id>/', views.start_test, name='start-test'),
    path('submit-answer/<int:response_id>/', views.submit_answer, name='submit-answer'),
    path('complete/<int:response_id>/', views.complete_test, name='complete-test'),
    path('result/<int:response_id>/', views.get_test_result, name='get-result'),
    
    # User statistics and recommendations
    path('user-stats/', views.get_user_stats, name='user-stats'),
    path('recommendations/', views.get_test_recommendations, name='test-recommendations'),
    
    # Backward compatibility
    path('psychometric-tests/', views.PsychometricTestListView.as_view(), name='psychometric-test-list'),
]
