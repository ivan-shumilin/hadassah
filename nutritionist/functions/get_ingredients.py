from nutritionist.functions.ttk import enumeration_ingredients, add_ingredient_for_dict, enumeration_semifinisheds, \
    merger_products
from nutritionist.models import UsersToday, IngredientСache, AllProductСache


def get_ingredients_for_ttk(catalog):
    """
    Составляем список всех ингредиетов в заказе.
    """
    ingredients: dict = {}

    for meal in ['breakfast', 'lunch', 'afternoon', 'dinner']:
        for category in ['porridge', 'salad', 'soup', 'main', 'garnish', 'dessert', 'fruit', 'drink', 'products']:
            for product in catalog[meal][category]:
                if product:
                    if product.get('product_id', None):
                        sub_ingredients: dict = enumeration_ingredients(
                            product['product_id'],
                        )
                    else:
                        print(f'нет product_id, {product["name"]}')
                    # добавляем sub_ingredients в ingredients
                    for sub_ingredient in sub_ingredients.items():
                        add_ingredient_for_dict(sub_ingredient, ingredients)
    return ingredients


def get_semifinished(catalog: dict, categories_all: set) -> dict:
    """
    Составляем список всех п/ф в заказе.
    """
    semifinisheds: dict = {}

    for meal in ['breakfast', 'lunch', 'afternoon', 'dinner']:
        for category in ['porridge', 'salad', 'soup', 'main', 'garnish', 'dessert', 'fruit', 'drink', 'products']:
            for product in catalog[meal][category]:
                if product:
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

from datetime import date, timedelta


def caching_ingredients():
    """
    Расчитываем иггредиеты на два дня вперед.
    """

    COUNT_DAYS: dict = {
        'tomorrow': 1,
        'after-tomorrow': 2,
    }
    meal: str
    day: str
    catalog: dict = {}
    is_public = False  # выводим технические названия блюд, не публичные
    type_order: str = 'flex-order'
    users = UsersToday.objects.all()
    for day in COUNT_DAYS.keys():
        date_create = date.today() + timedelta(days=COUNT_DAYS[day])
        for meal in ['breakfast', 'lunch', 'afternoon', 'dinner']:
            catalog[meal] = create_catalog_all_products_on_meal(users, meal, type_order, date_create, is_public)

        try:
            IngredientСache.objects.create(
                ingredient=get_ingredients_for_ttk(catalog),
                day=day,
            )
        except:
            logging.error(f'Ошибка в записи ингредиетов в КЕШ')
        AllProductСache.objects.create(
            all_product=catalog,
            day=day,
        )


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
        for diet in ['ОВД', 'ОВД без сахара', 'ЩД', 'ЩД без сахара',
                     'ОВД веган (пост) без глютена', 'Нулевая диета',
                     'БД', 'ВБД', 'НБД', 'НКД', 'ВКД', 'БД день 1',
                     'БД день 2', 'Безйодовая', 'ПЭТ/КТ', 'Без ограничений']:
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
