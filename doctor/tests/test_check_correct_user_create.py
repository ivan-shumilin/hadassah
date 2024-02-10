import unittest
from unittest.mock import patch

from django.test import RequestFactory

from doctor.forms import PatientRegistrationForm
from nutritionist.models import CustomUser
from doctor.functions.functions import create_user


class CustomUserCreateTests(unittest.TestCase):
    """ Полное тестирование функции create_user со всеми внутренними функциями.
     Warning!!! Для корректной работы тестов на данном этапе необходимо закомментировать импорт и
     все использования функции from doctor.tasks import my_job_send_messang_changes """

    def setUp(self):
        self.factory = RequestFactory()
        self.user = None

    @patch("doctor.functions.functions.get_user_name")
    @patch('doctor.functions.functions.logging')
    @patch("doctor.functions.functions.add_the_patient_menu")
    @patch("doctor.functions.functions.update_UsersToday")
    # @patch("doctor.functions.functions.check_meal_user")
    # @patch("doctor.functions.functions.is_user_look")
    @patch("doctor.functions.functions.get_now_show_meal")
    @patch("doctor.functions.functions.do_messang_send")
    @patch('doctor.functions.functions.add_the_patient_menu')
    @patch("doctor.functions.functions.add_features")
    @patch("doctor.functions.functions.check_change")
    def test_correct_user_save(
        self,
        mock_get_user_name,
        mock_logging,
        mock_add_the_patient_menu,
        mock_update_users_today,
        # mock_is_user_look,
        # mock_check_meal_user,
        mock_get_now_show_meal,
        mock_do_messang_send,
        mock_formatting_full_name,
        mock_add_features,
        mock_check_change,
    ):
        data = {
            "add_patient": "True",
            "full_name": "Егорова Светлана Степановна",
            "birthdate": "09.05.1990",
            "receipt_date": "01.02.2024",
            "receipt_time": "14:30:00",
            "floor": "3",
            "department": "Хирургия",
            "room_number": "4а-2",
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
            "is_change_diet_bd": "True",
            "extra_bouillon": "Завтрак",
            "is_bouillon_add": "True",
            "breakfast_add": "True",
            "lunch_add": "False",
            "afternoon_add": "False",
            "dinner_add": "False",
        }

        mock_logging.info.return_value = None
        mock_add_the_patient_menu.return_value = None
        mock_update_users_today.return_value = None
        mock_get_now_show_meal.return_value = "ужина"
        mock_do_messang_send.return_value = True
        mock_formatting_full_name.return_value = "Егорова Антонина Степановна"
        mock_add_features.return_value = 'Питание через зонд.'
        mock_check_change.return_value = 'завтрака', 0

        mock_get_user_name.return_value = ""
        count_after_add_user = CustomUser.objects.count()

        request = self.factory.post("/doctor/", data=data)
        request.user = self.user
        user_form = PatientRegistrationForm(request.POST)
        create_user(user_form, request)

        count = CustomUser.objects.count()
        current_user = CustomUser.objects.last()

        self.assertEqual(count_after_add_user, count - 1)

        # проверка, что данные корректно сохранились
        self.assertEqual(current_user.full_name, data["full_name"])
        self.assertEqual(current_user.birthdate.strftime("%d.%m.%Y"), data["birthdate"])
        self.assertEqual(current_user.receipt_date.strftime("%d.%m.%Y"), data["receipt_date"])
        self.assertEqual(current_user.receipt_time.strftime("%H:%M:%S"), data["receipt_time"])

        self.assertEqual(current_user.floor, data["floor"])
        self.assertEqual(current_user.department, data["department"])
        self.assertEqual(current_user.room_number, data["room_number"])
        self.assertEqual(current_user.bed, data["bed"])

        self.assertEqual(current_user.type_of_diet, data["type_of_diet"])
        self.assertEqual(current_user.comment, data["comment"])
        self.assertEqual(current_user.status, data["status"])

        self.assertFalse(current_user.is_accompanying)
        self.assertFalse(current_user.is_probe)
        self.assertTrue(current_user.is_without_salt)
        self.assertTrue(current_user.is_without_lactose)
        self.assertFalse(current_user.is_pureed_nutrition)
        self.assertEqual(current_user.type_pay, data["type_pay"])
        self.assertTrue(current_user.is_change_diet_bd)
        self.assertEqual(current_user.extra_bouillon, "breakfast")

        # проверим на добавление дубликатов
        response = create_user(user_form, request)
        count_after_duplicates = CustomUser.objects.count()
        self.assertEqual(count, count_after_duplicates)
        self.assertEqual(response, (None, None))
