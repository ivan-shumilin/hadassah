from nutritionist.functions.ttk import enumeration_ingredients, add_ingredient_for_dict, enumeration_semifinisheds, \
    merger_products


def get_ingredients(catalog):
    """
    Составляем список всех ингредиетов в заказе.
    """
    ingredients: dict = {}

    for meal in ['breakfast', 'lunch', 'afternoon', 'dinner']:
        for category in ['porridge', 'salad', 'soup', 'main', 'garnish', 'dessert', 'fruit', 'drink', 'products']:
            for product in catalog[meal][category]:
                if product:
                    if product.get('product_id', None):
                        sub_ingredients: dict = enumeration_ingredients(product['product_id'])
                    else:
                        print(f'нет product_id, {product["name"]}')
                    # добавляем sub_ingredients в ingredients
                    for sub_ingredient in sub_ingredients.items():
                        add_ingredient_for_dict(sub_ingredient, ingredients)
    return ingredients


def get_semifinished(catalog: dict) -> dict:
    """
    Составляем список всех п/ф в заказе.
    """
    semifinisheds: dict = {}

    for meal in ['breakfast', 'lunch', 'afternoon', 'dinner']:
        for category in ['porridge', 'salad', 'soup', 'main', 'garnish', 'dessert', 'fruit', 'drink', 'products']:
            for product in catalog[meal][category]:
                if product:
                    if product.get('product_id', None):
                        semifinisheds[product['product_id']]: dict = enumeration_semifinisheds(
                            product['product_id'],
                            int(product['count']),
                        )
                    else:
                        try:
                            print(f'нет product_id, {product["name"]}')
                        except:
                            print(f'нет product_id и name {product}')
    return semifinisheds


def get_semifinished_level_1(semifinished_level_0: dict) -> dict:
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

dict = {
    'level1': [
        {
            'product_id': {
                'name': 'name',
                'more': 'more',
                'items': [
                    {
                        'product_id': {
                            'name': 'name',
                            'more': 'more',
                            'items': [],
                        }
                    },
                ]
            }
        },
    ],
    'no_ttk': []
}