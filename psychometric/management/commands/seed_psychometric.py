from django.core.management.base import BaseCommand
from psychometric.models import PsychometricTest, Question


class Command(BaseCommand):
    help = 'Seed psychometric test data'

    def handle(self, *args, **options):
        # Create Career Readiness Test
        test, created = PsychometricTest.objects.get_or_create(
            name='Career Readiness Assessment',
            defaults={
                'description': 'Comprehensive assessment to evaluate your career readiness, personality traits, and ideal career paths.',
                'category': 'career_readiness',
                'is_active': True
            }
        )

        if created:
            self.stdout.write(f'Created test: {test.name}')
        else:
            self.stdout.write(f'Test already exists: {test.name}')

        # Create questions for the test
        questions_data = [
            {
                'text': 'I prefer working independently rather than in a team.',
                'question_type': 'scale',
                'order': 1
            },
            {
                'text': 'I enjoy solving complex problems and puzzles.',
                'question_type': 'scale',
                'order': 2
            },
            {
                'text': 'I am comfortable speaking in front of large groups.',
                'question_type': 'scale',
                'order': 3
            },
            {
                'text': 'I prefer structured, routine work over creative, open-ended tasks.',
                'question_type': 'scale',
                'order': 4
            },
            {
                'text': 'I enjoy learning new technologies and tools.',
                'question_type': 'scale',
                'order': 5
            },
            {
                'text': 'I work best under pressure and tight deadlines.',
                'question_type': 'scale',
                'order': 6
            },
            {
                'text': 'I prefer to lead projects rather than follow instructions.',
                'question_type': 'scale',
                'order': 7
            },
            {
                'text': 'I enjoy working with data and numbers.',
                'question_type': 'scale',
                'order': 8
            },
            {
                'text': 'I am interested in helping others and making a positive impact.',
                'question_type': 'scale',
                'order': 9
            },
            {
                'text': 'I prefer working with people over working with machines.',
                'question_type': 'scale',
                'order': 10
            },
            {
                'text': 'What is your ideal work environment?',
                'question_type': 'multiple_choice',
                'options': ['Office', 'Remote', 'Hybrid', 'Field work'],
                'order': 11
            },
            {
                'text': 'What motivates you most in your career?',
                'question_type': 'multiple_choice',
                'options': ['Financial success', 'Work-life balance', 'Making a difference', 'Learning and growth'],
                'order': 12
            },
            {
                'text': 'Describe your ideal career in 2-3 sentences.',
                'question_type': 'text',
                'order': 13
            }
        ]

        for question_data in questions_data:
            question, created = Question.objects.get_or_create(
                test=test,
                text=question_data['text'],
                defaults=question_data
            )
            if created:
                self.stdout.write(f'Created question: {question.text[:50]}...')
            else:
                self.stdout.write(f'Question already exists: {question.text[:50]}...')

        self.stdout.write(self.style.SUCCESS('Successfully seeded psychometric test data'))
