from datetime import time
from unittest.mock import patch

from django.test import TestCase

from doctor.functions.bot import check_change


class CheckChangeTestCase(TestCase):
    @patch('doctor.functions.bot.datetime')
    def test_breakfast(self, datetime_mock):
        time_mock = time(8, 30)
        datetime_mock.today.return_value.time.return_value = time_mock
        result = check_change('True')
        self.assertEqual(result, ('завтрака', 0))

    @patch('doctor.functions.bot.datetime')
    def test_lunch_1(self, datetime_mock):
        time_mock = time(8, 31)
        datetime_mock.today.return_value.time.return_value = time_mock
        result = check_change('True')
        self.assertEqual(result, ('обеда', 1))

    @patch('doctor.functions.bot.datetime')
    def test_lunch_2(self, datetime_mock):
        time_mock = time(12, 00)
        datetime_mock.today.return_value.time.return_value = time_mock
        result = check_change('True')
        self.assertEqual(result, ('обеда', 1))

    @patch('doctor.functions.bot.datetime')
    def test_afternoon_1(self, datetime_mock):
        time_mock = time(12, 1)
        datetime_mock.today.return_value.time.return_value = time_mock
        result = check_change('True')
        self.assertEqual(result, ('полдника', 2))

    @patch('doctor.functions.bot.datetime')
    def test_afternoon_2(self, datetime_mock):
        time_mock = time(15, 30)
        datetime_mock.today.return_value.time.return_value = time_mock
        result = check_change('True')
        self.assertEqual(result, ('полдника', 2))
    @patch('doctor.functions.bot.datetime')
    def test_dinner_1(self, datetime_mock):
        time_mock = time(15, 31)
        datetime_mock.today.return_value.time.return_value = time_mock
        result = check_change('True')
        self.assertEqual(result, ('ужина', 3))

    @patch('doctor.functions.bot.datetime')
    def test_dinner_2(self, datetime_mock):
        time_mock = time(18, 0)
        datetime_mock.today.return_value.time.return_value = time_mock
        result = check_change('True')
        self.assertEqual(result, ('ужина', 3))

    @patch('doctor.functions.bot.datetime')
    def test_tomorrow(self, datetime_mock):
        time_mock = time(18, 1)
        datetime_mock.today.return_value.time.return_value = time_mock
        result = check_change('True')
        self.assertEqual(result, ('завтра', 4))

    @patch('doctor.functions.bot.datetime')
    def test_no_flag(self, datetime_mock):
        time_mock = time(18, 1)
        datetime_mock.today.return_value.time.return_value = time_mock
        result = check_change('False')
        self.assertEqual(result, 'завтра')