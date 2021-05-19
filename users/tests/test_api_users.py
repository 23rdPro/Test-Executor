from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory, APIClient, RequestsClient, APITestCase, force_authenticate
from rest_framework import status

from users.models import User
from users.serializers import UserSerializer
from users.tests.factories import UserFactory
from users.views import UserViewSet


class TestUserAPI(APITestCase):
    def setUp(self) -> None:
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.request = RequestsClient()
        self.user = UserFactory()
        self.admin_user = User.objects.create_superuser(username='admin01')
        self.admin_user.set_password('sekret55@pass')
        self.token = Token.objects.create(user=self.admin_user)

    def test_user_auth(self):  # authentication & authorization
        response = self.client.logout()
        self.assertIsNone(response)
        self.assertNotEqual(self.client.get('/').status_code, 200)  # 302, not logged in

        response = self.client.login(username=self.user.username, password='password')
        self.assertIsNotNone(response)
        self.assertEqual(response, True)
        self.assertEqual(self.client.get('/').status_code, 200)

        request = self.request.get('http://localhost:8000/')  # production
        assert request.status_code == 200

    def test_user_api_create(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.token))
        response = self.client.post('/api/users/', data={
            'username': 'justin',
            'password': 'pass-code',
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        request = self.factory.get('/api/users/')
        users = User.objects.all()
        serializer = UserSerializer(users, many=True, context={'request': request})
        self.assertEqual(User.objects.all().count(), len(serializer.data))
        self.assertListEqual([u.username for u in User.objects.all()], [u['username'] for u in serializer.data])
