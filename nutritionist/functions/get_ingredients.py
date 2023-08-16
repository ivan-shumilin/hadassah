from nutritionist.functions.ttk import enumeration_ingredients, add_ingredient_for_dict


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

