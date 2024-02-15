import unittest
from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from doctor.views import AddDishAPIView, get_product_by_id, logging_change_dish_api, ChangeDishAPIView
from nutritionist.models import CustomUser, MenuByDay, MenuByDayReadyOrder


class ChangeDishAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create(username='testuser_api', password='testpassword_api')

    from unittest.mock import patch

    class TestAddDishAPIView(TestCase):
        def setUp(self):
            self.client = APIClient()
            self.user = CustomUser.objects.create(username='testuser_api', password='testpassword_api')

        @patch('doctor.views.get_product_by_id')
        @patch('doctor.views.logging_add_dish_api')
        @patch('doctor.views.MenuByDay.objects')
        @patch('doctor.views.MenuByDayReadyOrder.objects')
        def test_add_dish_api(self,
                              mock_menu_by_day_ready_order_objects,
                              mock_menu_by_day_objects,
                              mock_get_product_by_id,
                              mock_logging_add_dish_api
                              ):

            url = '/doctor/api/v1/add-dish'
            data_add_api = {
                'id_user': self.user.id,
                'date': '2024-02-14',
                'product_id': 463,
                'category': 'category_name',
                'meal': 'meal_name',
                'doctor': 'doctor_name',
                'order_status': 'fix-order',
            }

            # Заглушки для методов objects.all()
            mock_menu_by_day_objects.all.return_value = []
            mock_menu_by_day_ready_order_objects.all.return_value = []

            mock_get_product_by_id.return_value = 'Кефир'
            mock_logging_add_dish_api.return_value = 'Мок-сообщение'

            # Проверка, что используется таблица MenuByDay
            data_add_api['order_status'] = 'flex-order'
            response = self.client.post(url, data_add_api, format='json')

            self.assertEqual(response.status_code, 200)
            mock_menu_by_day_objects.all.assert_called_once()
            mock_menu_by_day_ready_order_objects.all.assert_not_called()

            # Проверка, что используется таблица MenuByDayReadyOrder
            data_add_api['order_status'] = 'flix-order'
            response = self.client.post(url, data_add_api, format='json')

            self.assertEqual(response.status_code, 200)
            mock_menu_by_day_ready_order_objects.all.assert_called_once()

            mock_logging_add_dish_api.info.assert_called_with('Save')

        @patch('doctor.views.get_product_by_id')
        @patch('doctor.views.logging_change_dish_api')
        @patch('doctor.views.MenuByDay.objects')
        @patch('doctor.views.MenuByDayReadyOrder.objects')
        def test_change_dish_api(self,
                                 mock_menu_by_day_ready_order_objects,
                                 mock_menu_by_day_objects,
                                 mock_get_product_by_id,
                                 mock_logging_change_dish_api
                                 ):
            url = '/doctor/api/v1/change-dish'
            data_change_api = {
                'id_user': self.user.id,
                'date': '2024-02-14',
                'category': 'category_name',
                'meal': 'meal_name',
                'product_id_add': 277,
                'product_id_remove': 463,
                'doctor': 'doctor_name',
                'order_status': 'fix-order',
            }

            # Заглушки для методов objects.all()
            mock_menu_by_day_objects.all.return_value = []
            mock_menu_by_day_ready_order_objects.all.return_value = []

            mock_get_product_by_id.return_value = 'Кефир'
            mock_logging_change_dish_api.return_value = 'Мок-сообщение'

            # Проверка, что используется таблица MenuByDay
            data_change_api['order_status'] = 'flex-order'
            response = self.client.post(url, data_change_api, format='json')

            self.assertEqual(response.status_code, 200)
            mock_menu_by_day_objects.all.assert_called_once()
            mock_menu_by_day_ready_order_objects.all.assert_not_called()

            # Проверка, что используется таблица MenuByDayReadyOrder
            data_change_api['order_status'] = 'fix-order'
            response = self.client.post(url, data_change_api, format='json')

            self.assertEqual(response.status_code, 200)
            mock_menu_by_day_ready_order_objects.all.assert_called_once()

            mock_logging_change_dish_api.info.assert_called_with('Save')

        @patch('doctor.views.get_product_by_id')
        @patch('doctor.views.logging_delete_dish_api')
        @patch('doctor.views.MenuByDay.objects')
        @patch('doctor.views.MenuByDayReadyOrder.objects')
        def test_change_dish_api(self,
                                 mock_menu_by_day_ready_order_objects,
                                 mock_menu_by_day_objects,
                                 mock_get_product_by_id,
                                 mock_logging_delete_dish_api
                                 ):
            url = '/doctor/api/v1/delete-dish'
            data_change_api = {
                'id_user': self.user.id,
                'date': '2024-02-14',
                'category': 'category_name',
                'meal': 'meal_name',
                'product_id': 277,
                'doctor': 'doctor_name',
                'order_status': 'fix-order',
            }

            # Заглушки для методов objects.all()
            mock_menu_by_day_objects.all.return_value = []
            mock_menu_by_day_ready_order_objects.all.return_value = []

            mock_get_product_by_id.return_value = 'Кефир'
            mock_logging_delete_dish_api.return_value = 'Мок-сообщение'

            # Проверка, что используется таблица MenuByDay
            data_change_api['order_status'] = 'flex-order'
            response = self.client.post(url, data_change_api, format='json')

            self.assertEqual(response.status_code, 200)
            mock_menu_by_day_objects.all.assert_called_once()
            mock_menu_by_day_ready_order_objects.all.assert_not_called()

            # Проверка, что используется таблица MenuByDayReadyOrder
            data_change_api['order_status'] = 'fix-order'
            response = self.client.post(url, data_change_api, format='json')

            self.assertEqual(response.status_code, 200)
            mock_menu_by_day_ready_order_objects.all.assert_called_once()

            mock_logging_delete_dish_api.info.assert_called_with('Save')
