from django.test import TestCase, Client
from rest_framework.test import APIRequestFactory
from rest_framework import status
from rest_framework.utils.serializer_helpers import ReturnDict

from executor.models import Executor, File
from executor.serializers import ExecutorSerializer, FileSerializer, TaskSerializer
from executor.tests.factories import FileFactory
from users.serializers import UserSerializer
from users.tests.factories import UserFactory


class ExecutorAPITest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.f1 = FileFactory()
        self.f2 = FileFactory()
        self.tester = UserFactory()
        self.executor = Executor.objects.create(
            environment_id=86,
            tester=self.tester,
        )
        self.executor.file.add(self.f1)
        self.executor.file.add(self.f2)
        self.factory = APIRequestFactory()
        self.executor2 = Executor.objects.create(environment_id=37, tester=self.tester)
        self.executor2.file.add(self.f2)

    def test_executor_api(self):
        executors = Executor.objects.all()
        request = self.factory.get('/')
        request.user = self.tester

        serializer = ExecutorSerializer(executors, many=True, context={'request': request})
        response = self.client.get('/api/executors/')
        self.assertEqual(response.data['results'], serializer.data)
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(response.data['next'], response.data['previous'])  # no pagination yet
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        executor = Executor.objects.get(id=self.executor2.id)
        serializer = ExecutorSerializer(executor, context={'request': request})
        self.assertIn(serializer.data, response.data['results'])

        self.client.login(username=self.tester.username, password='password')
        ctx_user = {'request': APIRequestFactory().get('/api/users/')}
        ctx_file = {'request': APIRequestFactory().get('/api/files/')}
        user_serializer = UserSerializer(self.tester, context=ctx_user)
        file_serializer = FileSerializer(File.objects.all(), many=True, context=ctx_file)
        response = self.client.post('/api/executors/', data={
            'tester': user_serializer.data['url'],
            'environment_id': 58,
            'file': [f['url'] for f in file_serializer.data]
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_task_serializer(self):
        e = Executor.objects.last()
        serializer = TaskSerializer(e)
        self.assertTrue(serializer.data['file'])
        self.assertTrue(serializer.data['test_log'])
        self.assertTrue(serializer.data['test_status'])
        self.assertEqual(type(serializer.data['file'] and serializer.data['test_log'] and
                              serializer.data['test_status']), str)
        self.assertEqual(type(serializer.data), ReturnDict)  # rest_framework
        self.assertEqual(type(serializer.data['created_at']), str)
        self.assertEqual(type(serializer.data['environment_id']), int)
        self.assertEqual(len(serializer.data), 7)  # nos of table columns for result
