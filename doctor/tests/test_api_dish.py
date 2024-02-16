import unittest
from unittest.mock import patch, MagicMock

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from nutritionist.models import CustomUser
from doctor.views import DeleteDishAPIView

# ДОПИСАТЬ !


class TestDeleteDishAPIView(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = '/doctor/api/v1/delete-dish'
        self.data = {
            'id_user': 1,
            'date': '2024-02-14',
            'product_id': 277,
            'category': 'main',
            'meal': 'breakfast',
            'doctor': 'doctor_name',
        }

    @patch('doctor.functions.functions.get_order_status')
    @patch('doctor.views.get_product_by_id')
    @patch('doctor.views.logging_delete_dish_api')
    @patch('nutritionist.models.MenuByDay.objects')
    @patch('nutritionist.models.MenuByDayReadyOrder.objects')
    @patch('nutritionist.models.CustomUser.objects')
    @patch('nutritionist.models.ModifiedDish.objects')
    # @patch.object(DeleteDishAPIView, 'logger')
    def test_delete_dish_api(self, mock_get_order_status, mock_get_product_by_id,
                             mock_logging_delete_dish_api, mock_menu_by_day_objects,
                             mock_menu_by_day_ready_order_objects, mock_custom_user_objects,
                             mock_modified_dish_objects):

        mock_get_order_status.return_value = 'flex-order'
        mock_get_product_by_id.return_value = 'Mock-product'
        mock_logging_delete_dish_api.return_value = 'Mock-message'

        mock_serializer = MagicMock()
        mock_serializer.is_valid.return_value = True
        mock_serializer.validated_data = self.data

        mock_menu_item = MagicMock()
        mock_menu_item.category = 'mock_category'
        mock_menu_item.get.return_value = None
        mock_menu_item.save.return_value = None

        mock_menu_by_day_objects.all.return_value = []
        mock_menu_by_day_objects.get.return_value = mock_menu_item

        mock_menu_by_day_ready_order_objects.all.return_value = []
        mock_menu_by_day_ready_order_objects.get.return_value = None

        mock_modified_dish_objects.filter.return_value.first.return_value = None
        mock_custom_user_objects.get.return_value = MagicMock()

        # mock_logger.info.return_value = 'Mock-message'
        # mock_logger.error.return_value = 'Mock-message'

        with patch('doctor.serializer.AddDishSerializer') as mock_add_dish_serializer:
            mock_add_dish_serializer.return_value = mock_serializer

        response = self.client.delete(self.url, data=self.data, format='json')
        self.assertEqual(response.status_code, 200)

        # Проверяем, что были вызваны нужные методы
        mock_menu_by_day_objects.all.assert_called_once()
        mock_menu_by_day_ready_order_objects.all.assert_not_called()

        mock_logging_delete_dish_api.assert_called_with() # валится тут!

        # mock_modified_dish_objects.saves.assert_called_once()
        # mock_modified_dish_objects.filter.return_value.first.assert_called_once()
        # mock_modified_dish_objects.filter.return_value.first.return_value.delete.assert_not_called()



# class TestAddDishAPIView(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.user = CustomUser.objects.create(username='testuser_api', password='testpassword_api')

    # @patch('doctor.views.get_product_by_id')
    # @patch('doctor.views.logging_add_dish_api')
    # @patch('.MenuByDay.objects')
    # @patch('doctor.views.MenuByDayReadyOrder.objects')
    # def test_add_dish_api(self,
    #                       mock_menu_by_day_ready_order_objects,
    #                       mock_menu_by_day_objects,
    #                       mock_get_product_by_id,
    #                       mock_logging_add_dish_api
    #                       ):
    #
    #     url = '/doctor/api/v1/add-dish'
    #     data_add_api = {
    #         'id_user': self.user.id,
    #         'date': '2024-02-14',
    #         'product_id': 463,
    #         'category': 'category_name',
    #         'meal': 'meal_name',
    #         'doctor': 'doctor_name',
    #         'order_status': 'fix-order',
    #     }
    #
    #     # Заглушки для методов objects.all()
    #     mock_menu_by_day_objects.all.return_value = []
    #     mock_menu_by_day_ready_order_objects.all.return_value = []
    #
    #     mock_get_product_by_id.return_value = 'Кефир'
    #     mock_logging_add_dish_api.return_value = 'Мок-сообщение'
    #
    #     # Проверка, что используется таблица MenuByDay
    #     data_add_api['order_status'] = 'flex-order'
    #     response = self.client.post(url, data_add_api, format='json')
    #
    #     self.assertEqual(response.status_code, 200)
    #     mock_menu_by_day_objects.all.assert_called_once()
    #     mock_menu_by_day_ready_order_objects.all.assert_not_called()
    #
    #     # Проверка, что используется таблица MenuByDayReadyOrder
    #     data_add_api['order_status'] = 'flix-order'
    #     response = self.client.post(url, data_add_api, format='json')
    #
    #     self.assertEqual(response.status_code, 200)
    #     mock_menu_by_day_ready_order_objects.all.assert_called_once()
    #
    #     mock_logging_add_dish_api.info.assert_called_with('Save')
    #
    # @patch('doctor.views.get_product_by_id')
    # @patch('doctor.views.logging_change_dish_api')
    # @patch('doctor.views.MenuByDay.objects')
    # @patch('doctor.views.MenuByDayReadyOrder.objects')
    # def test_change_dish_api(self,
    #                          mock_menu_by_day_ready_order_objects,
    #                          mock_menu_by_day_objects,
    #                          mock_get_product_by_id,
    #                          mock_logging_change_dish_api
    #                          ):
    #     url = '/doctor/api/v1/change-dish'
    #     data_change_api = {
    #         'id_user': self.user.id,
    #         'date': '2024-02-14',
    #         'category': 'category_name',
    #         'meal': 'meal_name',
    #         'product_id_add': 277,
    #         'product_id_remove': 463,
    #         'doctor': 'doctor_name',
    #         'order_status': 'fix-order',
    #     }
    #
    #     # Заглушки для методов objects.all()
    #     mock_menu_by_day_objects.all.return_value = []
    #     mock_menu_by_day_ready_order_objects.all.return_value = []
    #
    #     mock_get_product_by_id.return_value = 'Кефир'
    #     mock_logging_change_dish_api.return_value = 'Мок-сообщение'
    #
    #     # Проверка, что используется таблица MenuByDay
    #     data_change_api['order_status'] = 'flex-order'
    #     response = self.client.post(url, data_change_api, format='json')
    #
    #     self.assertEqual(response.status_code, 200)
    #     mock_menu_by_day_objects.all.assert_called_once()
    #     mock_menu_by_day_ready_order_objects.all.assert_not_called()
    #
    #     # Проверка, что используется таблица MenuByDayReadyOrder
    #     data_change_api['order_status'] = 'fix-order'
    #     response = self.client.post(url, data_change_api, format='json')
    #
    #     self.assertEqual(response.status_code, 200)
    #     mock_menu_by_day_ready_order_objects.all.assert_called_once()
    #
    #     mock_logging_change_dish_api.info.assert_called_with('Save')

    # @patch('doctor.functions.functions.get_order_status')
    # @patch('doctor.views.get_product_by_id')
    # @patch('doctor.views.logging_delete_dish_api')
    # @patch('doctor.views.MenuByDay.objects')
    # @patch('doctor.views.MenuByDayReadyOrder.objects')
    # def test_delete_dish_api(self,
    #                          mock_get_order_status,
    #                          mock_menu_by_day_ready_order_objects,
    #                          mock_menu_by_day_objects,
    #                          mock_get_product_by_id,
    #                          mock_logging_delete_dish_api
    #                          ):
    #     url = '/doctor/api/v1/delete-dish'
    #     data_delete_api = {
    #         'id_user': self.user.id,
    #         'date': '2024-02-14',
    #         'category': 'category_name',
    #         'meal': 'meal_name',
    #         'product_id': 277,
    #         'doctor': 'doctor_name',
    #     }
    #
    #     # Заглушки для методов
    #     mock_get_order_status.return_value = 'flex-order'
    #
    #     mock_menu_by_day_objects.all.return_value = []
    #     mock_menu_by_day_ready_order_objects.all.return_value = []
    #     mock_get_product_by_id.return_value = 'Кефир'
    #     mock_logging_delete_dish_api.return_value = 'Мок-сообщение'
    #
    #     # Проверка, что используется таблица MenuByDay
    #     response = self.client.delete(url, data_delete_api, format='json')
    #
    #     self.assertEqual(response.status_code, 200)
    #     mock_menu_by_day_objects.all.assert_called_once()
    #     mock_menu_by_day_ready_order_objects.all.assert_not_called()
    #
    #     mock_get_order_status.return_value = 'fix-order'
    #     # Проверка, что используется таблица MenuByDayReadyOrder
    #     response = self.client.post(url, data_delete_api, format='json')
    #
    #     self.assertEqual(response.status_code, 200)
    #     mock_menu_by_day_ready_order_objects.all.assert_called_once()
    #
    #     mock_logging_delete_dish_api.info.assert_called_with('Save')
