from django.test import TestCase, Client
from django.urls import reverse

from test_executor.settings import env
from users.models import User

from .factories import UserFactory


class TestUser(TestCase):
    def setUp(self) -> None:
        self.username = 'test-user'
        self.user = UserFactory()
        self.client = Client()

    def tearDown(self) -> None:
        pass

    @classmethod
    def setUpTestData(cls):
        for user_id in range(1, 3):
            user = User.objects.create_user(username='user0%d' % user_id)
            user.set_password('passsekret43')
            user.save()

    def test_login(self):
        response = self.client.get(reverse('login'))  # view -> return render(template, context)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        with self.assertRaises(AttributeError):
            self.assertTrue(response.url)  # Template response objects don't have url obj

        response = self.client.login(username='user01', password='passsekret43')
        self.assertTrue(response)
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'executor.html')
        with self.assertRaises(AttributeError):
            assert self.assertTrue(response.url)  # no response.url, template response

    def test_signup_view(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')

        response = self.client.post(reverse('signup'), data={
            'username': self.username,
            'password1': 'passsekret43',
            'password2': 'passsekret43'
        })
        self.assertEqual(response.status_code, 302)  # redirect after signup
        self.assertEqual(response.url, '/')  # redirect to home
        self.assertEqual(User.objects.all().count(), 4)

    def test_login_required_url_follow(self):
        response = self.client.get(reverse('home'), follow=True)

        self.assertRedirects(response, '/login/?next=/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

