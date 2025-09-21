from django.urls import path
from .views import (
    JobMarketDataListCreateView, JobMarketDataDetailView,
    IndustryTrendListCreateView, IndustryTrendDetailView,
    JobInsightsView
)

urlpatterns = [
    path('', JobInsightsView.as_view(), name='job-insights'),
    path('jobs/', JobMarketDataListCreateView.as_view()),
    path('jobs/<int:pk>/', JobMarketDataDetailView.as_view()),
    path('trends/', IndustryTrendListCreateView.as_view()),
    path('trends/<int:pk>/', IndustryTrendDetailView.as_view()),
]



