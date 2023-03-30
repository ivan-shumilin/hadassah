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

    for meal in ['breakfast', 'lunch', 'afternoon', 'dinner']:
        # if check_is_comment(user):
        #     products_cafe: tuple = [], [], [], []
        # else:
        products_cafe: tuple = creating_meal_menu_cafe(date_get, diet, meal)
        products_lp = ProductLp.objects.filter(Q(timetablelp__day_of_the_week=day_of_the_week) &
                                            Q(timetablelp__type_of_diet=translated_diet) &
                                            Q(timetablelp__meals=meal))

        menu[meal] = {'cafe': {
                    'main': products_cafe[0],
                    'garnish': products_cafe[1],
                    'salad': products_cafe[2],
                    'soup': products_cafe[3]
                }}

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
    return menu


def create_category(value):
    main = ''
    garnish = ''
    porridge = ''
    soup = ''
    dessert = ''
    fruit = ''
    drink = ''
    salad = ''
    for item in value:
        list_item = item.split('-')
        if 'main' in list_item:
            if list_item[0] == 'lp':
                main = list_item[2]
            else:
                main = 'cafe-main-' + list_item[2]

        if 'garnish' in list_item:
            if list_item[0] == 'lp':
                garnish = list_item[2]
            else:
                garnish = 'cafe-garnish-' + list_item[2]

        if 'porridge' in list_item:
            if list_item[0] == 'lp':
                porridge = list_item[2]
            else:
                porridge = 'cafe-porridge-' + list_item[2]

        if 'soup' in list_item:
            if list_item[0] == 'lp':
                soup = list_item[2]
            else:
                soup = 'cafe-soup-' + list_item[2]

        if 'dessert' in list_item:
            if list_item[0] == 'lp':
                dessert = list_item[2]
            else:
                dessert = 'cafe-dessert-' + list_item[2]

        if 'fruit' in list_item:
            if list_item[0] == 'lp':
                fruit = list_item[2]
            else:
                fruit = 'cafe-fruit-' + list_item[2]

        if 'drink' in list_item:
            if list_item[0] == 'lp':
                drink = list_item[2]
            else:
                drink = 'cafe-drink-' + list_item[2]

        if 'salad' in list_item:
            if list_item[0] == 'lp':
                salad = list_item[2]
            else:
                salad = 'cafe-salad-' + list_item[2]
    return main, garnish, porridge, soup, dessert, fruit, drink, salad


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
        patient_select[meal] = {
            'main': menu_item.main,
            'garnish': menu_item.garnish,
            'porridge': menu_item.porridge,
            'soup': menu_item.soup,
            'dessert': menu_item.dessert,
            'fruit': menu_item.fruit,
            'drink': menu_item.drink,
            'salad': menu_item.salad,
        }
# сделаем из словаря список
    patient_select_list = []
    for key in patient_select.keys():

        for key2 in patient_select[key].keys():
            if patient_select[key][key2] != None:
                if patient_select[key][key2] != '' and 'cafe' in patient_select[key][key2]:
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
        if count_product_without_garnish == 0:
            menu_for_lk_patient[meal]['cafe']['garnish'] = []
    return menu_for_lk_patient