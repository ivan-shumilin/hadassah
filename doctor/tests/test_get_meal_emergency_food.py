from datetime import time, date
from unittest.mock import patch

from django.test import TestCase

from doctor.functions.diet_formation import get_meal_emergency_food


class GetMealEmergencyFoodTestCase(TestCase):
    @patch('doctor.functions.diet_formation.datetime')
    def test_no(self, datetime_mock):
        time_mock = time(8, 29)
        datetime_mock.today.return_value.time.return_value = time_mock
        patient_receipt_date = date.today()
        patient_receipt_time = time(8, 31)
        result = get_meal_emergency_food(patient_receipt_date, patient_receipt_time)
        self.assertEqual(result, False)

    @patch('doctor.functions.diet_formation.datetime')
    def test_breakfast(self, datetime_mock):
        time_mock = time(8, 31)
        datetime_mock.today.return_value.time.return_value = time_mock
        patient_receipt_date = date.today()
        patient_receipt_time = time(8, 31)
        result = get_meal_emergency_food(patient_receipt_date, patient_receipt_time)
        self.assertEqual(result, 'breakfast')

    @patch('doctor.functions.diet_formation.datetime')
    def test_breakfast_1(self, datetime_mock):
        time_mock = time(10, 00)
        datetime_mock.today.return_value.time.return_value = time_mock
        patient_receipt_date = date.today()
        patient_receipt_time = time(10, 00)
        result = get_meal_emergency_food(patient_receipt_date, patient_receipt_time)
        self.assertEqual(result, 'breakfast')

    @patch('doctor.functions.diet_formation.datetime')
    def test_breakfast_2(self, datetime_mock):
        time_mock = time(9, 59)
        datetime_mock.today.return_value.time.return_value = time_mock
        patient_receipt_date = date.today()
        patient_receipt_time = time(9, 59)
        result = get_meal_emergency_food(patient_receipt_date, patient_receipt_time)
        self.assertEqual(result, 'breakfast')

    @patch('doctor.functions.diet_formation.datetime')
    def test_lunch_1(self, datetime_mock):
        time_mock = time(12, 00)
        datetime_mock.today.return_value.time.return_value = time_mock
        patient_receipt_date = date.today()
        patient_receipt_time = time(12, 1)
        result = get_meal_emergency_food(patient_receipt_date, patient_receipt_time)
        self.assertEqual(result, 'lunch')


    @patch('doctor.functions.diet_formation.datetime')
    def test_lunch_2(self, datetime_mock):
        time_mock = time(14, 00)
        datetime_mock.today.return_value.time.return_value = time_mock
        patient_receipt_date = date.today()
        patient_receipt_time = time(12, 1)
        result = get_meal_emergency_food(patient_receipt_date, patient_receipt_time)
        self.assertEqual(result, 'lunch')

    @patch('doctor.functions.diet_formation.datetime')
    def test_lunch_2_no(self, datetime_mock):
        time_mock = time(14, 00)
        datetime_mock.today.return_value.time.return_value = time_mock
        patient_receipt_date = date.today()
        patient_receipt_time = time(14, 1)
        result = get_meal_emergency_food(patient_receipt_date, patient_receipt_time)
        self.assertEqual(result, False)

    @patch('doctor.functions.diet_formation.datetime')
    def test_afternoon_1(self, datetime_mock):
        time_mock = time(15, 30)
        datetime_mock.today.return_value.time.return_value = time_mock
        patient_receipt_date = date.today()
        patient_receipt_time = time(15, 31)
        result = get_meal_emergency_food(patient_receipt_date, patient_receipt_time)
        self.assertEqual(result, 'afternoon')


    @patch('doctor.functions.diet_formation.datetime')
    def test_afternoon_2(self, datetime_mock):
        time_mock = time(16, 30)
        datetime_mock.today.return_value.time.return_value = time_mock
        patient_receipt_date = date.today()
        patient_receipt_time = time(16, 21)
        result = get_meal_emergency_food(patient_receipt_date, patient_receipt_time)
        self.assertEqual(result, 'afternoon')


    @patch('doctor.functions.diet_formation.datetime')
    def test_afternoon_2_no(self, datetime_mock):
        time_mock = time(16, 30)
        datetime_mock.today.return_value.time.return_value = time_mock
        patient_receipt_date = date.today()
        patient_receipt_time = time(16, 31)
        result = get_meal_emergency_food(patient_receipt_date, patient_receipt_time)
        self.assertEqual(result, False)

    # @patch('doctor.functions.diet_formation.datetime')
    # def test_lunch_2(self, datetime_mock):
    #     time_mock = time(12, 00)
    #     datetime_mock.today.return_value.time.return_value = time_mock
    #     result = get_next_meals()
    #     self.assertEqual(result, ['lunch', 'afternoon', 'dinner'])
    #
    # @patch('doctor.functions.diet_formation.datetime')
    # def test_afternoon_1(self, datetime_mock):
    #     time_mock = time(12, 2)
    #     datetime_mock.today.return_value.time.return_value = time_mock
    #     result = get_next_meals()
    #     self.assertEqual(result, ['afternoon', 'dinner'])
    #
    # @patch('doctor.functions.diet_formation.datetime')
    # def test_afternoon_2(self, datetime_mock):
    #     time_mock = time(15, 30)
    #     datetime_mock.today.return_value.time.return_value = time_mock
    #     result = get_next_meals()
    #     self.assertEqual(result, ['afternoon', 'dinner'])
    #
    # @patch('doctor.functions.diet_formation.datetime')
    # def test_dinner_1(self, datetime_mock):
    #     time_mock = time(15, 31)
    #     datetime_mock.today.return_value.time.return_value = time_mock
    #     result = get_next_meals()
    #     self.assertEqual(result, ['dinner'])
    #
    # @patch('doctor.functions.diet_formation.datetime')
    # def test_dinner_2(self, datetime_mock):
    #     time_mock = time(19, 0)
    #     datetime_mock.today.return_value.time.return_value = time_mock
    #     result = get_next_meals()
    #     self.assertEqual(result, ['dinner'])
    #
    # @patch('doctor.functions.diet_formation.datetime')
    # def test_tomorrow(self, datetime_mock):
    #     time_mock = time(19, 1)
    #     datetime_mock.today.return_value.time.return_value = time_mock
    #     result = get_next_meals()
    #     self.assertEqual(result, [])
