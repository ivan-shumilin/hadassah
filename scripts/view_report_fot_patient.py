import operator

from doctor.functions.functions import translate_meal
from nutritionist.models import Report, Product, ProductLp


def view_report_for_patient(patients_id: list) -> dict:
    """
    Выводим отчет по блюдам для группы пациентов. По заданым id пациентов.
    """

    filtered_report = Report.objects.filter(user_id__in=patients_id)

    report = {}
    for index, item in enumerate(filtered_report):
        if 'cafe' in item.product_id:
            try:
                product = Product.objects.get(id=item.product_id.split('-')[2])
                report.setdefault(item.date_create, []).append(
                    {'meal': f'{item.meal} ({item.type_of_diet})',
                     'category': product.category,
                     'name': product.name,
                     })
            except ValueError:
                pass
        else:
            if ',' in item.product_id:
                for id in item.product_id.split(','):
                    try:
                        product = ProductLp.objects.get(id=id)
                        report.setdefault(item.date_create, []).append(
                            {'meal': item.meal,
                             'category': product.category,
                             'name': product.name,
                             })
                    except:
                        pass
            else:
                try:
                    product = ProductLp.objects.get(id=item.product_id)
                    report.setdefault(item.date_create, []).append(
                        {'meal': item.meal,
                         'category': product.category,
                         'name': product.name,
                         })
                except:
                    pass

    meals = ['breakfast', 'lunch', 'afternoon', 'dinner']

    for data, reports in report.items():
        print(data)
        for meal in meals:
            print(translate_meal(meal))
            for r in reports:
                if r['meal'] == meal:
                    print(r['name'])

    print('End')
