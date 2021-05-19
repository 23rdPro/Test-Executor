from django.test import TestCase


def fizzbuzz_val(val):
    return ['Fizz' * (not i % 3) + 'Buzz' * (not i % 5) or i for i in range(1, val + 1)][-1]


class TestFizzBuzz(TestCase):
    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_multiples_of_3_and_5(self):
        self.assertEqual(fizzbuzz_val(15), 'FizzBuzz')

    def test_multiples_of_3_alone(self):
        self.assertTrue(fizzbuzz_val(3) is 'Fizz')
        self.assertTrue(fizzbuzz_val(99) is 'Fizz')
        self.assertFalse(fizzbuzz_val(15) is 'Fizz')
        self.assertFalse(fizzbuzz_val(8) is 'Fizz')

    def test_multiples_of_5_alone(self):
        self.assertTrue(fizzbuzz_val(5) is 'Buzz')
        self.assertTrue(fizzbuzz_val(10) is 'Buzz')
        self.assertTrue(fizzbuzz_val(20) is 'Buzz')
        self.assertFalse(fizzbuzz_val(8) is 'Buzz')

    def test_others(self):
        self.assertIsInstance(fizzbuzz_val(1), int)
        self.assertIsInstance(fizzbuzz_val(8), int)
