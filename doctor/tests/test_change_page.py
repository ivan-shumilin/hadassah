import unittest
from unittest.mock import patch, MagicMock
from django.test import RequestFactory
from django.urls import reverse

from nutritionist.views import tk


class TestTKView(unittest.TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @patch('nutritionist.views.get_tree_ttk')
    @patch('nutritionist.views.ProductLp.objects.filter')
    @patch('nutritionist.views.Ingredient.objects.filter')
    def test_tk_view(self, mock_ingredient_filter, mock_product_filter, mock_get_tree_ttk):
        id = 123
        count = '1'
        mock_get_tree_ttk.return_value = {'result': 'Технологическая карта'}, None
        mock_ingredient_filter.return_value.first.return_value = MagicMock(weight=0.5, technologyDescription='Some description')
        mock_product_filter.return_value.first.return_value = MagicMock(image='some-image-url')

        request = self.factory.get(reverse('tk', args=[id, 0]))
        response = tk(request, id, count)

        # self.assertEqual(response.status_code, 200)
        # self.assertIn('img', response.context)
        # self.assertIn('result', response.context)
        # self.assertIn('error', response.context)
        # self.assertIn('count', response.context)
        # self.assertIn('weight', response.context)

        mock_get_tree_ttk.assert_called_once_with(id, 3, [])
        mock_ingredient_filter.assert_called_once_with(product_id=id)
        mock_product_filter.assert_called_once_with(product_id=id)

        # Test if request.path == reverse('tk_for_epidemiologist', args=[id, 0])
        request = self.factory.get(reverse('tk_for_epidemiologist', args=[id, 0]))
        response = tk(request, id, count)
        self.assertEqual(response.template_name, 'tk_for_epidemiologist.html')


if __name__ == '__main__':
    unittest.main()