"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.views.static import serve as static_serve
from django.conf import settings
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('accounts.urls')),
    path('skills/', include('skills.urls')),
    path('recommendations/', include('careers.urls')),
    path('chatbot/', include('chatbot.urls')),
    path('insights/', include('insights.urls')),
    path('community/', include('community.urls')),
    path('gamification/', include('gamification.urls')),
    path('resume/', include('resume.urls')),
    # Homepage API endpoints
    path('api/auth-status/', views.auth_status, name='auth-status'),
    path('api/quick-login/', views.quick_login, name='quick-login'),
    path('api/dashboard-data/', views.dashboard_data, name='dashboard-data'),
    path('', TemplateView.as_view(template_name='career-advisor/index.html'), name='homepage'),
    path('index.html', TemplateView.as_view(template_name='index.html'), name='landing'),
    # Frontend routes served as templates
    path('login.html', TemplateView.as_view(template_name='login.html')), 
    path('signup.html', TemplateView.as_view(template_name='signup.html')),
    path('dashboard.html', TemplateView.as_view(template_name='dashboard.html')),
    path('chat.html', TemplateView.as_view(template_name='chat.html')),
    path('insights.html', TemplateView.as_view(template_name='insights.html')),
    path('community.html', TemplateView.as_view(template_name='community.html')),
    path('roadmap.html', TemplateView.as_view(template_name='roadmap.html')),
    path('resume.html', TemplateView.as_view(template_name='resume.html')),
    path('resume-analysis.html', TemplateView.as_view(template_name='resume-analysis.html')),
    path('psychometric.html', TemplateView.as_view(template_name='psychometric.html')),
    path('gamification.html', TemplateView.as_view(template_name='gamification.html')),
    # Career Advisor Assets
    path('career-advisor.js', static_serve, {
        'document_root': settings.BASE_DIR / 'frontend' / 'career-advisor',
        'path': 'career-advisor.js'
    }),
    # Authentication utilities
    path('auth-utils.js', static_serve, {
        'document_root': settings.BASE_DIR / 'frontend',
        'path': 'auth-utils.js'
    }),
    # Main app JavaScript
    path('app.js', static_serve, {
        'document_root': settings.BASE_DIR / 'frontend',
        'path': 'app.js'
    }),
]
