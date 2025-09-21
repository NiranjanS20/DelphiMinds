from django.urls import path
from .views import PostListCreateView, PostDetailView, CommentListCreateView, BenchmarkingView

urlpatterns = [
    path('posts/', PostListCreateView.as_view()),
    path('posts/<int:pk>/', PostDetailView.as_view()),
    path('posts/<int:post_id>/comments/', CommentListCreateView.as_view()),
    path('benchmark/', BenchmarkingView.as_view()),
]




