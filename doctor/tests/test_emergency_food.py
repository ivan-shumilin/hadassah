import unittest
from datetime import time, datetime, date
from unittest.mock import patch, MagicMock, Mock, call
from django.test import Client
from django.urls import reverse
from freezegun import freeze_time
from rest_framework.test import APIClient

from hadassah import settings
from nutritionist.models import CustomUser


class TestSendEmergencyFoodAPIView(unittest.TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = "/doctor/api/v1/send_emergency_food"
        self.data = {"data": "1&завтрака&no_working_hours", "user_name": "test doctor"}

    @freeze_time("2024-03-31 08:00:00")
    @patch("doctor.views.CustomUser.objects.get")
    @patch("doctor.views.my_job_send_messang_changes.delay")
    @patch("doctor.views.Report")
    def test_send_emergency_food(
        self,
        mock_report,
        mock_message_delay,
        mock_custom_user_get,
    ):

        # mock_custom_user_get.return_value = mock_patient

        mock_patient = MagicMock(name='mymock')
        mock_patient.full_name = "Тестов Тест Тестович"
        mock_patient.room_number = "2f-1"
        mock_patient.type_of_diet = "ОВД"

        mock_patient.comment = "Test comment"
        mock_patient.is_probe = True
        mock_patient.is_without_salt = False
        mock_patient.is_without_lactose = False
        mock_patient.is_pureed_nutrition = True

        mock_custom_user_get.return_value = mock_patient

        # time_mock = time(8, 30)
        # mock_datetime.today.time.return_value = time_mock
        # print("Test time:", mock_datetime.today.time.return_value.hour)
        # print(datetime)

        mock_report_instance = mock_report.return_value
        mock_report_instance.save.return_value = True

        response = self.client.post(self.url, data=self.data, format='json')

        self.assertEqual(response.status_code, 200)

        self.assertEqual(mock_message_delay.call_count, 2)

        # expected_message = (
        #     "<b>Доп. питание для экстренной госпитализации:</b>\n"
        #     "    \nTest Patient, 101\nstandard, завтрак\n"
        #     "    \n– Test Product\n(test doctor)"
        # )
        expected_message1 = '&#8505; <b>Изменение с завтрака</b>\nЭкстренное питание для Тестов Т.Т. ОВД\n(Test D.)'

        expected_message2 = ('<b>Доп. питание для экстренной госпитализации:</b>\n'
                             '    \nТестов Т.Т., 2f-1\nОВД\nКомментарий:'
                             ' Test comment Питание через зонд. Протертое питание.\n'
                             '    \n– Nutrien Sugarless 200 мл\n(Test D.)')

        mock_message_delay.assert_has_calls([
            call(expected_message2, settings.BOT_ID_EMERGEBCY_FOOD),
            call(expected_message1),
        ])

        expected_user_id = mock_patient
        expected_date_create = date(2024, 3, 31)
        expected_meal = "breakfast"
        expected_product_id = 569
        expected_type_of_diet = "ОВД"
        expected_type = "emergency-night"

        mock_report.assert_called_once_with(
            user_id=expected_user_id,
            date_create=expected_date_create,
            meal=expected_meal,
            product_id=expected_product_id,
            type_of_diet=expected_type_of_diet,
            type=expected_type
        )

        # Проверка создания объектов отчета
        # mock_product_lp_get.assert_called_once_with(id=569)


if __name__ == "__main__":
    unittest.main()
