from django.test import TestCase, Client

from executor.forms import ExecutorForm
from executor.models import File
from users.models import User


class ExecutorFormTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.u1 = User.objects.create_user(
            username='user-form1',
            password='password23'
        )
        self.u2 = User.objects.create_user(
            username='user-form2',
            password='password23'
        )
        self.f1 = File.objects.create(
            file='file-form1.py',
        )
        self.f2 = File.objects.create(
            file='file-form2.py',
        )
        self.f3 = File.objects.create(
            file='file-form3.py'
        )

        self.form_data1 = {'tester': self.u1, 'file': [f for f in File.objects.all()],
                           'environment_id': 101}
        self.form_data3 = {'tester': self.u1, 'file': [f for f in File.objects.all()],
                           'environment_id': 100}
        self.form_data2 = {'tester': self.u2, 'file': [f for f in File.objects.all()],
                           'environment_id': 23}

    def test_form_fields(self):
        # self.client.get(reverse('home'))
        # self.client.login(username=self.u1.username, password='password23')
        form1 = ExecutorForm(user=self.u1, data=self.form_data1)
        form2 = ExecutorForm(user=self.u1, data=self.form_data3)
        form3 = ExecutorForm(user=self.u2, data=self.form_data2)

        self.assertListEqual([True for _ in range(2)], list(i.is_valid() for i in [form2, form3]))
        self.assertFalse(form1.is_valid())
        self.assertTrue(form2.is_valid())
        self.assertTrue(form3.is_valid())
        self.assertEqual(User.objects.all().count(), 2)
        self.assertEqual(File.objects.all().count(), 3)  # 3
        with self.assertRaises(AssertionError):
            assert form1.is_valid()
