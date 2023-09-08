# import logging
#
# from scripts.create_catalog_all_products_on_meal import create_catalog_all_products_on_meal
# from nutritionist.functions.get_ingredients import get_ingredients_for_ttk
# from nutritionist.models import UsersToday, IngredientСache
#
# from datetime import date, timedelta
#
#
# def caching_ingredients():
#     """
#     Расчитываем иггредиеты на два дня вперед.
#     """
#
#     COUNT_DAYS: dict = {
#         'tomorrow': 1,
#         'after-tomorrow': 2,
#     }
#     meal: str
#     day: str
#     catalog: dict = {}
#     is_public = False  # выводим технические названия блюд, не публичные
#     type_order: str = 'flex-order'
#     users = UsersToday.objects.all()
#     for day in COUNT_DAYS.keys():
#         date_create = date.today() + timedelta(days=COUNT_DAYS[day])
#         for meal in ['breakfast', 'lunch', 'afternoon', 'dinner']:
#             catalog[meal] = create_catalog_all_products_on_meal(users, meal, type_order, date_create, is_public)
#
#         try:
#             IngredientСache.objects.create(
#                 ingredient=get_ingredients_for_ttk(catalog),
#                 day=day,
#             )
#         except:
#             logging.error(f'Ошибка в записи ингредиетов в КЕШ')
