from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import User


class AccountsModelAndApiTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testtraveller',
            email='traveller@example.com',
            password='testPassword123!',
            first_name='Chioma',
            last_name='Adeleke',
            bio='Lover of road trips in Nigeria.',
        )

    def test_user_creation_and_methods(self):
        self.assertEqual(self.user.get_display_name(), 'Chioma Adeleke')
        self.assertTrue('images.unsplash.com' in self.user.get_avatar_url())

    def test_signup_api(self):
        response = self.client.post('/api/auth/signup/', {
            'name': 'Emeka Obi',
            'email': 'emeka@example.com',
            'password': 'emekaPassword123!',
            'confirm_password': 'emekaPassword123!',
            'bio': 'Calabar and Enugu explorer.',
        })
        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.objects.filter(email='emeka@example.com').exists())

    def test_signin_and_signout_api(self):
        # Sign in with correct password
        response = self.client.post('/api/auth/signin/', {
            'email': 'traveller@example.com',
            'password': 'testPassword123!',
        }, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['user']['email'], 'traveller@example.com')

        # Check me endpoint
        me_resp = self.client.get('/api/auth/me/')
        self.assertEqual(me_resp.status_code, 200)
        self.assertTrue(me_resp.data['authenticated'])
        self.assertEqual(me_resp.data['user']['name'], 'Chioma Adeleke')

        # Sign out
        signout_resp = self.client.post('/api/auth/signout/')
        self.assertEqual(signout_resp.status_code, 200)

        # Check me endpoint after logout
        me_after = self.client.get('/api/auth/me/')
        self.assertFalse(me_after.data['authenticated'])

    def test_signin_invalid_credentials(self):
        response = self.client.post('/api/auth/signin/', {
            'email': 'traveller@example.com',
            'password': 'wrongPassword',
        }, content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_profile_update(self):
        self.client.force_login(self.user)
        response = self.client.patch('/api/auth/profile/', {
            'name': 'Chioma Adeleke-Bello',
            'bio': 'Updated bio description',
        }, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.get_display_name(), 'Chioma Adeleke-Bello')
        self.assertEqual(self.user.bio, 'Updated bio description')

    def test_forgot_password(self):
        response = self.client.post('/api/auth/forgot-password/', {
            'email': 'traveller@example.com',
        }, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.data)
