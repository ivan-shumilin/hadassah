from nutritionist.models import ProductLp, CustomUser, MenuByDay, Product
from typing import List
from datetime import datetime, date, timedelta
from django.utils import dateformat
from django.db.models.functions import Lower
from doctor.functions.functions import creating_meal_menu_cafe
from dateutil.parser import parse
from django.db.models import Q


def formation_menu(products):
    breakfast = {}
    breakfast['products_salad'] = list(products.filter(category='салат'))
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


def creates_dict_with_menu_patients_for_patient(user):
    menu_lp = ProductLp.objects.filter(Q(timetablelp__day_of_the_week=day_of_the_week) &
                                        Q(timetablelp__type_of_diet=translated_diet) &
                                        Q(timetablelp__meals=meal))
    menu_cafe = Product.objects.filter(Q(timetablelp__day_of_the_week=day_of_the_week) &
                                        Q(timetablelp__type_of_diet=translated_diet) &
                                        Q(timetablelp__meals=meal))
    menu = {}
    # day_date = {
    #     'today': str(date.today()),
    #     'tomorrow': str(date.today() + timedelta(days=1)),
    #     'day_after_tomorrow': str(date.today() + timedelta(days=2)),
    # }
    # for day, date_str in day_date.items():
    #     menu[day] = {}
    #     for meal in ['breakfast', 'lunch', 'afternoon', 'dinner']:
    #         menu[day][meal] = {
    #             'main': check_value_two(menu_all, date_str, meal, "main"),
    #             'garnish': check_value_two(menu_all, date_str, meal, "garnish"),
    #             'porridge': check_value_two(menu_all, date_str, meal, "porridge"),
    #             'soup': check_value_two(menu_all, date_str, meal, "soup"),
    #             'dessert': check_value_two(menu_all, date_str, meal, "dessert"),
    #             'fruit': check_value_two(menu_all, date_str, meal, "fruit"),
    #             'drink': check_value_two(menu_all, date_str, meal, "drink"),
    #             'salad': check_value_two(menu_all, date_str, meal, "salad"),
    #         }
    #     menu[day]['date_human_style'] = dateformat.format(date.fromisoformat(date_str), 'd E, l')
    return menu


def create_dict_products_lp(products_lp_category):
    list_with_products = []
    excluded_product = ['458']  # Вода "Jеvea" 0,51л.
    for item in products_lp_category:
        if not str(item.id) in excluded_product:
            # list_with_products.append({
            #     'id': item.id,
            #     'name': item.public_name,
            #     'carbohydrate': item.carbohydrate,
            #     'fat': item.fat,
            #     'fiber': item.fiber,
            #     'energy': item.energy,
            #     'image': item.image,
            #     'description': item.description,
            #     'category': item.category,
            #     'with_garnis': item.with_garnis
            # })
            list_with_products.append(item)
    return list_with_products


def creating_menu_for_patient(date_get, diet, day_of_the_week, translated_diet, user):
    """Создаем словарь со всеми вариантами блюд для пациента, и с отмеченными блюдами
        которые выбрал пациент.
    """
    menu = {}
    fix_dishes = []

    for meal in ['breakfast', 'lunch', 'afternoon', 'dinner']:
        # if check_is_comment(user):
        #     products_cafe: tuple = [], [], [], []
        # else:
        products_cafe: list = list(creating_meal_menu_cafe(date_get, diet, meal))
        cat_index = {
            'main': 0,
            'garnish': 1,
            'salad': 2,
            'soup': 3,
            'porridge': 5,
            'main-breakfast': 4,
            'dessert': 6,
        }

        products_menu_cafe: dict = {}
        products_add_lp: list = []
        menu_lp = MenuByDay.objects.filter(date=date_get, user_id=user, meal=meal).first()
        catergorys = ['salad', 'soup', 'main', 'garnish', 'porridge', 'dessert', 'fruit',]

        category_translation = {
            'salad': 'салат',
            'soup': 'суп',
            'main': 'основной',
            'garnish': 'гарнир',
            'porridge': 'каша',
            'dessert': 'десерт',
            'fruit': 'фрукты',
        }


        excluded_categories_for_lp: list = []
        excluded_categories_for_cafe: list = []
        # 'bouillon',
        for cat in catergorys:
            id_set = getattr(menu_lp, cat, None)
            if id_set:
                id_set = id_set.strip(',').split(',')
                if len(id_set) > 0:
                    for id in id_set:
                        if 'cafe' in id:
                            product = Product.objects.get(id=id.split('-')[2])
                            products_menu_cafe[cat] = product
                        else:
                            if id != '':
                                products_add_lp.append(id)
                if len(id_set) > 1:
                    excluded_categories_for_lp.append(category_translation[cat])
                    excluded_categories_for_cafe.append(cat)
                    if meal == 'breakfast':
                        if cat == 'main':
                            products_cafe[cat_index['main-breakfast']] = []
                    else:
                        if cat != 'fruit':
                            products_cafe[cat_index[cat]] = []
                    for id in id_set:
                        if 'cafe' in id:
                            fix_dishes.append(id)
                        else:
                            fix_dishes.append(f'lp-{cat}-{id}')


            else:
            # если в этой категории нет блюд, тогда нужно исключить ее
            # из products_lp и products_cafe
                excluded_categories_for_lp.append(category_translation[cat])
                excluded_categories_for_cafe.append(cat)

        # products_lp = ProductLp.objects.filter(id__in=products_lp)


        products_lp = ProductLp.objects.filter(
            Q(timetablelp__day_of_the_week=day_of_the_week) &
            Q(timetablelp__type_of_diet=translated_diet) &
            Q(timetablelp__meals=meal) &
            ~Q(category__in=excluded_categories_for_lp) |
            Q(id__in=products_add_lp)
        ).distinct()



        # cформировать лист с id продуктов
        menu_cafe: dict = {}
        catergorys_cafe = [cat for cat in ['main', 'garnish', 'salad', 'soup', 'porridge'] if cat not in excluded_categories_for_cafe]
        # catergorys_cafe = ['main', 'garnish', 'salad', 'soup', 'porridge']
        for cat in catergorys_cafe:
            product = products_menu_cafe.get(cat, None)
            if product:
                menu_cafe[cat] = [product]
            else:
                menu_cafe[cat] = []

        menu[meal] = {'cafe': {
                    'main': list(set(products_cafe[0] + menu_cafe.get('main', []))),
                    'garnish': list(set(products_cafe[1] + menu_cafe.get('garnish', []))),
                    'salad': list(set(products_cafe[2] + menu_cafe.get('salad', []))),
                    'soup': list(set(products_cafe[3] + menu_cafe.get('soup', []))),
                    'porridge': list(set(products_cafe[5] + menu_cafe.get('porridge', []))),
                }}

        if meal == 'breakfast':
            menu[meal]['cafe']['main'] = list(set(products_cafe[4] + menu_cafe.get('main', [])))

        menu[meal].update({'lp': {
            'porridge': create_dict_products_lp(list(products_lp.filter(category='каша'))),
            'salad': create_dict_products_lp(list(products_lp.filter(category='салат'))),
            'soup': create_dict_products_lp(list(products_lp.filter(category='суп'))),
            'main': create_dict_products_lp(list(products_lp.filter(category='основной'))),
            'garnish': create_dict_products_lp(list(products_lp.filter(category='гарнир'))),
            'dessert': create_dict_products_lp(list(products_lp.filter(category='десерт'))),
            'fruit': create_dict_products_lp(list(products_lp.filter(category='фрукты'))),
            'drink': create_dict_products_lp(list(products_lp.filter(category='напиток')))
        }})
    return menu, fix_dishes


def create_category(value):
    category = {
        "main": '',
        "garnish": '',
        "porridge": '',
        "soup": '',
        "dessert": '',
        "fruit": '',
        "drink": '',
        "salad": '',
    }

    category_lp_trans = {
        "гарнир": "garnish",
        "десерт": "dessert",
        "каша": "porridge",
        "напиток": "drink",
        "основной": "main",
        "салат": "salad",
        "суп": "soup",
        "фрукты": "fruit",
    }

    salad = ["Салаты"]
    soup = ["Первые блюда"]
    porridge = ["Каши"]
    main = ["Завтраки", "Вторые блюда", "Блюда от шефа"]
    garnish = ["Гарниры"]

    for item in value:
        list_item = item.split('-')
        # if 'main' in list_item:
        #     if list_item[0] == 'lp':
        #         main = list_item[2]
        #     else:
        #         main = 'cafe-change-' + list_item[2]
        #
        # if 'garnish' in list_item:
        #     if list_item[0] == 'lp':
        #         garnish = list_item[2]
        #     else:
        #         garnish = 'cafe-change-' + list_item[2]
        #
        # if 'porridge' in list_item:
        #     if list_item[0] == 'lp':
        #         porridge = list_item[2]
        #     else:
        #         porridge = 'cafe-change-' + list_item[2]
        #
        # if 'soup' in list_item:
        #     if list_item[0] == 'lp':
        #         soup = list_item[2]
        #     else:
        #         soup = 'cafe-salad-' + list_item[2]
        #
        # if 'dessert' in list_item:
        #     if list_item[0] == 'lp':
        #         dessert = list_item[2]
        #     else:
        #         dessert = 'cafe-change-' + list_item[2]
        #
        # if 'fruit' in list_item:
        #     if list_item[0] == 'lp':
        #         fruit = list_item[2]
        #     else:
        #         fruit = 'cafe-change-' + list_item[2]
        #
        # if 'drink' in list_item:
        #     if list_item[0] == 'lp':
        #         drink = list_item[2]
        #     else:
        #         drink = 'cafe-change-' + list_item[2]
        #
        # if 'salad' in list_item:
        #     if list_item[0] == 'lp':
        #         salad = list_item[2]
        #     else:
        #         salad = 'cafe-change-' + list_item[2]
        if list_item[0] == 'lp':
            id = list_item[2]
            category_name = ProductLp.objects.get(id=id).category
            category_name = category_lp_trans[category_name]
            # category[category_name] = id
            category[category_name] = category[category_name].split(',')
            if '' in category[category_name]:
                category[category_name].remove('')
            category[category_name].append(id)
            category[category_name] = ','.join(category[category_name])
            category[category_name].split(',')
        else:
            id = list_item[2]
            category_name = Product.objects.get(id=id).category
            if category_name in salad:
                category_name = "salad"
            elif category_name in soup:
                category_name = "soup"
            elif category_name in porridge:
                category_name = "porridge"
            elif category_name in main:
                category_name = "main"
            elif category_name in garnish:
                category_name = "garnish"
            category[category_name] = 'cafe-change-' + id

    return category


def create_patient_select(id, date_get):
    menu = MenuByDay.objects.filter(user_id=id)
    menu = menu.filter(date=date_get)
    if not menu:
        return ''

    patient_select = {}
    for meal in ['breakfast', 'lunch', 'afternoon', 'dinner']:
        try:
            menu_item = menu.get(meal=meal)
        except:
            continue

        try:
            main = 'cafe-change-' + menu_item.main.split("-")[2] if "cafe" in menu_item.main else 'lp-main-' + menu_item.main
        except:
            main = 'cafe-change-'

        try:
            garnish = 'cafe-change-' + menu_item.garnish.split("-")[2] if "cafe" in menu_item.garnish else 'lp-garnish-' + menu_item.garnish
        except:
            garnish = 'cafe-change-'

        try:
            porridge = 'cafe-change-' + menu_item.porridge.split("-")[2] if "cafe" in menu_item.porridge else 'lp-porridge-' + menu_item.porridge
        except:
            porridge = 'cafe-change-'

        try:
            soup = 'cafe-change-' + menu_item.soup.split("-")[2] if "cafe" in menu_item.soup else 'lp-soup-' + menu_item.soup
        except:
            soup = 'cafe-change-'

        try:
            dessert = 'cafe-change-' + menu_item.dessert.split("-")[2] if "cafe" in menu_item.dessert else 'lp-dessert-' + menu_item.dessert
        except:
            dessert = 'cafe-change-'

        try:
            fruit = 'cafe-change-' + menu_item.fruit.split("-")[2] if "cafe" in menu_item.fruit else 'lp-fruit-' + menu_item.fruit
        except:
            fruit = 'cafe-change-'

        try:
            drink = 'cafe-change-' + menu_item.drink.split("-")[2] if "cafe" in menu_item.drink else 'lp-drink-' + menu_item.drink
        except:
            drink = 'cafe-change-'

        try:
            salad = 'cafe-change-' + menu_item.salad.split("-")[2] if "cafe" in menu_item.salad else 'lp-salad-' + menu_item.salad
        except:
            salad = 'cafe-change-'

        patient_select[meal] = {
            'main': main if main != 'lp-main-' else None,
            'garnish': garnish if garnish != 'lp-garnish-' else None,
            'porridge': porridge if porridge != 'lp-porridge-' else None,
            'soup': soup if soup != 'lp-soup-' else None,
            'dessert': dessert if dessert != 'lp-dessert-' else None,
            'fruit': fruit if fruit != 'lp-fruit-' else None,
            'drink': drink if drink != 'lp-drink-' else None,
            'salad': salad if salad != 'lp-salad-' else None,
        }
# сделаем из словаря список
    patient_select_list = []
    for key in patient_select.keys():

        for key2 in patient_select[key].keys():
            if patient_select[key][key2] != None:
                if patient_select[key][key2] != '':
                    # if patient_select[key][key2] != '' and 'cafe' in patient_select[key][key2]:
                    patient_select_list.append(patient_select[key][key2])

    return ','.join(patient_select_list)


def date_menu_history(id, user):
    days = [date.today() - timedelta(days=delta + 1) for delta in range((date.today() - user.receipt_date).days)]
    days_history = []
    for day in days:
        days_history.append({'number': str(day), 'word': dateformat.format(day, 'd E, l')})
    return days_history

def check_is_comment(patient):
    if len(patient.comment) >= 2 or \
        patient.is_probe or \
        patient.is_without_salt or \
        patient.is_without_lactose or \
        patient.is_pureed_nutrition:
        return True
    return False


def del_if_not_garnish(menu_for_lk_patient):
    """
     Если нет гарнира на выбор, тогда удаляем все блюда без
     гарнира, тк не будет возможности выбрать гарнир.
    """
    for meal in ['lunch', 'dinner']:
        count_garnish = \
            len(menu_for_lk_patient[meal]['lp']['garnish'] + menu_for_lk_patient[meal]['cafe']['garnish'])
        if count_garnish == 0:
            menu_for_lk_patient[meal]['lp']['main'] = \
                [product for product in menu_for_lk_patient[meal]['lp']['main'] if product.with_garnish]
            menu_for_lk_patient[meal]['cafe']['main'] = \
                [product for product in menu_for_lk_patient[meal]['cafe']['main'] if product.with_garnish]
    return menu_for_lk_patient

def del_if_not_product_without_garnish(menu_for_lk_patient):
    """
    Если нет основных блюд для которых требуется гарнир, тогда удаляем гарниры.
    Но только из дополнительных гарниров (cafe)
    """
    for meal in ['lunch', 'dinner']:
        count_product_without_garnish = \
            len([product for product in menu_for_lk_patient[meal]['lp']['main'] if not product.with_garnish] + \
                [product for product in menu_for_lk_patient[meal]['cafe']['main'] if not product.with_garnish])
        count_product_main = \
            len([product for product in menu_for_lk_patient[meal]['lp']['main']] + \
                [product for product in menu_for_lk_patient[meal]['cafe']['main']])
        if count_product_without_garnish == 0 and count_product_main > 0:
            menu_for_lk_patient[meal]['cafe']['garnish'] = []
    return menu_for_lk_patient