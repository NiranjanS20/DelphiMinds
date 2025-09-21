from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model


class AuthFlowTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register_and_login(self):
        r = self.client.post('/auth/register', {
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'Str0ngP@ss!',
            'role': 'student',
        }, format='json')
        self.assertEqual(r.status_code, 201)

        r = self.client.post('/auth/login', {
            'username': 'alice',
            'password': 'Str0ngP@ss!'
        }, format='json')
        self.assertEqual(r.status_code, 200)
        self.assertIn('access', r.data)
        self.assertIn('refresh', r.data)

# Create your tests here.
