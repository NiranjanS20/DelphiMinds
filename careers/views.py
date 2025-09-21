from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.db.models import Count, Q, Sum
from django.db import models
from django.utils import timezone
from datetime import timedelta
from .models import (
    CareerPath, CareerRecommendation, RoadmapStep, ProjectRecommendation,
    PersonalizedRoadmap, RoadmapMilestone, LearningResource, SkillGapAnalysis, CareerProgressTracker
)
from .serializers import (
    CareerPathSerializer, CareerRecommendationSerializer, RoadmapStepSerializer, ProjectRecommendationSerializer,
    PersonalizedRoadmapSerializer, RoadmapMilestoneSerializer, LearningResourceSerializer, SkillGapAnalysisSerializer
)
from skills.models import UserSkill, Skill
from ml.recommender import score_career_paths
from ml.career_model import CareerRecommendationModel
from accounts.permissions import IsAdminOrReadOnly
import json


# Create your views here.


class CareerPathListCreateView(generics.ListCreateAPIView):
    queryset = CareerPath.objects.all().order_by('title')
    serializer_class = CareerPathSerializer
    permission_classes = [IsAdminOrReadOnly]


class CareerPathDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CareerPath.objects.all()
    serializer_class = CareerPathSerializer
    permission_classes = [IsAdminOrReadOnly]


class RecommendationListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        user_skill_levels = {us.skill_id: us.level for us in UserSkill.objects.filter(user=user).only('skill_id', 'level')}
        mapping = {cp.id: list(cp.required_skills.values_list('id', flat=True)) for cp in CareerPath.objects.all()}

        scored = score_career_paths(user_skill_levels, mapping)

        CareerRecommendation.objects.filter(user=user).delete()
        CareerRecommendation.objects.bulk_create([
            CareerRecommendation(user=user, career_path_id=cid, score=score)
            for cid, score in scored if score > 0
        ])

        queryset = CareerRecommendation.objects.filter(user=user).select_related('career_path').order_by('-score')
        data = CareerRecommendationSerializer(queryset, many=True).data
        return Response(data)


class RoadmapGenerateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        career_path_id = request.data.get('career_path_id')
        if not career_path_id:
            return Response({'detail': 'career_path_id required'}, status=400)
        # naive generator: one step per required skill if user level < 80
        RoadmapStep.objects.filter(user=user, career_path_id=career_path_id).delete()
        req_skill_ids = list(CareerPath.objects.get(id=career_path_id).required_skills.values_list('id', flat=True))
        user_levels = {us.skill_id: us.level for us in UserSkill.objects.filter(user=user, skill_id__in=req_skill_ids)}
        steps = []
        order = 1
        for sid in req_skill_ids:
            level = user_levels.get(sid, 0)
            if level < 80:
                steps.append(RoadmapStep(
                    user=user,
                    career_path_id=career_path_id,
                    skill_id=sid,
                    title=f"Improve {sid} to 80+",
                    description="Follow curated resources to reach proficiency.",
                    order=order,
                    estimated_hours=10,
                    resource_url="https://roadmap.sh/"
                ))
                order += 1
        if steps:
            RoadmapStep.objects.bulk_create(steps)
        data = RoadmapStepSerializer(RoadmapStep.objects.filter(user=user, career_path_id=career_path_id), many=True).data
        return Response(data)


class ProjectRecommendationView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        top = CareerRecommendation.objects.filter(user=user).order_by('-score').first()
        if not top:
            return Response([])
        ProjectRecommendation.objects.filter(user=user, career_path=top.career_path).delete()
        samples = [
            (f"Build a {top.career_path.title} demo", "Create a small app featuring core skills", 'intermediate'),
            ("Capstone portfolio project", "End-to-end project with docs and tests", 'advanced'),
        ]
        created = [ProjectRecommendation(user=user, career_path=top.career_path, title=t, description=d, difficulty=diff) for t, d, diff in samples]
        ProjectRecommendation.objects.bulk_create(created)
        data = ProjectRecommendationSerializer(ProjectRecommendation.objects.filter(user=user, career_path=top.career_path), many=True).data
        return Response(data)


class SimulationView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        # what-if: take provided skill adjustments and rescore
        user = request.user
        adjustments = request.data.get('adjustments', {})  # {skill_id: level}
        user_skill_levels = {us.skill_id: us.level for us in UserSkill.objects.filter(user=user).only('skill_id', 'level')}
        for sid, lvl in adjustments.items():
            try:
                sid_int = int(sid)
                user_skill_levels[sid_int] = int(lvl)
            except Exception:
                continue
        mapping = {cp.id: list(cp.required_skills.values_list('id', flat=True)) for cp in CareerPath.objects.all()}
        scored = score_career_paths(user_skill_levels, mapping)
        return Response([{ 'career_path_id': cid, 'score': score } for cid, score in scored])


class CareerRoadmapView(APIView):
    """Enhanced career roadmap endpoint using ML recommendations"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        user = request.user
        target_career = request.data.get('target_career')
        user_interests = request.data.get('interests', [])
        
        if not target_career:
            return Response(
                {'error': 'target_career is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get user skills from profile
        user_skills = {}
        if hasattr(user, 'profile') and user.profile.skills_json:
            user_skills = {skill['name']: skill['level'] for skill in user.profile.skills_json}
        
        # Use ML model for recommendations
        career_model = CareerRecommendationModel()
        roadmap = career_model.generate_learning_roadmap(user_skills, target_career)
        
        if 'error' in roadmap:
            return Response(roadmap, status=status.HTTP_404_NOT_FOUND)
        
        # Also get general career recommendations
        recommendations = career_model.recommend_careers(user_skills, user_interests)
        
        return Response({
            'roadmap': roadmap,
            'alternative_careers': recommendations[:5],
            'user_skills_count': len(user_skills),
            'recommendations': {
                'next_steps': self._generate_next_steps(roadmap),
                'resources': self._get_learning_resources(),
                'timeline': self._estimate_timeline(roadmap)
            }
        })
    
    def _generate_next_steps(self, roadmap):
        """Generate actionable next steps"""
        next_steps = []
        
        # Get first phase skills
        foundation_phase = roadmap.get('phases', {}).get('Foundation (0-3 months)', [])
        
        if foundation_phase:
            first_skill = foundation_phase[0]['skill']
            next_steps.append(f"Start learning {first_skill} - allocate 2-3 hours per week")
            next_steps.append("Set up a learning schedule and track your progress")
            next_steps.append("Join online communities related to your target career")
        
        next_steps.append("Update your LinkedIn profile to reflect your learning journey")
        next_steps.append("Start building a portfolio of projects")
        
        return next_steps[:5]
    
    def _get_learning_resources(self):
        """Get general learning resources"""
        return {
            'online_platforms': [
                {'name': 'Coursera', 'url': 'https://www.coursera.org/', 'type': 'University Courses'},
                {'name': 'Udemy', 'url': 'https://www.udemy.com/', 'type': 'Practical Courses'},
                {'name': 'FreeCodeCamp', 'url': 'https://www.freecodecamp.org/', 'type': 'Free Coding Bootcamp'},
                {'name': 'Pluralsight', 'url': 'https://www.pluralsight.com/', 'type': 'Tech Skills'},
                {'name': 'LinkedIn Learning', 'url': 'https://www.linkedin.com/learning/', 'type': 'Professional Skills'}
            ],
            'practice_platforms': [
                {'name': 'LeetCode', 'url': 'https://leetcode.com/', 'type': 'Coding Practice'},
                {'name': 'HackerRank', 'url': 'https://www.hackerrank.com/', 'type': 'Programming Challenges'},
                {'name': 'Kaggle', 'url': 'https://www.kaggle.com/', 'type': 'Data Science Competitions'},
                {'name': 'GitHub', 'url': 'https://github.com/', 'type': 'Project Hosting'}
            ]
        }
    
    def _estimate_timeline(self, roadmap):
        """Estimate learning timeline"""
        phases = roadmap.get('phases', {})
        total_hours = 0
        
        for phase_name, skills in phases.items():
            phase_hours = sum(skill.get('estimated_hours', 0) for skill in skills)
            total_hours += phase_hours
        
        weeks_at_10_hours = total_hours / 10  # Assuming 10 hours per week
        months = weeks_at_10_hours / 4.33  # Average weeks per month
        
        return {
            'total_estimated_hours': total_hours,
            'estimated_months_at_10h_week': round(months, 1),
            'estimated_months_at_5h_week': round(months * 2, 1),
            'recommendation': '10 hours per week for optimal progress'
        }


class PersonalizedRoadmapView(APIView):
    """Create and manage personalized roadmaps"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        """Get user's existing roadmaps"""
        roadmaps = PersonalizedRoadmap.objects.filter(user=request.user, is_active=True)
        serializer = PersonalizedRoadmapSerializer(roadmaps, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        """Create a new personalized roadmap"""
        data = request.data
        
        # Extract user inputs
        target_career_id = data.get('target_career_id')
        learning_style = data.get('learning_style', 'mixed')
        hours_per_week = data.get('hours_per_week', 10)
        current_skills = data.get('current_skills', {})
        
        if not target_career_id:
            return Response(
                {'error': 'target_career_id is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            target_career = CareerPath.objects.get(id=target_career_id)
        except CareerPath.DoesNotExist:
            return Response(
                {'error': 'Career path not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Check if user already has a roadmap for this career
        existing_roadmap = PersonalizedRoadmap.objects.filter(
            user=request.user, 
            target_career=target_career, 
            is_active=True
        ).first()
        
        if existing_roadmap:
            # Update existing roadmap
            existing_roadmap.learning_style = learning_style
            existing_roadmap.hours_per_week = hours_per_week
            existing_roadmap.save()
            roadmap = existing_roadmap
        else:
            # Create new roadmap
            roadmap = PersonalizedRoadmap.objects.create(
                user=request.user,
                target_career=target_career,
                title=f"Path to {target_career.title}",
                learning_style=learning_style,
                hours_per_week=hours_per_week
            )
        
        # Generate skill gap analysis
        self._generate_skill_gap_analysis(roadmap, current_skills)
        
        # Generate milestones
        self._generate_roadmap_milestones(roadmap, current_skills)
        
        # Calculate estimated completion time
        self._calculate_timeline(roadmap)
        
        serializer = PersonalizedRoadmapSerializer(roadmap)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def _generate_skill_gap_analysis(self, roadmap, current_skills):
        """Generate comprehensive skill gap analysis"""
        required_skills = {}
        for skill in roadmap.target_career.required_skills.all():
            required_skills[skill.name] = 80  # Assume 80 is proficient level
        
        missing_skills = []
        weak_skills = []
        strong_skills = []
        
        for skill_name, required_level in required_skills.items():
            current_level = current_skills.get(skill_name, 0)
            
            if current_level == 0:
                missing_skills.append(skill_name)
            elif current_level < required_level:
                weak_skills.append({
                    'skill': skill_name,
                    'current_level': current_level,
                    'required_level': required_level,
                    'gap': required_level - current_level
                })
            else:
                strong_skills.append({
                    'skill': skill_name,
                    'current_level': current_level,
                    'required_level': required_level
                })
        
        # Calculate skill match percentage
        total_skills = len(required_skills)
        matched_skills = len(strong_skills) + len([s for s in weak_skills if s['current_level'] >= s['required_level'] * 0.7])
        skill_match_percentage = (matched_skills / total_skills * 100) if total_skills > 0 else 0
        
        # Create or update skill gap analysis
        SkillGapAnalysis.objects.update_or_create(
            roadmap=roadmap,
            defaults={
                'current_skills': current_skills,
                'required_skills': required_skills,
                'missing_skills': missing_skills,
                'weak_skills': weak_skills,
                'strong_skills': strong_skills,
                'skill_match_percentage': skill_match_percentage
            }
        )
    
    def _generate_roadmap_milestones(self, roadmap, current_skills):
        """Generate comprehensive roadmap milestones"""
        # Clear existing milestones
        roadmap.milestones.all().delete()
        
        # Get skill gap analysis
        skill_gap = roadmap.skill_gap_analysis
        
        milestones = []
        order_foundation = 1
        order_intermediate = 1
        order_advanced = 1
        
        # Foundation Phase: Missing skills
        for skill_name in skill_gap.missing_skills:
            milestone = RoadmapMilestone(
                roadmap=roadmap,
                title=f"Learn {skill_name} Fundamentals",
                description=f"Start learning {skill_name} from scratch. Focus on basic concepts and hands-on practice.",
                phase='Foundation',
                order_in_phase=order_foundation,
                estimated_hours=20,
                estimated_weeks=3,
                priority='high' if order_foundation <= 3 else 'medium'
            )
            milestones.append(milestone)
            order_foundation += 1
        
        # Intermediate Phase: Weak skills
        for skill_info in skill_gap.weak_skills:
            milestone = RoadmapMilestone(
                roadmap=roadmap,
                title=f"Master {skill_info['skill']}",
                description=f"Improve your {skill_info['skill']} skills from level {skill_info['current_level']} to {skill_info['required_level']}.",
                phase='Intermediate',
                order_in_phase=order_intermediate,
                estimated_hours=15,
                estimated_weeks=2,
                priority='medium'
            )
            milestones.append(milestone)
            order_intermediate += 1
        
        # Advanced Phase: Specialization and Projects
        advanced_milestones = [
            {
                'title': 'Build Portfolio Project #1',
                'description': 'Create a comprehensive project showcasing your newly acquired skills.',
                'hours': 25,
                'weeks': 4
            },
            {
                'title': 'Gain Industry Certification',
                'description': 'Obtain a relevant certification to validate your skills.',
                'hours': 30,
                'weeks': 6
            },
            {
                'title': 'Build Portfolio Project #2',
                'description': 'Create an advanced project demonstrating mastery of the tech stack.',
                'hours': 35,
                'weeks': 5
            },
            {
                'title': 'Practice Technical Interviews',
                'description': 'Prepare for job interviews with coding challenges and system design.',
                'hours': 20,
                'weeks': 4
            },
            {
                'title': 'Network and Apply for Jobs',
                'description': 'Build professional network and start applying for positions.',
                'hours': 15,
                'weeks': 8
            }
        ]
        
        for adv_milestone in advanced_milestones:
            milestone = RoadmapMilestone(
                roadmap=roadmap,
                title=adv_milestone['title'],
                description=adv_milestone['description'],
                phase='Advanced',
                order_in_phase=order_advanced,
                estimated_hours=adv_milestone['hours'],
                estimated_weeks=adv_milestone['weeks'],
                priority='medium'
            )
            milestones.append(milestone)
            order_advanced += 1
        
        # Bulk create milestones
        RoadmapMilestone.objects.bulk_create(milestones)
        
        # Add learning resources to milestones
        self._add_learning_resources(roadmap)
    
    def _add_learning_resources(self, roadmap):
        """Add learning resources to milestones"""
        milestones = roadmap.milestones.all()
        
        # Resource templates based on learning style
        resource_templates = {
            'self_paced': [
                {'title': 'Coursera Course', 'type': 'course', 'provider': 'Coursera', 'cost': 'paid'},
                {'title': 'Free Tutorial Series', 'type': 'tutorial', 'provider': 'YouTube', 'cost': 'free'},
                {'title': 'Documentation', 'type': 'documentation', 'provider': 'Official Docs', 'cost': 'free'}
            ],
            'bootcamp': [
                {'title': 'Bootcamp Program', 'type': 'bootcamp', 'provider': 'Various', 'cost': 'paid'},
                {'title': 'Intensive Workshop', 'type': 'course', 'provider': 'Udemy', 'cost': 'paid'}
            ],
            'certification': [
                {'title': 'Official Certification', 'type': 'certification', 'provider': 'Industry Standard', 'cost': 'paid'},
                {'title': 'Practice Tests', 'type': 'practice', 'provider': 'Practice Platform', 'cost': 'freemium'}
            ]
        }
        
        style_resources = resource_templates.get(roadmap.learning_style, resource_templates['self_paced'])
        
        for milestone in milestones:
            for resource_template in style_resources:
                LearningResource.objects.create(
                    milestone=milestone,
                    title=f"{resource_template['title']} for {milestone.title}",
                    resource_type=resource_template['type'],
                    provider=resource_template['provider'],
                    cost_type=resource_template['cost'],
                    difficulty_level='beginner' if milestone.phase == 'Foundation' else 'intermediate',
                    is_recommended=True
                )
    
    def _calculate_timeline(self, roadmap):
        """Calculate estimated completion timeline"""
        total_hours = roadmap.milestones.aggregate(total=models.Sum('estimated_hours'))['total'] or 0
        estimated_weeks = total_hours / roadmap.hours_per_week
        
        roadmap.estimated_completion_weeks = int(estimated_weeks)
        roadmap.target_completion_date = timezone.now() + timedelta(weeks=estimated_weeks)
        roadmap.save()


class RoadmapMilestoneView(APIView):
    """Manage roadmap milestones"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, roadmap_id):
        """Get milestones for a specific roadmap"""
        try:
            roadmap = PersonalizedRoadmap.objects.get(id=roadmap_id, user=request.user)
        except PersonalizedRoadmap.DoesNotExist:
            return Response({'error': 'Roadmap not found'}, status=status.HTTP_404_NOT_FOUND)
        
        milestones = roadmap.milestones.all().order_by('phase', 'order_in_phase')
        serializer = RoadmapMilestoneSerializer(milestones, many=True)
        return Response(serializer.data)
    
    def patch(self, request, roadmap_id, milestone_id):
        """Update milestone status"""
        try:
            roadmap = PersonalizedRoadmap.objects.get(id=roadmap_id, user=request.user)
            milestone = roadmap.milestones.get(id=milestone_id)
        except (PersonalizedRoadmap.DoesNotExist, RoadmapMilestone.DoesNotExist):
            return Response({'error': 'Milestone not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Update milestone
        status_update = request.data.get('status')
        if status_update in ['pending', 'in_progress', 'completed', 'skipped']:
            milestone.status = status_update
            
            if status_update == 'completed':
                milestone.completion_date = timezone.now()
            elif status_update == 'in_progress':
                milestone.start_date = timezone.now()
            
            milestone.save()
            
            # Update roadmap progress
            roadmap.update_progress()
            
            # Create progress snapshot
            CareerProgressTracker.objects.create(
                roadmap=roadmap,
                completed_milestones=roadmap.milestones.filter(status='completed').count(),
                total_milestones=roadmap.milestones.count(),
                progress_percentage=roadmap.overall_progress_percentage,
                job_readiness_score=roadmap.job_readiness_score
            )
        
        # Add user notes if provided
        user_notes = request.data.get('user_notes')
        if user_notes:
            milestone.user_notes = user_notes
            milestone.save()
        
        serializer = RoadmapMilestoneSerializer(milestone)
        return Response(serializer.data)


class JobReadinessScoreView(APIView):
    """Calculate and return job readiness score"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, roadmap_id):
        """Get current job readiness score and breakdown"""
        try:
            roadmap = PersonalizedRoadmap.objects.get(id=roadmap_id, user=request.user)
        except PersonalizedRoadmap.DoesNotExist:
            return Response({'error': 'Roadmap not found'}, status=status.HTTP_404_NOT_FOUND)
        
        # Calculate detailed job readiness breakdown
        milestones = roadmap.milestones.all()
        completed_milestones = milestones.filter(status='completed')
        
        # Skills assessment (40% of score)
        skill_gap = getattr(roadmap, 'skill_gap_analysis', None)
        skills_score = skill_gap.skill_match_percentage if skill_gap else 0
        
        # Project completion (30% of score)
        project_milestones = milestones.filter(title__icontains='project')
        project_completion = (project_milestones.filter(status='completed').count() / 
                            max(project_milestones.count(), 1)) * 100
        
        # Certification (20% of score)
        cert_milestones = milestones.filter(title__icontains='certification')
        cert_completion = (cert_milestones.filter(status='completed').count() / 
                         max(cert_milestones.count(), 1)) * 100
        
        # Interview prep (10% of score)
        interview_milestones = milestones.filter(title__icontains='interview')
        interview_completion = (interview_milestones.filter(status='completed').count() / 
                              max(interview_milestones.count(), 1)) * 100
        
        # Calculate weighted score
        job_readiness_score = (
            skills_score * 0.4 + 
            project_completion * 0.3 + 
            cert_completion * 0.2 + 
            interview_completion * 0.1
        )
        
        # Update roadmap score
        roadmap.job_readiness_score = int(job_readiness_score)
        roadmap.save()
        
        return Response({
            'job_readiness_score': int(job_readiness_score),
            'breakdown': {
                'skills_assessment': {
                    'score': round(skills_score, 1),
                    'weight': '40%',
                    'description': 'Technical skills proficiency'
                },
                'project_portfolio': {
                    'score': round(project_completion, 1),
                    'weight': '30%',
                    'description': 'Completed projects and portfolio'
                },
                'certifications': {
                    'score': round(cert_completion, 1),
                    'weight': '20%',
                    'description': 'Industry certifications obtained'
                },
                'interview_readiness': {
                    'score': round(interview_completion, 1),
                    'weight': '10%',
                    'description': 'Interview preparation and practice'
                }
            },
            'recommendations': self._get_readiness_recommendations(job_readiness_score, {
                'skills': skills_score,
                'projects': project_completion,
                'certs': cert_completion,
                'interviews': interview_completion
            })
        })
    
    def _get_readiness_recommendations(self, overall_score, breakdown):
        """Generate recommendations based on job readiness score"""
        recommendations = []
        
        if overall_score < 30:
            recommendations.append("Focus on building fundamental skills - you're in the early learning phase")
        elif overall_score < 60:
            recommendations.append("Good progress! Continue building skills and start working on projects")
        elif overall_score < 80:
            recommendations.append("You're getting close! Focus on certifications and interview prep")
        else:
            recommendations.append("Excellent! You're ready to start applying for jobs")
        
        # Specific recommendations based on breakdown
        if breakdown['skills'] < 70:
            recommendations.append("Prioritize completing more skill-building milestones")
        
        if breakdown['projects'] < 50:
            recommendations.append("Build more portfolio projects to demonstrate your skills")
        
        if breakdown['certs'] < 50 and overall_score > 40:
            recommendations.append("Consider pursuing relevant industry certifications")
        
        if breakdown['interviews'] < 50 and overall_score > 60:
            recommendations.append("Start practicing technical interviews and coding challenges")
        
        return recommendations
