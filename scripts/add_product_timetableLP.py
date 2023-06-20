from django.db import transaction

from nutritionist.models import TimetableLp, ProductLp


@transaction.atomic
def add_product():
    """
    Добавляет продукт в меню
    """
    to_create = []
    days = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье']
    # meals = ['breakfast', 'lunch', 'afternoon', 'dinner']
    meals = ['dinner']
    diets = ['ОВД', 'ОВД без сахара', 'ОВД веган (пост) без глютена', 'Нулевая диета', 'БД день 1', 'БД день 2',
             'ЩД', 'ЩД без сахара', 'НБД', 'ВБД', 'НКД', 'ВКД', 'Безйодовая', 'ПЭТ/КТ', 'Без ограничений']
    # diets = ['ОВД']
    # diet_change = 'Без ограничений'
    product = ProductLp.objects.get(id='458')
    for diet in diets:
        for day in days:
            for meal in meals:
                to_create.append(TimetableLp(
                    item=product,
                    type_of_diet=diet,
                    day_of_the_week=day,
                    meals=meal,
                ))
    TimetableLp.objects.bulk_create(to_create)
    return 'OK'
