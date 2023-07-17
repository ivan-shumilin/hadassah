from django.db import transaction
from typing import Optional

from django.db.models import Q

from nutritionist.models import MenuByDay, MenuByDayReadyOrder


@transaction.atomic
def delete_or_change_product() -> str:
    """
    Удаляет один пробукт из заданого диапозона MenuByDay

    Если ProductLp - id
    Если Product - cafe-cat-id
    """
    start_date: str = '2023-07-17'
    end_date: str = '2023-07-17'
    old_product_id: str = '291'
    meals = ['dinner',]
    new_product_id: Optional[str] = '500'
    diet = "ОВД"

    # patient_id: Optional[str] = None

    category = 'garnish'

    all_menu = MenuByDay.objects.filter(
        Q(date__range=[start_date, end_date]),
        Q(meal__in=meals),
        type_of_diet=diet,
    )
    for menu in all_menu:
        product_set = getattr(menu, category)
        product_set = product_set.split(',')
        product_set = [pr for pr in product_set if pr != old_product_id]
        product_set.append(new_product_id)
        product_set = ','.join(product_set)
        setattr(menu, category, product_set)

    MenuByDay.objects.bulk_update(all_menu, [category])


# добавить позицию в меню
from nutritionist.models import MenuByDay
all_menu = MenuByDay.objects.filter(
    Q(date__range=["2023-06-22", "2023-06-22"]),
    Q(meal__in=['afternoon',]),
    Q(type_of_diet__in=["ОВД", "ЩД", "ВБД", "ВКД"]),
)
for menu in all_menu:
    product_set = menu.dessert.split(',')
    product_set.append('458')
    product_set = ','.join(product_set)
    menu.drink = product_set.strip(',')
    menu.save()



# жесткое добавление позиции в меню
from nutritionist.models import MenuByDay
all_menu = MenuByDay.objects.filter(
    Q(date__range=["2023-06-22", "2023-06-22"]),
    Q(meal__in=['afternoon',]),
    Q(type_of_diet__in=["ОВД", "ЩД", "ВБД", "ВКД"]),
)
for menu in all_menu:
    menu.dessert = '573'
    menu.save()


