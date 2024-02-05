import unittest
from datetime import date, datetime
from unittest.mock import patch

from django.test import RequestFactory

from doctor.functions.functions import archiving_user
from nutritionist.models import CustomUser


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.factory = RequestFactory()

        self.data = {
            "username": "qwld[kf",
            "full_name": "Климов Клим Климович",
            "birthdate": date(1990, 9, 9),
            "receipt_date": date(2024, 2, 5),
            "receipt_time": datetime.strptime("14:30", "%H:%S").time(),
            "floor": "3",
            "department": "Хирургия",
            "room_number": "3а-2",
            "bed": "K1",
            "type_of_diet": "ОВД веган (пост) без глютена",
            "comment": "Приносить компоты. все питание в жидком виде.",
            "status": "patient",
            "is_accompanying": "False",
            "is_probe": "False",
            "is_without_salt": "True",
            "is_without_lactose": "True",
            "is_pureed_nutrition": "False",
            "type_pay": "None",
            "extra_bouillon": "",
        }

        self.user = CustomUser.objects.create_user(**self.data)

    @patch("doctor.functions.functions.formatting_full_name")
    @patch("doctor.functions.functions.get_user_name")
    def test_check_archive_user(self, mock_get_user_name, mock_formatting_full_name):

        mock_get_user_name.return_value = ""
        mock_formatting_full_name.return_value = ""

        count = CustomUser.objects.count()
        request = self.factory.post("/doctor/", data=self.data)
        response = archiving_user(self.user, request)

        count_after_archive = CustomUser.objects.count()

        # проверка, статуса и возвращаемого значения
        self.assertEqual(self.user.status, "patient_archive")
        self.assertEqual(response, "archived")

        # проверка, что количество пациентов не поменялось
        self.assertEqual(count_after_archive, count)

        # проверка, что повторного архивирования не будет
        response = archiving_user(self.user, request)
        self.assertEqual(response, None)
