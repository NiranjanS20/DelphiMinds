from django.core.management.base import BaseCommand
from gamification.models import Badge


class Command(BaseCommand):
    help = 'Seed gamification data'

    def handle(self, *args, **options):
        badges_data = [
            {
                'name': 'First Steps',
                'description': 'Complete your first skill assessment',
                'icon': '🎯',
                'points_required': 10,
                'skill_category': 'general'
            },
            {
                'name': 'Python Master',
                'description': 'Achieve expert level in Python programming',
                'icon': '🐍',
                'points_required': 50,
                'skill_category': 'programming'
            },
            {
                'name': 'JavaScript Ninja',
                'description': 'Master JavaScript and frontend development',
                'icon': '⚡',
                'points_required': 50,
                'skill_category': 'programming'
            },
            {
                'name': 'Data Scientist',
                'description': 'Excel in data science and machine learning',
                'icon': '📊',
                'points_required': 75,
                'skill_category': 'data_science'
            },
            {
                'name': 'Team Player',
                'description': 'Actively participate in community discussions',
                'icon': '👥',
                'points_required': 25,
                'skill_category': 'community'
            },
            {
                'name': 'Resume Expert',
                'description': 'Upload and analyze your first resume',
                'icon': '📄',
                'points_required': 15,
                'skill_category': 'career'
            },
            {
                'name': 'Test Taker',
                'description': 'Complete your first psychometric test',
                'icon': '🧠',
                'points_required': 20,
                'skill_category': 'assessment'
            },
            {
                'name': 'Streak Master',
                'description': 'Maintain a 7-day learning streak',
                'icon': '🔥',
                'points_required': 30,
                'skill_category': 'consistency'
            }
        ]

        for badge_data in badges_data:
            badge, created = Badge.objects.get_or_create(
                name=badge_data['name'],
                defaults=badge_data
            )
            if created:
                self.stdout.write(f'Created badge: {badge.name}')
            else:
                self.stdout.write(f'Badge already exists: {badge.name}')

        self.stdout.write(self.style.SUCCESS('Successfully seeded gamification data'))
