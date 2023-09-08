""" Модуль по API получает ТТК и из ингридиентов собирает состав блюда. """
from doctor.functions.download import get_tk, get_name_by_api, get_ingredients
from nutritionist.models import Ingredient
from django.db import transaction

from nutritionist.models import ProductLp


def get_ttk(id):
    """ Получаем ТТК до 5ого уровня """
    import operator
    tk, error = get_tk(id)

    for item_tk_1 in tk['assemblyCharts']:
        try:
            item_tk_1['name'] = Ingredient.objects.filter(product_id=item_tk_1['assembledProductId']).first().name
        except:
            item_tk_1['name'] = get_name_by_api(item_tk_1['assembledProductId'])
# уровень 2
        for item_tk_2 in item_tk_1['items']:
            try:
                item_tk_2['name'] = Ingredient.objects.filter(product_id=item_tk_2['productId']).first().name
            except:
                item_tk_2['name'] = get_name_by_api(item_tk_2['productId'])
            # получить список ингридиентов для каждого item_tk_2
            try:
                item_tk_2['item'] = get_ingredients(item_tk_2['productId'], item_tk_2['name'])
            except:
                item_tk_2['item'] = None
# уровень 3
#             for item_tk_3 in item_tk_2.get('items', []):
#                 try:
#                     item_tk_3['name'] = Ingredient.objects.filter(product_id=item_tk_3['productId']).first().name
#                 except:
#                     item_tk_3['name'] = get_name(item_tk_3['productId'])


    result = tk['assemblyCharts'][0]

    for ing in result['items']:
        for ing2 in tk['assemblyCharts'][1:]:
            try:
                if ing['productId'] == ing2['assembledProductId']:
                    ing['items'] = ing2['items'].copy()
                    # уровень 3
                    for ing3 in ing['items']:
                        try:
                            ing3['items'] = get_ingredients(ing3['productId'], ing3['name'])

                            for ing4 in ing3['items']:
                                try:
                                    ing4['name'] = Ingredient.objects.filter(
                                        product_id=ing4['productId']).first().name
                                except:
                                    ing4['name'] = get_name_by_api(ing4['productId'])
                                try:
                                    ing4['items'] = get_ingredients(ing4['productId'], ing4['name'])
                                    for ing5 in ing4['items']:
                                        try:
                                            ing5['name'] = Ingredient.objects.filter(
                                                product_id=ing5['productId']).first().name
                                        except:
                                            ing5['name'] = get_name_by_api(ing5['productId'])
                                except:
                                    ing4['items'] = None
                        except:
                            ing3['items'] = None
            except:
                pass
        if 'items' not in ing:
            ing['items'] = None
    return result


def create_composition_from_ttk(ttk):
    """ Из ингредиентов ТТК формируем состав блюда. """

    def recorsion(items, is_one=False):
        composition: str = ""
        for item_l in items:
            items_l = item_l.get('items', [])
            if items_l in [None, '', ]:
                items_l = []
            if len(items_l) >= 2:
                composition += item_l.get('name', 'XXX')
                composition += recorsion(items_l.copy())
            elif len(items_l) == 1:
                composition += recorsion(items_l.copy(), is_one=True)
            else:
                composition += item_l.get('name', 'XXX')
                composition += ', '
        if is_one:
            return f' {composition.strip(", ")}, '
        else:
            return f' ({composition.strip(", ")}), '

    composition: str = ""
    for item in ttk['items']:
        items = item.get('items', [])
        if items in [None, '']:
            items = []
        if len(items) >= 2:
            composition += item.get('name', 'XXX')
            composition += recorsion(items.copy())
        elif len(items) == 1:
            composition += recorsion(items.copy(), is_one=True)
        else:
            composition += item.get('name', 'XXX')
            composition += ', '
    composition = composition.replace('  ', ' '). \
                              replace(' ,', ','). \
                              replace('  ,', ','). \
                              replace(' п/ф', ''). \
                              replace('п/ф', ''). \
                              replace(' п/ф', ''). \
                              replace('с/м', ''). \
                              replace(' с/м', ''). \
                              replace('с/с', ''). \
                              replace(' с/с', ''). \
                              replace(' зам.', ''). \
                              replace(' очищ.', ''). \
                              replace(' пост', ''). \
                              replace('(продукт полутвердый)', ''). \
                              strip().strip(',').capitalize()
    return composition

def description_parsing(id):
    """ По product_id парсим состав блюда """
    try:
        ttk = get_ttk(id)
        compileall = create_composition_from_ttk(ttk)
    except:
        compileall = "Отсутствует"
    return compileall


@transaction.atomic
def update_product_description():
    """
    Обновляет состав продукта в ProductLp.
    """
    products = ProductLp.objects.all()
    for i, p in enumerate(products):
        if p.product_id:
            description = description_parsing(p.product_id)
            print(f'{i}. {p.name}, {description}')
            p.description = description

    ProductLp.objects.bulk_update(products, ['description', ])