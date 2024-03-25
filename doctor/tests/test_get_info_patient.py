from random import randint
from unittest import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from doctor.functions.functions import add_features
from nutritionist.models import CustomUser


class GetInfoPatientAPIViewTestCase(TestCase):
    def setUp(self):
        self.patient = CustomUser.objects.create(
            username='test_patient_',
            full_name="test patient",
            type_of_diet="ОВД",
            comment="Test Comment",
            is_probe=False,
            is_without_salt=False,
            is_without_lactose=False,
            is_pureed_nutrition=False,
        )
        self.url = reverse('get_info_patient_api')

    def test_get_info_patient_api_view(self):
        client = APIClient()
        response = client.get(self.url, {"user_id": self.patient.id})

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.data["full_name"], "test patient")
        self.assertEqual(response.data["type_of_diet"], "ОВД")
        self.assertEqual(response.data["comment"], "Test Comment")

        response = client.get(self.url, {"user_id": ''})
        self.assertEqual(response.status_code, 200)
        with self.assertRaises(KeyError):
            try_get = response.data["full_name"]

class TestAddFeatures(TestCase):
    # здесь опять круговой импорт!!
    def test_no_features(self):
        comment = "Some comment"
        result = add_features(comment, False, False, False, False)
        self.assertEqual(result, "Some comment")

    def test_with_probe(self):
        comment = "Some comment"
        result = add_features(comment, True, False, False, False)
        self.assertEqual(result, "Some comment Питание через зонд.")
