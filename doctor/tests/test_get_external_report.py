import datetime
import unittest

from nutritionist.functions.report import create_external_report
from nutritionist.models import CustomUser, Report


class TestExternalReportCreate(unittest.TestCase):

    def setUp(self):
        user = CustomUser.objects.create_user(username="test_for_excel")

        # создадим данные о завтраке состоящего из продукта с id=299
        data_1 = {
            "user_id": user,
            "product_id": 299,
            "date_create": "2024-02-15",
            "meal": "breakfast",
            "type_of_diet": "ОВД",
            "category": None,
            "type": "emergency-day",
        }

        data_2 = {
            "user_id": user,
            "product_id": 109,
            "date_create": "2024-02-15",
            "meal": "dinner",
            "type_of_diet": "Нулевая диета",  # 150
            "category": None,
            "type": None,
        }

        Report.objects.create(**data_1)
        Report.objects.create(**data_2)

    def test_get_report_dict(self):
        query = Report.objects.all()
        response = create_external_report(query)
        check_dct = {
            "2024-02-15": {
                "afternoon": {},
                "breakfast": {
                    "ОВД": {
                        "count": 1,
                        "count_bouillon": 0,
                        "count_emergency_food": 0,
                        "money": 750,
                    }
                },
                "dinner": {
                    "Нулевая диета": {
                        "count": 1,
                        "count_bouillon": 0,
                        "count_emergency_food": 0,
                        "money": 150,
                    }
                },
                "lunch": {},
                "Всего": {"count": 2, "money": 900},
            },
            "Итого": {"Всего за период": {"count": 2, "money": 900}},
            "Нулевая диета": {"count": 1, "money": 150},
            "Сухпаек": {"count": 0, "money": 0},
        }

        self.assertEqual(response, check_dct)
