from django.db import transaction
from typing import Optional

from django.db.models import Q

from nutritionist.models import MenuByDay


@transaction.atomic
def delete_or_change_product() -> str:
    """
    Удаляет один пробукт из заданого диапозона MenuByDay

    Если ProductLp - id
    Если Product - cafe-cat-id
    """
    start_date: str = '2023-06-02'
    end_date: str = '2023-06-04'
    old_product_id: str = '458'
    meals = ['dinner',]
    # new_product_id: Optional[str] = None
    # patient_id: Optional[str] = None


    category = 'drink'

    all_menu = MenuByDay.objects.filter(
        Q(date__range=[start_date, end_date]),
        Q(meal__in=meals)
    )
    for menu in all_menu:
        product_set = getattr(menu, category)
        product_set = product_set.split(',')
        product_set = [pr for pr in product_set if pr != old_product_id]
        product_set = ','.join(product_set)
        setattr(menu, category, product_set)

    MenuByDay.objects.bulk_update(all_menu, [category])

