from django.core.management.base import BaseCommand
from skills.models import Skill
from careers.models import CareerPath


class Command(BaseCommand):
    help = 'Seed initial skills and career paths'

    def handle(self, *args, **options):
        skills = [
            ('Python', 'Programming'),
            ('Django', 'Web'),
            ('JavaScript', 'Programming'),
            ('SQL', 'Data'),
            ('Machine Learning', 'AI'),
            ('Communication', 'Soft'),
            ('Cloud', 'DevOps'),
        ]

        skill_objs = {}
        for name, category in skills:
            obj, _ = Skill.objects.get_or_create(name=name, defaults={'category': category})
            skill_objs[name] = obj

        self.stdout.write(self.style.SUCCESS(f'Seeded {len(skill_objs)} skills'))

        roles = [
            ('Backend Developer', 'Build and maintain server-side logic', ['Python', 'Django', 'SQL', 'Cloud']),
            ('Fullstack Developer', 'End-to-end web applications', ['Python', 'Django', 'JavaScript', 'SQL']),
            ('Data Scientist', 'Analyze data and build models', ['Python', 'Machine Learning', 'SQL']),
            ('DevOps Engineer', 'CI/CD and infrastructure', ['Cloud', 'Python', 'Communication']),
        ]

        for title, desc, reqs in roles:
            cp, _ = CareerPath.objects.get_or_create(title=title, defaults={'description': desc})
            cp.required_skills.set([skill_objs[r] for r in reqs])

        self.stdout.write(self.style.SUCCESS('Seeded career paths'))


