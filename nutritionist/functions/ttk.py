import operator, time

from nutritionist.functions.functions import get_name_and_measure_unit, get_coefficient, create_ttk
from nutritionist.models import Ingredient, TTK, ProductLp
from doctor.functions.download import get_tk, get_measure_unit, get_allergens, get_weight_tk


def add_status():
    """
    Проставляем всем ТТК статус (блюдо, пф, ингредиент)
    """
    TTK.objects.filter(parent_ttk__isnull=True).update(status='product')
    TTK.objects.exclude(status__in=['pf', 'product']).update(status='ingredient')


def create_all_ttk(id: str, count=1):
    """
    Получаем тех. карту и обрабатываем ее.  Записываем в базу данных.
    """
    try:
        # получаем ТТК
        tk, error = get_tk(id)

        for item_tk_1 in tk['assemblyCharts']:
            # добавляем имя
            item_tk_1['name'], _ = get_name_and_measure_unit(item_tk_1['assembledProductId'])

            # добавляем вес
            try:
                item_tk_1['weight'] = \
                    Ingredient.objects.filter(product_id=item_tk_1['assembledProductId']).first().weight * 1000
            except:
                item_tk_1['weight'] = 0

            # получаем ед.измерения (кг, л)
            item_tk_1['measure_unit'] = get_measure_unit(item_tk_1['assembledProductId'])

            # добавляем имена и ед. измерения ингредиентам 1-ого уровня
            for item_tk_2 in item_tk_1['items']:
                name, measure_unit = get_name_and_measure_unit(item_tk_2['productId'])
                item_tk_2['name'] = name

        # Высчитываем вес с учетом того, что некоторые ТК указаны на определенное кол-во порций
        for item_tk_1 in tk['assemblyCharts']:
            count_por = item_tk_1['assembledAmount']
            for sub_item in item_tk_1['items']:
                sub_item['amountIn'] = sub_item['amountIn'] / count_por
                sub_item['amountMiddle'] = sub_item['amountMiddle'] / count_por
                sub_item['amountOut'] = sub_item['amountOut'] / count_por

        try:
            # записываем 0 уровень (само блюдо)
            result = tk['assemblyCharts'][0]
            parent_ttk = create_ttk(result, 'assembledProductId')
        except:
            result = "Нет данных"

        if result != "Нет данных":
            for ing in result['items']:
                for ing2 in tk['assemblyCharts'][1:]:
                    try:
                        if ing['productId'] == ing2['assembledProductId']:
                            ing['items'] = ing2['items'].copy()
                    except:
                        pass
                if 'items' not in ing:
                    ing['items'] = None

            result['allergens'] = get_allergens(id)

            for item in result['items']:
                if item['items']:
                    item['weight_tk'] = get_weight_tk(item['productId'])
                    for sub_item in item['items']:
                        sub_item['amountIn'] = item['amountIn'] * sub_item['amountIn']
                        sub_item['amountMiddle'] = item['amountMiddle'] * sub_item['amountMiddle']
                        sub_item['amountOut'] = item['amountOut'] * sub_item['amountOut']

            result['items'].sort(key=operator.itemgetter('sortWeight'))

            weight = int(result['weight'])
        else:
            weight = 0
        #######################
        # Получаем 3-ий уровень
        for item_1 in result['items']:
            # 1-ый уровень
            _, measure_unit = get_name_and_measure_unit(item_1['productId'])
            item_1['measure_unit'] = measure_unit
            parent1_ttk = create_ttk(item_1, 'productId', parent_ttk)
            print(
                f"1-{item_1['name']}|",
                f"Б в ед. изм. - {item_1['amountIn']}",
                f"Вес б, {item_1['amountMiddle']}",
                f"Вес н {item_1['amountOut']}"
            )
            item_1 = [] if item_1.get('items') is None else item_1.get('items')

            # 2-ой уровень
            for item_2 in item_1:
                _, measure_unit = get_name_and_measure_unit(item_2['productId'])
                item_2['measure_unit'] = measure_unit
                parent2_ttk = create_ttk(item_2, 'productId', parent1_ttk)
                parent1_ttk.status = 'pf'
                parent1_ttk.save(update_fields=['status'])
                print(
                    f"2--{item_2['name']}|",
                    f"Б ед. изм. - {item_2['amountIn']}",
                    f"Вес б, {item_2['amountMiddle']}",
                    f"Вес н, {item_2['amountOut']}"
                )
                # задержка для обращения к api, если не делать сервер iiko добавляет в ЧС
                time.sleep(1)
                # Получаем ТК 2-ого уровня
                tk, error = get_tk(item_2['productId'])
                if len(tk['assemblyCharts']) > 0:
                    weight_pf_local = {
                        'amountIn': item_2['amountIn'],
                        'amountMiddle': item_2['amountMiddle'],
                        'amountOut': item_2['amountOut'],
                    }
                    # получаем вес ТТК
                    try:
                        weight_pf_main = \
                            float(
                                Ingredient.objects.filter(
                                    product_id=item_2['productId']
                                ).first().weight
                            )
                    except:
                        weight_pf_main = 0
                    # вес всей ТТК / вес в ТТК 1-ого уровня * на кол-во порций в ТТК (закладка)

                    coefficient: dict = {
                        'amountIn': get_coefficient(
                            weight_pf_main,
                            weight_pf_local['amountIn'],
                            tk['assemblyCharts'][0]['assembledAmount'],
                        ),
                        'amountMiddle': get_coefficient(
                            weight_pf_main,
                            weight_pf_local['amountMiddle'],
                            tk['assemblyCharts'][0]['assembledAmount'],
                        ),
                        'amountOut': get_coefficient(
                            weight_pf_main,
                            weight_pf_local['amountOut'],
                            tk['assemblyCharts'][0]['assembledAmount'],
                        ),
                    }

                    item_2['items'] = []

                    # получаем ингредиенты 3-его уровня
                    for item_3 in tk['assemblyCharts'][0]['items']:
                        # вес п/ф в конкретной ТТК
                        weight_pf_local_2 = {
                            'amountIn': item_3['amountIn'] / coefficient['amountIn'],
                            'amountMiddle': item_3['amountMiddle'] / coefficient['amountMiddle'],
                            'amountOut': item_3['amountOut'] / coefficient['amountOut'],
                        }
                        # получение имени
                        name, measure_unit = get_name_and_measure_unit(item_3['productId'])
                        item_3['name'] = name
                        item_3['measure_unit'] = measure_unit
                        item_3['amountIn'] = weight_pf_local_2['amountIn']
                        item_3['amountMiddle'] = weight_pf_local_2['amountMiddle']
                        item_3['amountOut'] = weight_pf_local_2['amountOut']

                        item_2['items'].append(item_3)
                        parent3_ttk = create_ttk(item_3, 'productId',  parent2_ttk)
                        parent2_ttk.status = 'pf'
                        parent2_ttk.save(update_fields=['status'])
                        print(
                            f"3---{item_3['name']}",
                            f"Б в ед. изм {weight_pf_local_2['amountIn']}",
                            f"Вес б {weight_pf_local_2['amountMiddle']}",
                            f"Вес н {weight_pf_local_2['amountOut']}"
                        )

                        # вес закладки в ТТК в гр. или мл.
                        try:
                            weight_pf_main_2 = \
                                float(Ingredient.objects.filter(product_id=item_3['productId']).first().weight)
                        except:
                            weight_pf_main_2 = 0

                        coefficient_2 = {
                            'amountIn': get_coefficient(
                                weight_pf_main_2,
                                weight_pf_local_2['amountIn'],
                                1,
                            ),
                            'amountMiddle': get_coefficient(
                                weight_pf_main_2,
                                weight_pf_local_2['amountMiddle'],
                                1,
                            ),
                            'amountOut': get_coefficient(
                                weight_pf_main_2,
                                weight_pf_local_2['amountOut'],
                                1,
                            ),
                        }

                        item_3['items'] = []
                        for ing2 in tk['assemblyCharts'][1:]:
                            try:
                                if item_3['productId'] == ing2['assembledProductId']:
                                    for item_4 in ing2['items']:
                                        # вес п/ф в конкретной ТТК
                                        weight_pf_local_3 = {
                                            'amountIn': item_4['amountIn'] / coefficient_2['amountIn'],
                                            'amountMiddle': item_4['amountMiddle'] / coefficient_2['amountMiddle'],
                                            'amountOut': item_4['amountOut'] / coefficient_2['amountOut'],
                                        }
                                        # получение имени
                                        name, measure_unit = get_name_and_measure_unit(item_4['productId'])
                                        item_4['name'] = name
                                        item_4['measure_unit'] = measure_unit

                                        item_4['amountIn'] = weight_pf_local_3['amountIn']
                                        item_4['amountMiddle'] = weight_pf_local_3['amountMiddle']
                                        item_4['amountOut'] = weight_pf_local_3['amountOut']
                                        parent4_ttk = create_ttk(item_4, 'productId',  parent3_ttk)
                                        parent3_ttk.status = 'pf'
                                        parent3_ttk.save(update_fields=['status'])
                                        print(
                                            f"4----{item_4['name']}|",
                                            f"Б в ед. изм {item_4['amountIn']}",
                                            f"Вес б {item_4['amountMiddle']}",
                                            f"Вес н {item_4['amountOut']}"
                                        )
                                        item_3['items'].append(item_4)
                            except:
                                pass
    except:
        print('Ошибка', id)
        return None
    # проставить всем ингредиетам статус: блюдо, пф, ингредиент
    add_status()
    print('Успешно', id)
    return result, error, weight


def view_ttk(product_id='15918a36-734e-4f59-820c-1cd6a33d4e77'):
    """ Вывод ТТК """
    ttk_main = TTK.objects.filter(product_id=product_id).first()
    ttk_child = TTK.objects.filter(parent_ttk=ttk_main)
    for ttk in ttk_child:
        print('1- ', ttk.name, ttk.ingredient)
        ttk_child_2 = TTK.objects.filter(parent_ttk=ttk)
        for ttk in ttk_child_2:
            print('2-- ', ttk.name, ttk.ingredient)
            ttk_child_3 = TTK.objects.filter(parent_ttk=ttk)
            for ttk in ttk_child_3:
                print('3--- ', ttk.name, ttk.ingredient)
                ttk_child_4 = TTK.objects.filter(parent_ttk=ttk)
                for ttk in ttk_child_4:
                    print('4---- ', ttk.name, ttk.ingredient)
                    ttk_child_5 = TTK.objects.filter(parent_ttk=ttk)
                    for ttk in ttk_child_5:
                        print('5----- ', ttk.name, ttk.ingredient)



def if_none_get_zero(value):
    return float(value) if value is not None else 0

def is_categories(ttk, categories):
    if ttk.ingredient:
        return ttk.ingredient.groupId in categories
    return False


def add_ingredient(ttk, ingredients):
    if ttk.status == 'ingredient':
        if ttk.product_id in ingredients:
            ingredients[ttk.product_id]['amount_in'] =\
                if_none_get_zero(ingredients[ttk.product_id]['amount_in']) + if_none_get_zero(ttk.amount_in)
            ingredients[ttk.product_id]['amount_middle'] =\
                if_none_get_zero(ingredients[ttk.product_id]['amount_middle']) + if_none_get_zero(ttk.amount_middle)
            ingredients[ttk.product_id]['amount_out'] =\
                if_none_get_zero(ingredients[ttk.product_id]['amount_out']) + if_none_get_zero(ttk.amount_out)

        else:
            category = get_ingredient_category(ttk)
            ingredients[ttk.product_id] = {
                'measure_unit': ttk.measure_unit,
                'name': ttk.name,
                'amount_in': if_none_get_zero(ttk.amount_in),
                'amount_middle': if_none_get_zero(ttk.amount_middle),
                'amount_out': if_none_get_zero(ttk.amount_out),
                'category': category.get('id', '0')
            }


def add_ingredient_for_dict(ttk, ingredients):
    product_id, data = ttk
    if product_id in ingredients:
        ingredients[product_id]['amount_in'] = ingredients[product_id]['amount_in'] + data['amount_in']
        ingredients[product_id]['amount_middle'] = ingredients[product_id]['amount_middle'] + data['amount_middle']
        ingredients[product_id]['amount_out'] = ingredients[product_id]['amount_out'] + data['amount_out']
    else:
        ingredients[product_id] = {
            'name': data['name'],
            'measure_unit': data['measure_unit'],
            'amount_in': data['amount_in'],
            'amount_middle': data['amount_middle'],
            'amount_out': data['amount_out'],
            'category': data['category'],
         }


def merger_products(product_main: dict, product_sub: dict) -> dict:
    """
    Обьединяет две ТТК, проходит на 5 уровней в глубину.
    """

    product_main['amount_in'] = \
        if_none_get_zero(product_main['amount_in']) + if_none_get_zero(product_sub['amount_in'])
    product_main['amount_middle'] = \
        if_none_get_zero(product_main['amount_middle']) + if_none_get_zero(product_sub['amount_middle'])
    product_main['amount_out'] = \
        if_none_get_zero(product_main['amount_out']) + if_none_get_zero(product_sub['amount_out'])
# 1
    level_1 = {
        'main': product_main.get('items', {}),
        'sub': product_sub.get('items', {}),
    }
    for key1 in level_1['main'].keys():
        level_1['main'][key1]['amount_in'] = \
            (if_none_get_zero(level_1['main'][key1]['amount_in']) +
             if_none_get_zero(level_1['sub'][key1]['amount_in']))

        level_1['main'][key1]['amount_middle'] = \
            (if_none_get_zero(level_1['main'][key1]['amount_middle']) +
             if_none_get_zero(level_1['sub'][key1]['amount_middle']))

        level_1['main'][key1]['amount_out'] = \
            (if_none_get_zero(level_1['main'][key1]['amount_out']) +
             if_none_get_zero(level_1['sub'][key1]['amount_out']))
# 2
        level_2 = {
            'main': level_1['main'][key1].get('items', {}),
            'sub': level_1['sub'][key1].get('items', {}),
        }
        for key2 in level_2['main'].keys():
            level_2['main'][key2]['amount_in'] = \
                (if_none_get_zero(level_2['main'][key2]['amount_in']) +
                 if_none_get_zero(level_2['sub'][key2]['amount_in']))

            level_2['main'][key2]['amount_middle'] = \
                (if_none_get_zero(level_2['main'][key2]['amount_middle']) +
                 if_none_get_zero(level_2['sub'][key2]['amount_middle']))

            level_2['main'][key2]['amount_out'] = \
                (if_none_get_zero(level_2['main'][key2]['amount_out']) +
                 if_none_get_zero(level_2['sub'][key2]['amount_out']))

    return product_main


def enumeration_ingredients(product_id='15918a36-734e-4f59-820c-1cd6a33d4e77'):
    """ Перебор всех инредиентов. """
    ingredients: dict = {}
    ttk_main = TTK.objects.filter(product_id=product_id).first()
    if ttk_main == None:
        return {}
    ttk_child = TTK.objects.filter(parent_ttk=ttk_main)

    for ttk in ttk_child:
        add_ingredient(ttk, ingredients)
        ttk_child_2 = TTK.objects.filter(parent_ttk=ttk)
        for ttk in ttk_child_2:
            add_ingredient(ttk, ingredients)
            ttk_child_3 = TTK.objects.filter(parent_ttk=ttk)
            for ttk in ttk_child_3:
                add_ingredient(ttk, ingredients)
                ttk_child_4 = TTK.objects.filter(parent_ttk=ttk)
                for ttk in ttk_child_4:
                    add_ingredient(ttk, ingredients)
                    ttk_child_5 = TTK.objects.filter(parent_ttk=ttk)
                    for ttk in ttk_child_5:
                        add_ingredient(ttk, ingredients)
    return ingredients


def get_ingredient_category(ttk):
    try:
        category: dict = {
            'id': ttk.ingredient.groupId,
            'name': ttk.ingredient.category,
        }
    except Exception as e:
        category: dict = {
            'id': '0',
            'name': 'Отсутствует',
        }
        print(f'Ошибка {e}')
    return category

def enumeration_semifinisheds(product_id='15918a36-734e-4f59-820c-1cd6a33d4e77', count=1, categories_all=None):
    """
    Проходим по всем уровням ТТК
    """
    ttk_main = TTK.objects.filter(product_id=product_id).first()
    if not ttk_main:
        print(f'Для продукта с product_id {product_id} не существует TTK')
        return None, categories_all

    ttk_child = TTK.objects.filter(parent_ttk=ttk_main)

    semifinisheds: dict = {
            'name': ttk_main.name,
            'measure_unit': ttk_main.measure_unit,
            'amount_in': if_none_get_zero(ttk_main.amount_in) * count,
            'amount_middle': if_none_get_zero(ttk_main.amount_middle) * count,
            'amount_out': if_none_get_zero(ttk_main.amount_out) * count,
            'status': ttk_main.status,
            'items': {},

    }

    for ttk1 in ttk_child:
        category = get_ingredient_category(ttk1)
        if category not in categories_all:
            categories_all.append(category)

        level1 = semifinisheds['items']
        if ttk1.status == 'ingredient':
            continue

        level1[ttk1.product_id] = {
                'name': ttk1.name,
                'measure_unit': ttk1.measure_unit,
                'amount_in': if_none_get_zero(ttk1.amount_in) * count,
                'amount_middle': if_none_get_zero(ttk1.amount_middle) * count,
                'amount_out': if_none_get_zero(ttk1.amount_out) * count,
                'status': ttk1.status,
                'items': {},
                'category': category,
        }
        ttk_child_2 = TTK.objects.filter(parent_ttk=ttk1)
        for ttk2 in ttk_child_2:
            category = get_ingredient_category(ttk2)
            if category not in categories_all:
                categories_all.append(category)

            level2 = level1[ttk1.product_id]['items']
            level2[ttk2.product_id] = {
                'name': ttk2.name,
                'measure_unit': ttk2.measure_unit,
                'amount_in': if_none_get_zero(ttk2.amount_in) * count,
                'amount_middle': if_none_get_zero(ttk2.amount_middle) * count,
                'amount_out': if_none_get_zero(ttk2.amount_out) * count,
                'status': ttk2.status,
                'items': {},
                'category': category,
            }
            if ttk2.status == 'ingredient':
                continue
            ttk_child_3 = TTK.objects.filter(parent_ttk=ttk2)
            for ttk3 in ttk_child_3:
                category = get_ingredient_category(ttk3)
                if category not in categories_all:
                    categories_all.append(category)

                level3 = level2[ttk2.product_id]['items']
                level3[ttk3.product_id] = {
                    'name': ttk3.name,
                    'measure_unit': ttk3.measure_unit,
                    'amount_in': if_none_get_zero(ttk3.amount_in) * count,
                    'amount_middle': if_none_get_zero(ttk3.amount_middle) * count,
                    'amount_out': if_none_get_zero(ttk3.amount_out) * count,
                    'status': ttk3.status,
                    'items': {},
                    'category': category,
                }
                if ttk3.status == 'ingredient':
                    continue
                ttk_child_4 = TTK.objects.filter(parent_ttk=ttk3)
                for ttk4 in ttk_child_4:
                    category = get_ingredient_category(ttk4)
                    if category not in categories_all:
                        categories_all.append(category)

                    level4 = level3[ttk3.product_id]['items']
                    level4[ttk3.product_id] = {
                        'name': ttk4.name,
                        'measure_unit': ttk4.measure_unit,
                        'amount_in': if_none_get_zero(ttk4.amount_in) * count,
                        'amount_middle': if_none_get_zero(ttk4.amount_middle) * count,
                        'amount_out': if_none_get_zero(ttk4.amount_out) * count,
                        'status': ttk4.status,
                        'items': {},
                        'category': category,
                    }
                    if ttk4.status == 'ingredient':
                        continue
                    ttk_child_5 = TTK.objects.filter(parent_ttk=ttk4)
                    for ttk5 in ttk_child_5:
                        category = get_ingredient_category(ttk5)
                        if category not in categories_all:
                            categories_all.append(category)

                        level5 = level4[ttk4.product_id]['items']
                        level5[ttk5.product_id] = {
                            'name': ttk5.name,
                            'measure_unit': ttk5.measure_unit,
                            'amount_in': if_none_get_zero(ttk5.amount_in) * count,
                            'amount_middle': if_none_get_zero(ttk5.amount_middle) * count,
                            'amount_out': if_none_get_zero(ttk5.amount_out) * count,
                            'status': ttk5.status,
                            'items': {},
                            'category': category,
                        }
                        if ttk5.status == 'ingredient':
                            continue
    return semifinisheds, categories_all


def get_tree_ttk(product_id='15918a36-734e-4f59-820c-1cd6a33d4e77', count=1, categories_all=[]):
    """
    Проходим по всем уровням ТТК
    """
    ttk_main = TTK.objects.filter(product_id=product_id).first()
    if not ttk_main:
        print(f'Для продукта с product_id {product_id} не существует TTK')
        return None, categories_all

    ttk_child = TTK.objects.filter(parent_ttk=ttk_main)

    semifinisheds: dict = {
            'name': ttk_main.name,
            'measure_unit': ttk_main.measure_unit,
            'amount_in': if_none_get_zero(ttk_main.amount_in),
            'amount_middle': if_none_get_zero(ttk_main.amount_middle),
            'amount_out': if_none_get_zero(ttk_main.amount_out),
            'status': ttk_main.status,
            'items': {},

    }

    for ttk1 in ttk_child:
        level1 = semifinisheds['items']
        level1[ttk1.product_id] = {
                'name': ttk1.name,
                'measure_unit': ttk1.measure_unit,
                'amount_in': if_none_get_zero(ttk1.amount_in),
                'amount_middle': if_none_get_zero(ttk1.amount_middle),
                'amount_out': if_none_get_zero(ttk1.amount_out),
                'status': ttk1.status,
                'items': {},
        }
        ttk_child_2 = TTK.objects.filter(parent_ttk=ttk1)
        for ttk2 in ttk_child_2:
            level2 = level1[ttk1.product_id]['items']
            level2[ttk2.product_id] = {
                'name': ttk2.name,
                'measure_unit': ttk2.measure_unit,
                'amount_in': if_none_get_zero(ttk2.amount_in),
                'amount_middle': if_none_get_zero(ttk2.amount_middle),
                'amount_out': if_none_get_zero(ttk2.amount_out),
                'status': ttk2.status,
                'items': {},
            }
            ttk_child_3 = TTK.objects.filter(parent_ttk=ttk2)
            for ttk3 in ttk_child_3:
                level3 = level2[ttk2.product_id]['items']
                level3[ttk3.product_id] = {
                    'name': ttk3.name,
                    'measure_unit': ttk3.measure_unit,
                    'amount_in': if_none_get_zero(ttk3.amount_in),
                    'amount_middle': if_none_get_zero(ttk3.amount_middle),
                    'amount_out': if_none_get_zero(ttk3.amount_out),
                    'status': ttk3.status,
                    'items': {},
                }
                ttk_child_4 = TTK.objects.filter(parent_ttk=ttk3)
                for ttk4 in ttk_child_4:
                    level4 = level3[ttk3.product_id]['items']
                    level4[ttk3.product_id] = {
                        'name': ttk4.name,
                        'measure_unit': ttk4.measure_unit,
                        'amount_in': if_none_get_zero(ttk4.amount_in),
                        'amount_middle': if_none_get_zero(ttk4.amount_middle) * c,
                        'amount_out': if_none_get_zero(ttk4.amount_out),
                        'status': ttk4.status,
                        'items': {},
                    }
                    ttk_child_5 = TTK.objects.filter(parent_ttk=ttk4)
                    for ttk5 in ttk_child_5:
                        level5 = level4[ttk4.product_id]['items']
                        level5[ttk5.product_id] = {
                            'name': ttk5.name,
                            'measure_unit': ttk5.measure_unit,
                            'amount_in': if_none_get_zero(ttk5.amount_in),
                            'amount_middle': if_none_get_zero(ttk5.amount_middle),
                            'amount_out': if_none_get_zero(ttk5.amount_out),
                            'status': ttk5.status,
                            'items': {},
                        }
    return semifinisheds, categories_all


def write_ttk_in_bd():
    """
    Записывает ТТК в базу данных.
    from nutritionist.functions.ttk import write_ttk_in_bd
    write_ttk_in_bd()
    """
    TTK.objects.all().delete()
    category = 'салат'
    products = ProductLp.objects.all()
    count = products.count()
    for i, product in enumerate(products):
        print(f'блюдо {i+1}, из {count}, {product.name}, {product.product_id}')
        if product.product_id:
            create_all_ttk(product.product_id)
        else:
            print('Ошибка', product.product_id)

    add_status()