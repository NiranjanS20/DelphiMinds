from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from .models import Skill


class SkillEndpointsTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        User = get_user_model()
        self.user = User.objects.create_user(username='bob', password='Str0ngP@ss!')
        self.client.force_authenticate(self.user)
        self.skill = Skill.objects.create(name='Python', category='Programming')

    def test_list_skills_and_add_user_skill(self):
        r = self.client.get('/skills/')
        self.assertEqual(r.status_code, 200)
        self.assertGreaterEqual(len(r.data), 1)

        r = self.client.post('/skills/my/', { 'skill_id': self.skill.id, 'level': 60 }, format='json')
        self.assertEqual(r.status_code, 201)

# Create your tests here.
