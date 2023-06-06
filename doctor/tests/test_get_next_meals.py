from datetime import time
from unittest.mock import patch

from django.test import TestCase

from doctor.functions.diet_formation import get_next_meals


class GetNextMealsTestCase(TestCase):
    @patch('doctor.functions.diet_formation.datetime')
    def test_breakfast(self, datetime_mock):
        time_mock = time(8, 30)
        datetime_mock.today.return_value.time.return_value = time_mock
        result = get_next_meals()
        self.assertEqual(result, ['breakfast', 'lunch', 'afternoon', 'dinner'])

    @patch('doctor.functions.diet_formation.datetime')
    def test_lunch_1(self, datetime_mock):
        time_mock = time(8, 31)
        datetime_mock.today.return_value.time.return_value = time_mock
        result = get_next_meals()
        self.assertEqual(result, ['lunch', 'afternoon', 'dinner'])

    @patch('doctor.functions.diet_formation.datetime')
    def test_lunch_2(self, datetime_mock):
        time_mock = time(12, 00)
        datetime_mock.today.return_value.time.return_value = time_mock
        result = get_next_meals()
        self.assertEqual(result, ['lunch', 'afternoon', 'dinner'])

    @patch('doctor.functions.diet_formation.datetime')
    def test_afternoon_1(self, datetime_mock):
        time_mock = time(12, 2)
        datetime_mock.today.return_value.time.return_value = time_mock
        result = get_next_meals()
        self.assertEqual(result, ['afternoon', 'dinner'])

    @patch('doctor.functions.diet_formation.datetime')
    def test_afternoon_2(self, datetime_mock):
        time_mock = time(15, 30)
        datetime_mock.today.return_value.time.return_value = time_mock
        result = get_next_meals()
        self.assertEqual(result, ['afternoon', 'dinner'])

    @patch('doctor.functions.diet_formation.datetime')
    def test_dinner_1(self, datetime_mock):
        time_mock = time(15, 31)
        datetime_mock.today.return_value.time.return_value = time_mock
        result = get_next_meals()
        self.assertEqual(result, ['dinner'])

    @patch('doctor.functions.diet_formation.datetime')
    def test_dinner_2(self, datetime_mock):
        time_mock = time(19, 0)
        datetime_mock.today.return_value.time.return_value = time_mock
        result = get_next_meals()
        self.assertEqual(result, ['dinner'])

    @patch('doctor.functions.diet_formation.datetime')
    def test_tomorrow(self, datetime_mock):
        time_mock = time(19, 1)
        datetime_mock.today.return_value.time.return_value = time_mock
        result = get_next_meals()
        self.assertEqual(result, [])
