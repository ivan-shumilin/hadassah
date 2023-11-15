from doctor.functions.diet_formation import add_default_menu_on_one_day
from nutritionist.functions.ttk import enumeration_ingredients, add_ingredient_for_dict, enumeration_semifinisheds, \
    merger_products
from nutritionist.models import UsersToday, IngredientСache, AllProductСache, CustomUser
from django.db import transaction


def multiply_by_quantity(ingredients, count):
    """
    Умножаем ингредиенты на вес.
    """
    for ingredient in ingredients.values():
        ingredient['amount_in'] *= count
        ingredient['amount_middle'] *= count
        ingredient['amount_out'] *= count
    return ingredients


def get_count(product=None) -> int:
    if product is None:
        product = {}
    try:
        count: int = int(product.get('count', 0))
    except:
        count: int = 0
    return count


def get_ingredients_for_ttk(catalog):
    """
    Составляем список всех ингредиетов в заказе.
    """
    ingredients: dict = {}

    for meal in ['breakfast', 'lunch', 'afternoon', 'dinner']:
        for category in ['porridge', 'salad', 'soup', 'main', 'garnish', 'dessert', 'fruit', 'drink', 'products']:
            for product in catalog[meal][category]:
                if product and product.get('category', None) != 'товар':
                    if product.get('product_id', None):
                        # делаем иерархию ТТК плоской
                        sub_ingredients: dict = enumeration_ingredients(
                            product['product_id'],
                        )
                        # увеличиваем вес с учетом кол-ва блюд
                        count: int = get_count(product)
                        sub_ingredients = multiply_by_quantity(sub_ingredients, count)
                        # обьединяем ингредиеты
                        for sub_ingredient in sub_ingredients.items():
                            add_ingredient_for_dict(sub_ingredient, ingredients)

                    else:
                        print(f'нет product_id, {product["name"]}')

                    # добавляем sub_ingredients в ingredients
    return ingredients


def get_semifinished(catalog: dict, categories_all: set) -> dict:
    """
    Составляем список всех п/ф в заказе.
    """
    semifinisheds: dict = {}

    for meal in ['breakfast', 'lunch', 'afternoon', 'dinner']:
        for category in ['porridge', 'salad', 'soup', 'main', 'garnish', 'dessert', 'fruit', 'drink', 'products']:
            for product in catalog[meal][category]:
                if product and product.get('category', None) != 'товар':
                    if product.get('product_id', None):
                        semifinisheds[product['product_id']], categories_all = enumeration_semifinisheds(
                            product['product_id'],
                            int(product['count']),
                            categories_all,
                        )
                    else:
                        try:
                            print(f'нет product_id, {product["name"]}')
                        except:
                            print(f'нет product_id и name {product}')
    return semifinisheds, categories_all


def get_semifinished_level_1(semifinished_level_0: dict, filter_categories=[]) -> dict:
    """
    Возвращает ТТК второго уровня.
    """
    semifinished_level_1: dict = {}
    for product_level_1 in semifinished_level_0.values():
        if product_level_1:
            for key, product in product_level_1.get('items', {}).items():
                if product.get('status', None) != 'ingredient':
                    if key not in semifinished_level_1:
                        semifinished_level_1[key] = product
                    else:
                        merger_products(semifinished_level_1[key], product)
    return semifinished_level_1


import logging

from datetime import date, timedelta, datetime


def get_range_date(start: str, end: str):
    range: list = []

    start_date = datetime.strptime(start, '%d.%m.%Y')
    end_date = datetime.strptime(end, '%d.%m.%Y')

    current_date = start_date
    while current_date < end_date + timedelta(days=1):
        temp_date = current_date
        while temp_date < end_date + timedelta(days=1):

            range.append((current_date, temp_date))
            temp_date += timedelta(days=1)
        current_date += timedelta(days=1)
    return range


def join_catalog(catalog_set):
    import copy
    if len(catalog_set) == 1:
        return catalog_set[0]

    result = copy.deepcopy(catalog_set[0])
    for catalog in catalog_set[1:]:
        for meal_name, meal_products in catalog.items():
            for category_name, category_products in meal_products.items():
                for product in category_products:
                    if product:
                        # поверяем в result если есть такой продукт - обьединяем,
                        # если нет - добавляем
                        for product_from_result in result[meal_name][category_name]:
                            if product_from_result:
                                if product.get('id', None) == product_from_result.get('id', None):
                                    # обьединяем продукты
                                    product_from_result['count'] = str(int(product_from_result['count']) + int(product['count']))
                                    break
                        else:
                            result[meal_name][category_name].append(product)
    return result


def add_menu_three_days_ahead_from_caching():
    """
    Добовляем меню на 4-ый и 5-ый день.
    """
    users = CustomUser.objects.filter(status='patient')
    days = [date.today() + timedelta(days=delta) for delta in [3, 4, 5, 6]]
    for user in users:
        menu_all = MenuByDay.objects.filter(user_id=user.id)
        # порядок дней для формирования меню (БД)
        if user.type_of_diet == 'БД день 1':
            days_for_bd = ['понедельник', 'понедельник', 'понедельник', 'понедельник', 'понедельник', 'понедельник', 'понедельник']
        elif user.type_of_diet == 'БД день 2':
            days_for_bd = ['вторник', 'вторник', 'вторник', 'вторник', 'вторник', 'вторник', 'вторник']
        else:
            days_for_bd = []
        for index, day in enumerate(days):
            if len(menu_all.filter(date=str(day))) == 0 and (day >= user.receipt_date):
                for change_day in days[index:]:
                    add_default_menu_on_one_day(change_day, user, index, days_for_bd)
    return


def del_menu_three_days_ahead_from_caching():
    MenuByDay.objects.filter(date__in=[date.today() + timedelta(days=delta) for delta in [3, 4, 5, 6]]).delete()



def caching_ingredients():
    """
    Расчитываем иггредиеты на два дня вперед.
    """
    # реализоано кешировани. Там есть какая-то ошибка, надо будет пофиксить. Отрпавить на сервер. Добавить блюда.
    # и накатить все обнавления
    # добавляем данные в MenuByDay на 4-ый и 5-ый день для расчетов
    add_menu_three_days_ahead_from_caching()
    # start = date.today().strftime('%d.%m.%Y')
    # end = (date.today() + timedelta(days=1)).strftime('%d.%m.%Y')

    start = date.today().strftime('%d.%m.%Y')
    end = (date.today() + timedelta(days=6)).strftime('%d.%m.%Y')
    
    range = get_range_date(start, end)

    meal: str
    day: str
    is_public = False  # выводим технические названия блюд, не публичные
    type_order: str = 'flex-order'
    users = UsersToday.objects.all()
    for start, end in range:
        print('***********************************************************')
        print('***********************************************************')
        print('***********************************************************')
        print(f"{start.strftime('%d.%m.%Y')} - {end.strftime('%d.%m.%Y')}")
        print('***********************************************************')
        print('***********************************************************')
        print('***********************************************************')

        i = 0
        catalog_set: list = []
        while start + timedelta(days=i) <= end:
            date_create = (start + timedelta(days=i)).strftime('%Y-%m-%d')
            i += 1
            catalog: dict = {}
            for meal in ['breakfast', 'lunch', 'afternoon', 'dinner']:
                catalog[meal] = create_catalog_all_products_on_meal(users, meal, type_order, date_create, is_public)
            catalog_set.append(catalog)

        catalog = join_catalog(catalog_set)
        try:
            IngredientСache.objects.create(
                ingredient=get_ingredients_for_ttk(catalog),
                start=start,
                end=end,
            )
        except:
            logging.error(f'Ошибка в записи ингредиетов в КЕШ')
        AllProductСache.objects.create(
            all_product=catalog,
            start=start,
            end=end,
        )
    del_menu_three_days_ahead_from_caching()

from doctor.functions.functions import check_value_two, add_features
from nutritionist.functions.functions import combine_broths
from nutritionist.models import MenuByDay, MenuByDayReadyOrder


def create_catalog_all_products_on_meal(users, meal, type_order, date_create, is_public):
    """
    Получаем все блюда на прием пищи
    """

    catalog: dict = {}

    for category in ['porridge', 'salad', 'soup', 'main', 'garnish', 'dessert', 'fruit', 'drink', 'products']:
        list_whith_unique_products = []
        for diet in ['ОВД', 'ОВД без сахара', 'ЩД', 'ЩД без сахара', 'БД день 1',
                  'БД день 2', 'ОВД веган (пост) без глютена', 'Нулевая диета',
                  'НБД', 'ВБД', 'НКД', 'Безйодовая', 'ПЭТ/КТ', 'Без ограничений',
                  'ОВД (Э)', 'ОВД без сахара (Э)', 'ЩД (Э)', 'ЩД без сахара (Э)', 'БД день 1 (Э)',
                  'БД день 2 (Э)', 'ОВД веган (пост) без глютена (Э)', 'Нулевая диета (Э)',
                  'НБД (Э)', 'ВБД (Э)', 'НКД (Э)', 'Безйодовая (Э)', 'ПЭТ/КТ (Э)', 'Без ограничений (Э)',
                  'ОВД (П)', 'ОВД без сахара (П)', 'ЩД (П)', 'ЩД без сахара (П)', 'БД день 1 (П)',
                  'БД день 2 (П)', 'ОВД веган (пост) без глютена (П)', 'Нулевая диета (П)',
                  'НБД (П)', 'ВБД (П)', 'НКД (П)', 'Безйодовая (П)', 'ПЭТ/КТ (П)', 'Без ограничений (П)'
                  ]:
            users_with_diet = users.filter(type_of_diet=diet)
            all_products = [] # стовляем список всех продуктов
            comment_list = []
            for user in users_with_diet:
                if type_order == 'flex-order':
                    menu_all = MenuByDay.objects.filter(user_id=user.user_id)
                else:
                    menu_all = MenuByDayReadyOrder.objects.filter(user_id=user.id)
                # if category == 'products' or category ==  'drink':
                #     pr = check_value_two(menu_all, str((date_create)), meal, category, is_public)
                if category == 'soup':
                    pr = check_value_two(menu_all, str((date_create)), meal, 'soup', user.id, is_public) + \
                         check_value_two(menu_all, str((date_create)), meal, 'bouillon', user.id, is_public)
                    try:
                        pr.remove(None)
                    except:
                        pass
                else:
                    pr = check_value_two(menu_all, str((date_create)), meal, category, user.id, is_public)

                if pr[0] not in [None, [None]]:
                    for item in pr:
                        item['comment'] = add_features(user.comment,
                             user.is_probe,
                             user.is_without_salt,
                             user.is_without_lactose,
                             user.is_pureed_nutrition)
                        all_products.append(item)

            # составляем список с уникальными продуктами
            unique_products = []
            for product in all_products:
                flag = True
                for un_product in unique_products:
                    if product != None or un_product != None:
                        if product['id'] == un_product['id']:
                            flag = False
                if flag == True:
                    if product:
                        if 'cafe' not in product['id']:
                            unique_products.append(product)

            # добавляем элеметны списока с уникальными продуктами, кол-вом(сколько продуктов всего)
            # типом диеты
            for un_product in unique_products:
                count = 0
                comment_list = []
                for product in all_products:
                    if product['id'] == un_product['id']:
                        count += 1
                        comment_list.append(product['comment'])
                un_product['count'] = str(count)
                un_product.setdefault('diet', []).append(diet)
                if '' in comment_list:
                    comment_list.sort()
                comment_set = set(comment_list)
                comment_list_dict = [{'comment': f'{"Без комментария." if item == "" else item}', 'count': comment_list.count(item)} for item in comment_set]

                un_product['comments'] = comment_list_dict

            [list_whith_unique_products.append(item) for item in unique_products]
        catalog[category] = list_whith_unique_products

    for cat in catalog.values():
        for i, pr in enumerate(cat):
            for ii in range(i + 1, len(cat)):
                if pr != None and cat[ii] != None:
                    if pr['id'] == cat[ii]['id']:
                        pr['count'] = str(int(pr['count']) + int(cat[ii]['count']))
                        for item in cat[ii]['diet']:
                            pr.setdefault('diet', []).append(item)
                        pr['comments'] = pr['comments'] + cat[ii]['comments']
                        cat[ii] = None
    # обьединяем доп. бульон и бульон и удаляем None
    soups = [soup for soup in catalog['soup'] if soup]
    soups = combine_broths(soups)
    catalog['soup'] = soups

    for item in catalog.values():
        for product in item:
            if product != None:
                catalog_key_set = list(set([item['comment'] for item in product['comments']]))
                if 'Без комментария.' in catalog_key_set:
                    catalog_key_set.remove('Без комментария.')
                    catalog_key_set.insert(0, 'Без комментария.')
                result = []
                if 'Без комментария.' in catalog_key_set:
                    catalog_key_set
                for key in catalog_key_set:
                    result.append({'comment': key,
                                   'count': sum([item['count'] for item in product['comments'] if key == item['comment']])})
                product['comments'] = result

    number = 0
    for item in catalog.values():
        for product in item:
            if product != None:
                number += 1
                product['number'] = number
                product['diet'] = {
                    'many': len(product['diet']) > 1,
                    'diet': [{'name': pr} for pr in product['diet']]
                }

    return catalog
