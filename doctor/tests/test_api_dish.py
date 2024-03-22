from unittest import TestCase, mock
from unittest.mock import patch, MagicMock, Mock

from django.urls import reverse
from rest_framework.test import APIClient


class AddDishAPIViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('add_dish_api')
        self.data = {
            'id_user': 1,
            'date': '2024-02-14',
            'product_id': 277,
            'category': 'main',
            'meal': 'breakfast',
            'doctor': 'doctor_name',
        }

    @patch('doctor.views.logging.getLogger')
    @patch('doctor.views.CustomUser.objects.get')
    @patch('doctor.views.ModifiedDish')
    @patch('doctor.views.UsersReadyOrder.objects.filter')
    @patch('doctor.views.MenuByDay.objects.all')
    @patch('doctor.views.MenuByDayReadyOrder.objects.all')
    @patch('doctor.views.get_order_status')
    @patch('doctor.views.get_product_by_id')
    def test_add_dish_api(self, mock_get_product_by_id, mock_get_order_status, mock_menu_by_day_ready_order_all,
                  mock_menu_by_day_all, mock_users_ready_order_filter, mock_modified_dish, mock_get_user,
                  mock_get_logger):
        # моки для логгера
        mock_logger_instance = MagicMock()
        mock_get_logger.return_value = mock_logger_instance

        mock_get_product_by_id.return_value = 'Test Product'
        mock_get_order_status.return_value = 'fix-order'
        mock_menu_by_day_all.return_value = MagicMock()
        mock_menu_by_day_ready_order_all.return_value = MagicMock()
        mock_users_ready_order_filter.return_value = MagicMock()
        mock_get_user.return_value = MagicMock()
        mock_modified_dish.objects.create.return_value = MagicMock()

        response = self.client.post(self.url, data=self.data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'status': 'OK'})

        mock_menu_by_day_all.assert_called()
        mock_menu_by_day_ready_order_all.assert_called()

        # проверю что вызывается save
        mock_menu = MagicMock()
        mock_item_menu = MagicMock()
        mock_menu.get.return_value = mock_item_menu
        mock_item_menu.category = ''
        mock_item_menu.save = MagicMock()
        mock_menu_by_day_ready_order_all.return_value = mock_menu

        self.client.post(self.url, data=self.data, format='json')
        self.assertTrue(mock_item_menu.save.called)

# Дописать!

class ChangeDishAPIViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('change_dish_api')
        self.data = {
            'id_user': 1,
            'date': '2024-02-14',
            'category': 'main',
            'meal': 'breakfast',
            'product_id_add': 277,
            'product_id_del': 278,
            'doctor': 'doctor_name',
        }

    @mock.patch('doctor.views.CustomUser.objects.filter')
    @mock.patch('doctor.views.ModifiedDish.objects.filter')
    @mock.patch('doctor.views.MenuByDay.objects.all')
    @mock.patch('doctor.views.MenuByDayReadyOrder.objects.all')
    @mock.patch('doctor.views.get_order_status')
    @mock.patch('doctor.views.get_product_by_id')
    def test_change_dish_api_success(self, mock_get_product_by_id, mock_get_order_status,
                                      mock_menu_by_day_ready_order_all, mock_menu_by_day_all,
                                      mock_modified_dish_filter, mock_custom_user_filter):

        mock_get_product_by_id.side_effect = lambda x: 'Test Product' if x == 277 else 'Deleted Product'
        mock_get_order_status.return_value = 'fix-order'

        mock_menu_by_day_all.return_value = mock.Mock()
        mock_menu_by_day_ready_order_all.return_value = mock.Mock()

        # Мокирование CustomUser и ModifiedDish для успешного выполнения операции
        mock_custom_user_filter.return_value.first.return_value = mock.Mock()
        mock_modified_dish_filter.return_value.first.return_value = mock.Mock()

        mock_menu = MagicMock()
        mock_item_menu = MagicMock()
        mock_menu.get.return_value = mock_item_menu
        mock_item_menu.category = ''
        mock_item_menu.save = MagicMock()
        mock_menu_by_day_ready_order_all.return_value = mock_menu

        response = self.client.put(self.url, data=self.data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'status': 'OK'})


    # @mock.patch('doctor.views.CustomUser.objects.filter')
    # @mock.patch('doctor.views.ModifiedDish.objects.filter')
    # @mock.patch('doctor.views.MenuByDay.objects.all')
    # @mock.patch('doctor.views.MenuByDayReadyOrder.objects.all')
    # @mock.patch('doctor.views.get_order_status')
    # @mock.patch('doctor.views.get_product_by_id')
    # def test_change_dish_api_error(self, mock_get_product_by_id, mock_get_order_status,
    #                                 mock_menu_by_day_ready_order_all, mock_menu_by_day_all,
    #                                 mock_modified_dish_filter, mock_custom_user_filter):
    #
    #     mock_get_product_by_id.side_effect = lambda x: 'Test Product' if x == 277 else 'Deleted Product'
    #     mock_get_order_status.return_value = 'fix-order'
    #
    #     mock_menu_by_day_all.return_value = mock.Mock()
    #     mock_menu_by_day_ready_order_all.return_value = mock.Mock()
    #
    #     # Мокирование CustomUser для ошибки при попытке удаления блюда
    #     mock_custom_user_filter.return_value.first.return_value = mock.Mock()
    #     mock_modified_dish_filter.return_value.first.return_value = mock.Mock(side_effect=Exception("Delete Error"))
    #
    #     response = self.client.put(self.url, data=self.data, format='json')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.data, {'status': 'Error'})
