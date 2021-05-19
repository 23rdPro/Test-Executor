from django.urls import reverse
from executor.models import Executor, File
from django.test import TestCase, Client

from users.models import User
from users.tests.factories import UserFactory
from .factories import FileFactory
from django_capture_on_commit_callbacks import capture_on_commit_callbacks


class TestExecuteTaskView(TestCase):

    def setUp(self) -> None:
        self.user = UserFactory()
        self.client = Client()
        self.user1 = User.objects.create(username='test-redirect')
        self.user1.set_password('sekret55@pass')
        self.user1.save()
        self.file3 = FileFactory()
        self.file4 = FileFactory()
        self.file1 = File.objects.create(file='foo.py')
        self.file2 = File.objects.create(file='bar.py')
        self.files = [file for file in File.objects.all()]

    def test_login_required(self):
        # before login
        home = self.client.get('/')
        result = self.client.get(reverse('result'))

        self.assertEqual(result.url, "/login/?next=/result/")
        self.assertTrue(home.url)
        self.assertEqual(home.url, "/login/?next=/")
        self.assertEqual(User.objects.all().count(), 2)
        self.assertEqual(home.status_code, result.status_code)  # 302
        with self.assertRaises(AssertionError):
            self.assertTemplateUsed(home, 'executor.html')

        # after login
        self.client.login(username='test-redirect', password='sekret55@pass')
        home = self.client.get('/')
        result = self.client.get('/result/')
        user = User.objects.get(username='test-redirect')
        self.assertTemplateUsed(home, 'executor.html')
        self.assertEqual(home.status_code, result.status_code)  # consequent 200 following login
        self.assertTrue(home.context['form'])
        self.assertTrue(result.context['user'])
        self.assertEqual(result.context['user'], user)
        self.assertTrue(home.context['form']['file'].name)
        self.assertEqual(home.context['form']['file'].name, 'file')

    def test_task_on_commit(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)  # redirect to login page
        self.assertEqual(response.url, "/login/?next=/")

        # after login
        response = self.client.login(username='test-redirect', password='sekret55@pass')
        assert response  # response == True
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'executor.html')

        # post executor without on_commit test
        response = self.client.post('/', {
            'tester': 2,    # logged in user id
            'environment_id': 3,
            'file': [i for i in range(1, 4)]  # all four files
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/result/')

        # response = self.client.get('/')

        with capture_on_commit_callbacks(execute=True) as call_back:
            response = self.client.post('/', {
                'tester': 2,    # logged in user id
                'environment_id': 34,
                'file': [i for i in range(1, 3)]
            })

        self.assertEqual(Executor.objects.all().count(), 2)
        self.assertEqual(len(call_back), 1)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/result/')

# class TestCeleryTask(SimpleTestCase):
#     allow_database_queries = True
#
#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#         cls.celery_worker = start_worker(app=app, perform_ping_check=False)
#         cls.celery_worker.__enter__()
#
#     @classmethod
#     def tearDownClass(cls):
#         super().tearDownClass()
#         cls.celery_worker.__exit__(None, None, None)
#
#     def test_success(self):
#         tasks.execute_test_from.delay(['foo', 'bar'])
