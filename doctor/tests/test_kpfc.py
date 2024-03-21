import unittest

from django.urls import reverse

from doctor.functions.functions import get_normal_kpfc
from doctor.views import GetNewKpfc
from django.test import RequestFactory


# КРУГОВОЙ ИМПОРТ - КОММЕНТ my_job_sending in doctor/func/func
class TestGetNormalKpfc(unittest.TestCase):
    def test_ovd_diet(self):
        expected_result = {
            'p': (76, 99),
            'f': (63, 88),
            'c': (270, 363),
            'k': (1953, 2640)
        }
        result = get_normal_kpfc('ОВД')
        self.assertEqual(result, expected_result)

    def test_shd_diet(self):
        expected_result = {
            'p': (76, 99),
            'f': (63, 88),
            'c': (270, 385),
            'k': (1953, 2728)
        }
        result = get_normal_kpfc('ЩД')
        self.assertEqual(result, expected_result)

    def test_vbd_diet(self):
        expected_result = {
            'p': (99, 132),
            'f': (72, 99),
            'c': (225, 385),
            'k': (1872, 2959)
        }
        result = get_normal_kpfc('ВБД')
        self.assertEqual(result, expected_result)

    def test_nbd_diet(self):
        expected_result = {
            'p': (18, 66),
            'f': (72, 99),
            'c': (315, 440),
            'k': (1908, 2915)
        }
        result = get_normal_kpfc('НБД')
        self.assertEqual(result, expected_result)

    def test_nkd_diet(self):
        expected_result = {
            'p': (71, 88),
            'f': (54, 77),
            'c': (117, 165),
            'k': (1206, 1705)
        }
        result = get_normal_kpfc('НКД')
        self.assertEqual(result, expected_result)

    def test_unknown_diet(self):
        result = get_normal_kpfc('Unknown Diet')
        self.assertIsNone(result)


class TestGetNewKpfc(unittest.TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_get_new_kpfc(self):
        url = reverse('get_new_kpfc')
        request = self.factory.get(url, {'type_of_diet': 'ОВД'})
        view = GetNewKpfc.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)

        # Проверю какую нибудь диету
        expected_data = {
            'p': (76, 99),
            'f': (63, 88),
            'c': (270, 363),
            'k': (1953, 2640)
        }
        self.assertEqual(response.data, expected_data)

        data = {'type_of_diet': 'Unknown'}
        request = self.factory.get(url, data)
        view = GetNewKpfc.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.data)


if __name__ == '__main__':
    unittest.main()
