from nutritionist.models import ProductLp, CustomUser, MenuByDay, Product
from django.db import transaction
from dateutil.parser import parse
from django.db.models import Q
from typing import List
from datetime import datetime, date, timedelta
from django.utils import dateformat
from django.db.models.functions import Lower

def sorting_dishes(meal, queryset_main_dishes, queryset_garnish, queryset_salad, queryset_soup):
    """Сортировка блюд по приемам пищи"""

    if meal == 'breakfast':
        return [], [], [], []
    if meal == 'afternoon':
        return [], [], [], []
    if meal == 'lunch':
        if len(queryset_main_dishes) == 0:
            queryset_main_dishes = []
        if len(queryset_garnish) == 0:
            queryset_garnish = []
        if len(queryset_salad) == 0:
            queryset_salad = []
        if len(queryset_soup) == 0:
            queryset_soup = []

        if len(queryset_main_dishes) == 1 or len(queryset_main_dishes) == 2:
            queryset_main_dishes = queryset_main_dishes[0:1]
        if len(queryset_garnish) == 1 or len(queryset_garnish) == 2:
            queryset_garnish = queryset_garnish[0:1]
        if len(queryset_salad) == 1 or len(queryset_salad) == 2:
            queryset_salad = queryset_salad[0:1]
        if len(queryset_soup) == 1 or len(queryset_soup) == 2:
            queryset_soup = queryset_soup[0:1]

        if len(queryset_main_dishes) >= 3:
            queryset_main_dishes = queryset_main_dishes[0:2]
        if len(queryset_garnish) >= 3:
            queryset_garnish = queryset_garnish[0:2]
        if len(queryset_salad) >= 3:
            queryset_salad = queryset_salad[0:2]
        if len(queryset_soup) >= 3:
            queryset_soup = queryset_soup[0:2]

    if meal == 'dinner':
        queryset_salad = queryset_soup = []

        if len(queryset_main_dishes) <= 1:
            queryset_main_dishes = []
        if len(queryset_garnish) <= 1:
            queryset_garnish = []


        if len(queryset_main_dishes) == 2:
            queryset_main_dishes = queryset_main_dishes[1:2]
        if len(queryset_garnish) == 2:
            queryset_garnish = queryset_garnish[1:2]


        if len(queryset_main_dishes) == 3:
            queryset_main_dishes = queryset_main_dishes[2:3]
        if len(queryset_garnish) == 3:
            queryset_garnish = queryset_garnish[2:3]


        if len(queryset_main_dishes) >= 4:
            queryset_main_dishes = queryset_main_dishes[2:4]
        if len(queryset_garnish) >= 3:
            queryset_garnish = queryset_garnish[2:4]

    return queryset_main_dishes, queryset_garnish, queryset_salad, queryset_soup


def parsing():
    import fake_useragent
    import requests
    from bs4 import BeautifulSoup
    import pickle

    with open('doctor/html/drinks.html', 'rb') as input_file:
        data = input_file.read()

    menu = {}
    soup = BeautifulSoup(data, 'lxml')
    soup_table = soup.find_all('table')

    for table in soup_table:
        name_all = table.find_all('td', class_="sa2fc3875")
        for name in name_all:
            if not name.get_text():
                continue
            else:
                menu[name.get_text()] = {}
                desc_list = []
                desc_all = table.find_all('td', class_="s76dce60f")
                for desc_item in desc_all:
                    if not desc_item.text:
                        continue
                    else:
                        desc_list.append(desc_item.text)
                desc = ', '.join(desc_list)
                desc = desc.lower()
                desc = desc.capitalize()
                desc = desc + '.'
                cffe = table.find_all('td', class_="s4502787a")
                try:
                    energy = cffe[7].text
                except Exception:
                    energy = '0'

                try:
                    carbohydrate = cffe[4].text
                except Exception:
                    carbohydrate = '0'

                try:
                    fat = cffe[5].text
                except Exception:
                    fat = '0'

                try:
                    fiber = cffe[6].text
                except Exception:
                    fiber = '0'
                menu[name.get_text()] = {'descriptions': desc,
                                         'carbohydrate': carbohydrate,
                                         'fat': fat,
                                         'fiber': fiber,
                                         'energy': energy,
                                         'category': 'напиток',

                                         }
    load_menu(menu)


@transaction.atomic
def load_menu(menu):
    menu_items = menu
    to_create = []
    for menu_item in menu_items:
        to_create.append(ProductLp(
            name=menu_item,
            description=menu_items[menu_item]['descriptions'],
            carbohydrate=menu_items[menu_item]['carbohydrate'],
            fat=menu_items[menu_item]['fat'],
            fiber=menu_items[menu_item]['fiber'],
            energy=menu_items[menu_item]['energy'],
            category=menu_items[menu_item]['category'],


    ))
    ProductLp.objects.bulk_create(to_create)


def get_day_of_the_week(date_get):
    '''Дату в формате Y-M-D в день недели прописью'''
    DAT_OF_THE_WEEK = {
        'Monday': 'понедельник',
        'Tuesday': 'вторник',
        'Wednesday': 'среда',
        'Thursday': 'четверг',
        'Friday': 'пятница',
        'Saturday': 'суббота',
        'Sunday': 'воскресенье',
    }
    return DAT_OF_THE_WEEK[parse(date_get).strftime('%A')]


def translate_diet(diet):
    TYPE_DIET = {
        'ovd': 'ОВД',
        'ovd_sugarless': 'ОВД без сахара',
        'shd': 'ЩД',
        'bd': 'БД',
        'vbd': 'ВБД',
        'nbd': 'НБД',
        'nkd': 'НКД',
        'vkd': 'ВКД',
        'ОВД': 'ovd',
        'ОВД без сахара': 'ovd_sugarless',
        'ЩД': 'shd',
        'БД': 'bd',
        'ВБД': 'vbd',
        'НБД': 'nbd',
        'НКД': 'nkd',
        'ВКД': 'vkd',
    }
    return TYPE_DIET[diet]


def сhange_password(email, request):
    user = CustomUser.objects.get(id=request.user.id)
    user.email = email
    user.save()
    return

# formset[0].initial['full_name']
def formatting_full_name(full_name):
    list = full_name.split()
    res = ''
    for index, value in enumerate(list):
        print(index, len(list))
        if index == 0:
            res += value.capitalize() + ' '
            continue
        if index == len(list) - 1:
            res += value[0:1].capitalize()
            continue
        else:
            res += value[0:1].capitalize() + '.'
    return res

def check_value(category, products):
    value: str = ''
    try:
        value = products.get(category=category).id
        value = 'lp-' + str(value)
    except Exception:
        value = None
    return value

def check_value_(menu_all, date_str, meal, category):
    try:
        id = menu_all.filter(date=date_str).get(meal=meal).main
        if 'cafe' in id:
            product = Product.objects.get(id=id.split('-')[2])
        else:
            product = ProductLp.objects.get(id=id)
        value = {
            'id': id,
            'name': product.name,
            'carbohydrate': product.carbohydrate,
            'fat': product.fat,
            'fiber': product.fiber,
            'energy': product.energy,
            'image': product.image,
            'description': product.description,
            'category': product.category,
        }
    except Exception:
        value = None
    return value

def create_value(product, id):
    value: str = ''
    value = {
        'id': id,
        'name': product.name,
        'carbohydrate': round(float(product.carbohydrate), 1),
        'fat': round(float(product.fat), 1),
        'fiber': round(float(product.fiber), 1),
        'energy': round(float(product.energy), 1),
        'image': product.image,
        'description': product.description,
        'category': product.category,
    }
    return value



def check_value_two(menu_all, date_str, meal, category):
    value: str = ''
    if category == 'main':
        try:
            id = menu_all.filter(date=date_str).get(meal=meal).main
            if id == '':
                return None
            if 'cafe' in id:
                product = Product.objects.get(id=id.split('-')[2])
            else:
                product = ProductLp.objects.get(id=id)
            value = create_value(product, id)
        except Exception:
            value = None
        return value
    if category == 'garnish':
        try:
            id = menu_all.filter(date=date_str).get(meal=meal).garnish
            if id == '':
                return None
            if 'cafe' in id:
                product = Product.objects.get(id=id.split('-')[2])
            else:
                product = ProductLp.objects.get(id=id)
            value = create_value(product, id)
        except Exception:
            value = None
        return value
    if category == 'porridge':
        try:
            id = menu_all.filter(date=date_str).get(meal=meal).porridge
            if id == '':
                return None
            if 'cafe' in id:
                product = Product.objects.get(id=id.split('-')[2])
            else:
                product = ProductLp.objects.get(id=id)
            value = create_value(product, id)
        except Exception:
            value = None
        return value
    if category == 'soup':
        try:
            id = menu_all.filter(date=date_str).get(meal=meal).soup
            if id == '':
                return None
            if 'cafe' in id:
                product = Product.objects.get(id=id.split('-')[2])
            else:
                product = ProductLp.objects.get(id=id)
                value = create_value(product, id)
        except Exception:
            value = None
        return value
    if category == 'dessert':
        try:
            id = menu_all.filter(date=date_str).get(meal=meal).dessert
            if id == '':
                return None
            if 'cafe' in id:
                product = Product.objects.get(id=id.split('-')[2])
            else:
                product = ProductLp.objects.get(id=id)
                value = create_value(product, id)
        except Exception:
            value = None
        return value
    if category == 'fruit':
        try:
            id = menu_all.filter(date=date_str).get(meal=meal).fruit
            if id == '':
                return None
            if 'cafe' in id:
                product = Product.objects.get(id=id.split('-')[2])
            else:
                product = ProductLp.objects.get(id=id)
                value = create_value(product, id)
        except Exception:
            value = None
        return value
    if category == 'drink':
        try:
            id = menu_all.filter(date=date_str).get(meal=meal).drink
            if id == '':
                return None
            if 'cafe' in id:
                product = Product.objects.get(id=id.split('-')[2])
            else:
                product = ProductLp.objects.get(id=id)
            value = create_value(product, id)
        except Exception:
            value = None
        return value
    if category == 'salad':
        try:
            id = menu_all.filter(date=date_str).get(meal=meal).salad
            if id == '':
                return None
            if 'cafe' in id:
                product = Product.objects.get(id=id.split('-')[2])
            else:
                product = ProductLp.objects.get(id=id)
            value = create_value(product, id)
        except Exception:
            value = None
        return value



def creates_dict_with_menu_patients(id):
    menu_all = MenuByDay.objects.filter(user_id=id)
    menu = {}
    day_date = {
        'today': str(date.today()),
        'tomorrow': str(date.today() + timedelta(days=1)),
        'day_after_tomorrow': str(date.today() + timedelta(days=2)),
    }
    for day, date_str in day_date.items():
        menu[day] = {}
        for meal in ['breakfast', 'afternoon', 'lunch', 'dinner']:
            menu[day][meal] = {
                'main': check_value_two(menu_all, date_str, meal, "main"),
                'garnish': check_value_two(menu_all, date_str, meal, "garnish"),
                'porridge': check_value_two(menu_all, date_str, meal, "porridge"),
                'soup': check_value_two(menu_all, date_str, meal, "soup"),
                'dessert': check_value_two(menu_all, date_str, meal, "dessert"),
                'fruit': check_value_two(menu_all, date_str, meal, "fruit"),
                'drink': check_value_two(menu_all, date_str, meal, "drink"),
                'salad': check_value_two(menu_all, date_str, meal, "salad"),
            }
        menu[day]['date_human_style'] = dateformat.format(date.fromisoformat(date_str), 'd E, l')
    return menu

def add_default_menu(user):
    # генератор списка return даты на след 2 дня
    days = [parse(user.receipt_date) + timedelta(days=delta) for delta in [0, 1, 2]]
    for day_of_the_week in days:
        for meal in ['breakfast', 'afternoon', 'lunch', 'dinner']:
            translated_diet = user.type_of_diet
            products = ProductLp.objects.filter(Q(timetablelp__day_of_the_week=get_day_of_the_week(str(day_of_the_week))) &
                                                Q(timetablelp__type_of_diet=translated_diet) &
                                                Q(timetablelp__meals=meal))
            to_create = []
            to_create.append(MenuByDay(
                user_id=user,
                date=day_of_the_week,
                meal=meal,
                main=check_value('основной', products),
                garnish=check_value('гарнир', products),
                porridge=check_value('каша', products),
                soup=check_value('суп', products),
                dessert=check_value('десерт', products),
                fruit=check_value('фрукты', products),
                drink=check_value('напиток', products),
                salad=check_value('салат', products),
                ))
            MenuByDay.objects.bulk_create(to_create)
    return

def add_default_menu_on_one_day(day_of_the_week, user):
    for meal in ['breakfast', 'afternoon', 'lunch', 'dinner']:
        translated_diet = user.type_of_diet
        products = ProductLp.objects.filter(Q(timetablelp__day_of_the_week=get_day_of_the_week(str(day_of_the_week))) &
                                            Q(timetablelp__type_of_diet=translated_diet) &
                                            Q(timetablelp__meals=meal))
        to_create = []
        to_create.append(MenuByDay(
            user_id=user,
            date=day_of_the_week,
            meal=meal,
            main=check_value('основной', products),
            garnish=check_value('гарнир', products),
            porridge=check_value('каша', products),
            soup=check_value('суп', products),
            dessert=check_value('десерт', products),
            fruit=check_value('фрукты', products),
            drink=check_value('напиток', products),
            salad=check_value('салат', products),
            ))
        MenuByDay.objects.bulk_create(to_create)
    return

def add_menu_three_days_ahead():
    users = CustomUser.objects.filter(status='patient')
    days = [date.today() + timedelta(days=delta) for delta in [0, 1, 2]]
    for user in users:
        menu_all = MenuByDay.objects.filter(user_id=user.id)
        for index, day in enumerate(days):
            if len(menu_all.filter(date=str(day))) == 0 and (day >= user.receipt_date):
                for change_day in days[index:]:
                    add_default_menu_on_one_day(change_day, user)
    return


def creating_meal_menu_cafe(date_get, diet, meal):

    queryset_main_dishes = list(Product.objects.filter(timetable__datetime=date_get).filter(**{diet: 'True'}).filter(
        category='Вторые блюда').order_by(Lower('name')))
    queryset_garnish = list(Product.objects.filter(timetable__datetime=date_get).filter(**{diet: 'True'}).filter(
        category='Гарниры').order_by(Lower('name')))
    queryset_salad = list(Product.objects.filter(timetable__datetime=date_get).filter(**{diet: 'True'}).filter(
        category='Салаты').order_by(Lower('name')))
    queryset_soup = list(Product.objects.filter(timetable__datetime=date_get).filter(**{diet: 'True'}).filter(
        category='Первые блюда').order_by(Lower('name')))

    queryset_main_dishes, queryset_garnish, queryset_salad, queryset_soup = \
        sorting_dishes(meal, queryset_main_dishes, queryset_garnish, queryset_salad, queryset_soup)

    return queryset_main_dishes, queryset_garnish, queryset_salad, queryset_soup


def creating_meal_menu_lp(day_of_the_week, translated_diet, meal):
    products_main = []
    products_porridge = []
    products_dessert = []
    products_fruit = []
    products_salad = []
    products_soup = []
    products_drink = []
    products_garnish = []

    products = ProductLp.objects.filter(Q(timetablelp__day_of_the_week=day_of_the_week) &
                                        Q(timetablelp__type_of_diet=translated_diet) &
                                        Q(timetablelp__meals=meal))

    if meal == 'breakfast':
        products_garnish = list(products.filter(category='гарнир'))
        products_main = list(products.filter(category='основной'))
        products_porridge = list(products.filter(category='каша'))

    if meal == 'afternoon':
        products_main = list(products.filter(category='основной'))
        products_dessert = list(products.filter(category='десерт'))
        products_fruit = list(products.filter(category='фрукты'))
        products_drink = list(products.filter(category='напиток'))

    if meal == 'lunch':
        products_main = list(products.filter(category='основной'))
        products_garnish = list(products.filter(category='гарнир'))
        products_salad = list(products.filter(category='салат'))
        products_soup = list(products.filter(category='суп'))
        products_drink = list(products.filter(category='напиток'))

    if meal == 'dinner':
        products_main = list(products.filter(category='основной'))
        products_garnish = list(products.filter(category='гарнир'))
        products_drink = list(products.filter(category='напиток'))
    return products_main, products_garnish, products_salad, products_soup, products_porridge, products_dessert, products_fruit, products_drink