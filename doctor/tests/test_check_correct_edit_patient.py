import unittest

from django.test import RequestFactory

from doctor.forms import PatientRegistrationForm
from doctor.functions.functions import edit_user
from nutritionist.models import CustomUser
from unittest.mock import patch


class MyTestCase(unittest.TestCase):
    """ Полное тестирование функции edit_user.
     Warning!!! Для корректной работы тестов на данном этапе необходимо закомментировать импорт и
     все использования функции from doctor.tasks import my_job_send_messang_changes """

    def setUp(self):
        self.type = 'edit'
        self.factory = RequestFactory()
        self.data = {
            "username": "akdjflsdjF;",
            "full_name": "Тестов Тест Тестович",
            "birthdate": "1989-09-09",
            "receipt_date": "2024-03-01",
            "receipt_time": "14:30:00",
            "floor": "3",
            "department": "Хирургия",
            "room_number": "4а-1",
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
            "is_change_diet_bd": "False",
            "extra_bouillon": "",
        }

        self.user = CustomUser.objects.create_user(**self.data)

    @patch("doctor.functions.functions.get_user_name")
    @patch("doctor.functions.functions.comment_formatting")
    @patch("doctor.functions.functions.add_features")
    def test_edit_user(self, mock_comment_formatting, mock_add_features, mock_get_user_name):
        data_for_insert = {
                    "id_edit_user": str(self.user.id),
                    "edit_patient_flag": "On",
                    "full_name1": "Иванов Иван Иванович", # новые данные
                    "birthdate1": "09.09.1989",
                    "receipt_date1": "01.03.2024",
                    "receipt_time1": "14:30:00",
                    "floor1": "3",
                    "department1": "Реанимация", # новые данные
                    "room_number1": "4а-1",
                    "bed1": "K1",
                    "type_of_diet1": "ОВД веган (пост) без глютена",
                    "comment1": "Приносить компоты. все питание в жидком виде.",
                    "status1": "patient",
                    "edit_is_accompanying": "False",
                    "edit_is_probe": "False",
                    "edit_is_without_salt": "True",
                    "edit_is_without_lactose": "True",
                    "edit_is_pureed_nutrition": "False",
                    "edit_type_pay": "None",
                    "is_change_diet_bd1": "False",
                    "is_bouillon": "",
                    }

        mock_comment_formatting.return_value = ""
        mock_add_features.return_value = 'Питание через зонд.'
        mock_get_user_name.return_value = ""

        count = CustomUser.objects.count()

        request = self.factory.post("/doctor/", data=data_for_insert)
        user_form = PatientRegistrationForm(request.POST)
        edit_user(user_form, self.type, request)

        # проверка, что после редактирования у нас такое же количество пациентов, как и было
        count_after_insert = CustomUser.objects.count()
        self.assertEqual(count, count_after_insert)

        # проверка, что данные сохранились
        user_after_update = CustomUser.objects.get(id=self.user.id)
        self.assertEqual(user_after_update.full_name, "Иванов Иван Иванович")
        self.assertEqual(user_after_update.department, "Реанимация")

        # проверка, что другие данные - прежние
        self.assertEqual(user_after_update.receipt_time.strftime("%H:%M:%S"), self.data["receipt_time"])
        self.assertTrue(user_after_update.is_without_lactose)
