from django.urls import path
from . import views

urlpatterns = [
    path('badges/', views.BadgeListView.as_view(), name='badge-list'),
    path('my-badges/', views.UserBadgeListView.as_view(), name='user-badge-list'),
    path('streak/', views.StreakView.as_view(), name='streak'),
    path('leaderboard/', views.LeaderboardView.as_view(), name='leaderboard'),
    path('achievements/', views.user_achievements, name='user-achievements'),
    path('certifications/', views.user_certifications, name='user-certifications'),
    path('update-streak/', views.update_streak, name='update-streak'),
    path('award-badge/<int:badge_id>/', views.award_badge, name='award-badge'),
]
