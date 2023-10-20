from django.db import transaction

from nutritionist.models import TimetableLp


@transaction.atomic
def copy_diet():
    """
    Копирует существуюшию диету в новую диету.
    """
    to_create = []
    days = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье']
    meals = ['breakfast', 'lunch', 'afternoon', 'dinner']
    # meals = ['dinner']
    # diets = ['ОВД', 'ОВД без сахара', 'ОВД веган (пост) без глютена', 'Нулевая диета', 'БД день 1', 'БД день 2',
    #          'ЩД', 'ЩД без сахара', 'НБД', 'ВБД', 'НКД', 'ВКД', 'Безйодовая', 'ПЭТ/КТ', 'Без ограничений']
    diets = ['Нулевая диета']
    diet_change = 'ОВД (Э)'
    for diet in diets:
        for day in days:
            for meal in meals:
                protduct_set = TimetableLp.objects.filter(type_of_diet=diet, day_of_the_week=day, meals=meal)
                for product in protduct_set:
                    to_create.append(TimetableLp(
                        item=product.item,
                        type_of_diet=diet_change,
                        day_of_the_week=day,
                        meals=meal,
                    ))
    TimetableLp.objects.bulk_create(to_create)
    return 'OK'
