import unittest
from django.urls import reverse
from rest_framework.test import APIClient

from doctor.functions.helpers import formatting_full_name_mode_full
from nutritionist.models import CustomUser


class TestCheckIsHavePatientAPIView(unittest.TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('check-is-have-patient')

    def test_check_patient_exist(self):
        # Создаем тестового пациента
        patient = CustomUser.objects.create(full_name="John Doe", status="patient")

        response = self.client.get(self.url, {'full_name': 'John Doe'})
        self.assertEqual(response.status_code, 200)  # Проверяем успешный статус ответа
        self.assertEqual(response.json()['status'], 'patient')  # Проверяем статус пациента

    def test_check_patient_not_exist(self):
        # Отправляем GET-запрос для проверки несуществующего пациента
        response = self.client.get(self.url, {'full_name': 'Jane Doe'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'None')


class TestFormattingFullName(unittest.TestCase):
    def test_formatting_full_name_mode_full(self):
        self.assertEqual(formatting_full_name_mode_full("ivan ivanov ivanovich"), "Ivan Ivanov Ivanovich")
        self.assertEqual(formatting_full_name_mode_full("  klim klimovich "), "Klim Klimovich")
        self.assertEqual(formatting_full_name_mode_full("JOHN SMITH"), "John Smith")
        self.assertEqual(formatting_full_name_mode_full("mike jones"), "Mike Jones")
        self.assertEqual(formatting_full_name_mode_full("alisa ageeva"), "Alisa Ageeva")

if __name__ == '__main__':
    unittest.main()
