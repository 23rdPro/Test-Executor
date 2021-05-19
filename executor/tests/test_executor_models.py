from django.db import IntegrityError
from django.test import TestCase

from executor.models import Executor, File
from users.tests.factories import UserFactory


class FileModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        File.objects.create(file='foo.py', )

    def test_label(self):
        file = File.objects.get(file='foo.py')
        file_label = file._meta.get_field('file').verbose_name

        with self.assertRaises(IntegrityError):
            File.objects.create(file='foo.py')
        self.assertEqual(file_label, 'file')
        self.assertEqual(str(file), file.file)

    def test_field_max_length(self):
        file = File.objects.get(file='foo.py')  # unique field
        file_length = file._meta.get_field('file').max_length
        self.assertEqual(file_length, 64)


class ExecutorModelTest(TestCase):
    def setUp(self) -> None:
        self.file1 = File.objects.create(
            file='test_foo.py',
        )
        self.file2 = File.objects.create(
            file='test_bar.py',
        )
        tester = UserFactory()
        self.exec1 = Executor.objects.create(tester=tester, environment_id=10)
        self.exec2 = Executor.objects.create(tester=tester, environment_id=2)

        self.exec1.file.add(self.file2)
        self.exec1.file.add(self.file1)

        self.exec2.file.add(self.file2)

        self.files = [g.file for g in self.exec1.file.all()]
        self.str = str(self.exec1)

    def test_create_objects(self):
        e = Executor.objects.all().count()
        self.assertEqual(e, 2)
        with self.assertRaises(IntegrityError):
            Executor.objects.create(environment_id=10)
        self.assertIn('test_bar.py', self.files)
        self.assertIn('test_foo.py', self.files)
        self.assertEqual(self.str, ', '.join(self.files))
