def formation_menu(products):
    breakfast = {}
    breakfast['products_garnish'] = list(products.filter(category='гарнир'))
    breakfast['products_main'] = list(products.filter(category='основной'))
    breakfast['products_porridge'] = list(products.filter(category='каша'))

    afternoon = {}
    afternoon['products_main'] = list(products.filter(category='основной'))
    afternoon['products_dessert'] = list(products.filter(category='десерт'))
    afternoon['products_fruit'] = list(products.filter(category='фрукты'))
    afternoon['products_drink'] = list(products.filter(category='напиток'))

    lunch = {}
    lunch['products_main'] = list(products.filter(category='основной'))
    lunch['products_garnish'] = list(products.filter(category='гарнир'))
    lunch['products_salad'] = list(products.filter(category='салат'))
    lunch['products_soup'] = list(products.filter(category='суп'))
    lunch['products_drink'] = list(products.filter(category='напиток'))

    dinner = {}
    dinner['products_main'] = list(products.filter(category='основной'))
    dinner['products_garnish'] = list(products.filter(category='гарнир'))
    dinner['products_drink'] = list(products.filter(category='напиток'))

    return breakfast, afternoon, lunch, dinner
