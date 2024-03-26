from unittest import TestCase, mock
from unittest.mock import patch, MagicMock

from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from hadassah import settings


class TestSendPatientProductsAPIView(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = "/doctor/api/v1/send-patient-products"

        self.data = {
            "id_user": 1,
            "date_show": "2024-03-01",
            "products": "product1&?&product2",
            "meal": "breakfast",
            "user_name": "Anonymizes",
            "comment": "Test comment",
        }

    @patch("doctor.views.my_job_send_messang_changes.delay")
    @patch("doctor.views.CustomUser.objects.get")
    def test_send_patient_products(self, mock_custom_user_get, mock_send_message):

        mock_patient = MagicMock()
        mock_patient.full_name = "Тестов Тест Тестович"
        mock_patient.room_number = "2f-1"
        mock_patient.type_of_diet = "ОВД"
        mock_custom_user_get.return_value = mock_patient

        response = self.client.post(self.url, data=self.data, format="json")

        full_name = "Тестов Т.Т."
        room_number = ', ' + mock_patient.room_number
        meal = "завтрак"
        comment = self.data["comment"]
        products = self.data["products"]
        user_name = self.data["user_name"]

        messange = f"<b>Корректировка для экстренной госпитализации:</b>\n"
        messange += f"   \n"
        messange += f"{full_name}{room_number}\n"
        messange += f"{mock_patient.type_of_diet}, {meal}\n"
        messange += f"Комментарий: {comment}\n" if comment != "" else ""
        messange += f"   \n"
        for product_name in products.strip("&?&").split("&?&"):
            messange += f"– {product_name}\n"

        messange += f"({user_name})"

        self.assertEqual(response.status_code, 200)
        mock_send_message.assert_called_once_with(
            messange, settings.BOT_ID_EMERGEBCY_FOOD,
        )
