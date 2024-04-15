import unittest
from unittest.mock import patch, MagicMock, call
from django.test import TestCase, Client
from django.urls import reverse

from nutritionist.views import tk


class TestTKView(TestCase):
    def setUp(self):
        self.client = Client()

    @patch('nutritionist.views.get_tree_ttk')
    @patch('nutritionist.views.ProductLp.objects.filter')
    @patch('nutritionist.views.Ingredient.objects.filter')
    def test_tk_view(self, mock_ingredient_filter, mock_product_filter, mock_get_tree_ttk):

        id_test = 123
        count = 1

        mock_get_tree_ttk.return_value = {'result': 'some_result'}, None
        result_dict = {'weight': '', 'technologyDescription': ''}

        mock_get_tree_ttk.side_effect = lambda id, count, _: ({'result': result_dict}, None)\
            if id == id_test else (result_dict, None)

        mock_ingredient_filter.return_value.first.return_value = MagicMock(weight=0.5, technologyDescription='Some description')
        mock_product_filter.return_value.first.return_value = MagicMock(image='some-image-url')

        # проверю что прихожу со страницы для эпидемиолога
        path = reverse('tk', args=[id_test, 0])
        response = self.client.get(reverse('tk', args=[id_test, 0]), {'request.path': path})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tk.html')

        self.assertIn('img', response.context)
        self.assertIn('result', response.context)
        self.assertIn('error', response.context)
        self.assertIn('count', response.context)
        self.assertIn('weight', response.context)
        #
        mock_get_tree_ttk.assert_called_once_with('123', count, [])
        mock_product_filter.assert_called_once_with(product_id='123')

        # теперь проверю что пришла со страницы 'tk_for_epidemiologist.html'
        path_2 = reverse('tk_for_epidemiologist', args=[id_test, 0])
        response_2 = self.client.get(reverse(path_2))

        self.assertEqual(response_2.status_code, 200)

        self.assertIn('img', response.context)
        self.assertIn('result', response.context)
        self.assertIn('error', response.context)
        self.assertIn('count', response.context)
        self.assertIn('weight', response.context)

        self.assertTemplateUsed(response_2, 'tk_for_epidemiologist.html')
