from nutritionist.models import ProductLp, CustomUser, MenuByDay, Product, BotChatId,\
    UsersToday, MenuByDayReadyOrder, UsersReadyOrder
from django.db import transaction
from dateutil.parser import parse
from django.db.models import Q
from typing import List
from datetime import datetime, date, timedelta
from django.utils import dateformat
from django.db.models.functions import Lower
import logging, random, telepot
from doctor.functions.bot import check_change, formatting_full_name, do_messang_send
from doctor.functions.for_print_forms import create_user_today, check_time, update_UsersToday, update_СhangesUsersToday, \
    applies_changes
from doctor.tasks import my_job_send_messang_changes


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

def translate_meal(meal):
    MEALS = {
        'breakfast': 'Завтрак',
        'lunch': 'Обед',
        'afternoon': 'Полдник',
        'dinner': 'Ужин'
    }
    return MEALS[meal]


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
            res += value[0:1].capitalize() + '.'
            continue
        else:
            res += value[0:1].capitalize() + '.'
    return res

def check_value(category, products):
    value: str = ''
    try:
        value = products.get(category=category).id
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
        'carbohydrate': round(float(0 if product.carbohydrate == None else product.carbohydrate), 1),
        'fat': round(float(0 if product.fat == None else product.fat), 1),
        'fiber': round(float(0 if product.fiber == None else product.fiber), 1),
        'energy': round(float(0 if product.energy == None else product.energy), 1),
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
    """ Создаем меню на 3 дня для вывода в ЛК врача"""
    menu_all = MenuByDay.objects.filter(user_id=id)
    menu = {}
    day_date = {
        'today': str(date.today()),
        'tomorrow': str(date.today() + timedelta(days=1)),
        'day_after_tomorrow': str(date.today() + timedelta(days=2)),
    }
    for day, date_str in day_date.items():
        menu[day] = {}
        for meal in ['breakfast', 'lunch', 'afternoon', 'dinner']:
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
        menu[day]['date'] = dateformat.format(date.fromisoformat(date_str), 'Y-m-d')
    return menu


def creates_dict_with_menu_patients_on_day(id, date_show):
    """ Создаем меню на день для вывода в ЛК пациента(история) """
    menu_all = MenuByDay.objects.filter(user_id=id)
    menu = {}

    for meal in ['breakfast', 'lunch', 'afternoon', 'dinner']:
        menu[meal] = {
            'main': check_value_two(menu_all, date_show, meal, "main"),
            'garnish': check_value_two(menu_all, date_show, meal, "garnish"),
            'porridge': check_value_two(menu_all, date_show, meal, "porridge"),
            'soup': check_value_two(menu_all, date_show, meal, "soup"),
            'dessert': check_value_two(menu_all, date_show, meal, "dessert"),
            'fruit': check_value_two(menu_all, date_show, meal, "fruit"),
            'drink': check_value_two(menu_all, date_show, meal, "drink"),
            'salad': check_value_two(menu_all, date_show, meal, "salad"),
        }
    return menu


def add_default_menu(user):
    # генератор списка return даты на след 3 дня
    days = [parse(user.receipt_date) + timedelta(days=delta) for delta in [0, 1, 2]]
    for day_of_the_week in days:
        for meal in ['breakfast', 'lunch', 'afternoon', 'dinner']:
            translated_diet = user.type_of_diet
            products = ProductLp.objects.filter(Q(timetablelp__day_of_the_week=get_day_of_the_week(str(day_of_the_week))) &
                                                Q(timetablelp__type_of_diet=translated_diet) &
                                                Q(timetablelp__meals=meal))
            to_create = []
            to_create.append(MenuByDay(
                user_id=user,
                date=day_of_the_week,
                meal=meal,
                type_of_diet=user.type_of_diet,
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
    for meal in ['breakfast', 'lunch', 'afternoon', 'dinner']:
        translated_diet = user.type_of_diet
        products = ProductLp.objects.filter(Q(timetablelp__day_of_the_week=get_day_of_the_week(str(day_of_the_week))) &
                                            Q(timetablelp__type_of_diet=translated_diet) &
                                            Q(timetablelp__meals=meal))
        to_create = []
        to_create.append(MenuByDay(
            user_id=user,
            date=day_of_the_week,
            meal=meal,
            type_of_diet=user.type_of_diet,
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


def check_have_menu():
    # посмотреть все даты от регистрации до сегодня -1, если нет меню, тогда добавить.
    users = CustomUser.objects.filter(status='patient')
    # days = [date.today() + timedelta(days=delta) for delta in [0, 1, 2]]
    for user in users:
        menu_all = MenuByDay.objects.filter(user_id=user.id)
        # находим кол-во дней от сегодня до даты регитрации
        count_days = date.today() - user.receipt_date
        for delta in range(1, count_days.days - 1):
            # дата сегодня минус delta
            day = date.today() - timedelta(days=delta)
            if len(menu_all.filter(date=str(day))) == 0:
                add_default_menu_on_one_day(day, user)
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


def delete_choices(CustomUserFormSet):
    """ Удаляем два выбора из formset 'не выбрано', '-------' """
    CustomUserFormSet.form.base_fields['department'].choices = CustomUserFormSet.form.base_fields['department'].choices[
                                                               2:]
    CustomUserFormSet.form.base_fields['type_of_diet'].choices = CustomUserFormSet.form.base_fields[
                                                                     'type_of_diet'].choices[
                                                                 2:]
    CustomUserFormSet.form.base_fields['room_number'].choices = CustomUserFormSet.form.base_fields[
                                                                    'room_number'].choices[
                                                                2:]
    return CustomUserFormSet

logging.basicConfig(
    level=logging.DEBUG,
    filename="mylog.log",
    format="%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s",
    datefmt='%Y-%m-%d %H:%M:%S',
)


def check_meal_user(user, type):
    """ Вернет на какой прием пищи успевает пациент. """
    if type == 'archiving':
        receipt_time = parse(str(user.receipt_date) + ' ' + str(user.receipt_time)).time()
        receipt_date = parse(str(user.receipt_date))
    else:
        receipt_time = parse(user.receipt_date + ' ' + user.receipt_time).time()
        receipt_date = parse(user.receipt_date)
    # Если пользователь есть в UsersReadyOrder, тогда вернем "завтрак".
    if receipt_date.date() >= date.today():
        if receipt_time.hour > 0 and receipt_time.hour < 10:
            return 'зактрака', 0
        if receipt_time.hour >= 10 and receipt_time.hour < 14:
            return 'обеда', 1
        if receipt_time.hour >= 14 and receipt_time.hour < 17:
            return 'полдника', 2
        if receipt_time.hour >= 17 and receipt_time.hour < 21:
            return 'ужина', 3
        if receipt_time.hour >= 21:
            return 'завтра', 4
    else:
        return 'зактрака', 0

def get_now_show_meal():
    """ Вернет след прием пищи. """
    time = datetime.today().time()
    if time.hour > 0 and time.hour < 9:
        return 'зактрака'
    if time.hour >= 9 and time.hour < 12:
        return 'обеда'
    if time.hour >= 12 and time.hour < 16:
        return 'полдника'
    if time.hour >= 16 and time.hour < 19:
        return 'ужина'
    return 'завтра'




def create_user(user_form):
    # генерируем уникальный логин
    while True:
        login = ''.join([random.choice("123456789qwertyuiopasdfghjklzxcvbnm") for i in range(10)])
        try:
            CustomUser.objects.get(id=login)
            continue
        except Exception:
            break

    user = CustomUser.objects.create_user(login)
    user.full_name = user_form.data['full_name']
    user.receipt_date = datetime.strptime(user_form.data['receipt_date'], '%d.%m.%Y').strftime('%Y-%m-%d')
    user.receipt_time = parse(user_form.data['receipt_time']).strftime('%h:%m')
    user.receipt_time = user_form.data['receipt_time']
    user.department = user_form.data['department']
    user.room_number = user_form.data['room_number']
    user.type_of_diet = user_form.data['type_of_diet']
    user.comment = user_form.data['comment']
    user.status = 'patient'
    user.save()
    logging.info(f'Создан пациент {user_form.data["full_name"]} {user_form.data["type_of_diet"]}')
    add_default_menu(user)
    add_menu_three_days_ahead()

    if datetime.today().time().hour >= 19:
        if parse(user.receipt_date).date() == (date.today() + timedelta(days=1)) and \
            (parse(user.receipt_date + ' ' + user.receipt_time).time() <= parse(user.receipt_date + ' ' + '10:00').time()):
                update_UsersToday(user)
        else:
            if parse(user.receipt_date).date() == date.today():
                update_UsersToday(user)
    else:  # время меньше 19
        if parse(user.receipt_date).date() == date.today():
            # Проверяем с какого приема пищи мы можем накормить пациента.
            meal_permissible, weight_meal_permissible = check_change('True')
            # Проверяем на какой прием пищи успевает пациент пациента.
            meal_user, weight_meal_user = check_meal_user(user, 'creating')
            # Прием пищи с которого пациент будет добавлен в заказ.
            meal_order = meal_permissible if weight_meal_permissible >= weight_meal_user else meal_user
            # Определяем, какой след прием пищи.
            now_show_meal = get_now_show_meal()
            if meal_order == now_show_meal and meal_order != 'завтра':
                update_UsersToday(user)
            if do_messang_send() and meal_order != 'завтра':  # c 17 до 7 утра не отправляем сообщения
                regard = u'\u26a0\ufe0f'
                messang = f'{regard} <b>Изменение с {meal_order}</b>\n'
                messang += f'Поступил пациент {formatting_full_name(user.full_name)} ({user.type_of_diet})\n'
                if user.comment:
                    messang += f'Комментарий: "{user.comment}"'
                my_job_send_messang_changes.delay(messang)


def get_next_meals():
    """ Вернет след прием пищи. """
    time = datetime.today().time()
    if time.hour > 0 and time.hour < 7:
        return ['breakfast', 'lunch', 'afternoon', 'dinner']
    if time.hour >= 7 and time.hour < 11:
        return ['lunch', 'afternoon', 'dinner']
    if time.hour >= 11 and time.hour < 14:
        return ['afternoon', 'dinner']
    if time.hour >= 14 and time.hour < 17:
        return ['dinner']
    return []

@transaction.atomic
def load_menu_for_future(user, meal, change_day):
    to_create = []
    translated_diet = user.type_of_diet
    products = ProductLp.objects.filter(
        Q(timetablelp__day_of_the_week=get_day_of_the_week(str(change_day))) &
        Q(timetablelp__type_of_diet=translated_diet) &
        Q(timetablelp__meals=meal))
    to_create.append(MenuByDay(
        user_id=user,
        date=change_day,
        meal=meal,
        type_of_diet=user.type_of_diet,
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

def delete_menu_for_future(user, days, next_meals):
    for index, change_day in enumerate(days):
        next_meals = next_meals if index == 0 else ['breakfast', 'lunch', 'afternoon', 'dinner']
        for meal in next_meals:
            set_menu_del = MenuByDay.objects.filter(user_id=user.id).filter(date=str(change_day)).filter(meal=meal)
            for menu_del in set_menu_del:
                menu_del.delete()

def update_menu_for_future(user, flag_is_change_diet):
    """ Если поменялась диета или добавили комментарий.
        Удаляем все меню в будущем и добавляем новое.
     """
    try:
        if flag_is_change_diet:
            UsersReadyOrder.objects.get(user_id=user.id)
        next_meals = get_next_meals()
        days = [date.today() + timedelta(days=delta) for delta in [0, 1, 2]]
        delete_menu_for_future(user, days, next_meals)

        for index, change_day in enumerate(days):
            next_meals = next_meals if index == 0 else ['breakfast', 'lunch', 'afternoon', 'dinner']
            for meal in next_meals:
                load_menu_for_future(user, meal, change_day)
    except:
        MenuByDay.objects.filter(user_id=user.id).delete()
        add_default_menu(user)
        add_menu_three_days_ahead()


def edit_user(user_form, type):
    changes = []
    # flag = False
    is_change_diet = False
    flag_add_comment = False
    user = CustomUser.objects.get(id=user_form.data['id_edit_user'])
    # обравляем CustomUser и состовляем список изменений
    if user.full_name != user_form.data['full_name1']:
        changes.append(f"ФИО <b>{user.full_name}</b> изменена на <u><b>{user_form.data['full_name1']}</b></u>")
    user.full_name = user_form.data['full_name1']
    if user.receipt_date != datetime.strptime(user_form.data['receipt_date1'], '%d.%m.%Y').date():
        # # проверяем если дату из прошлого поренесли в будущее
        # if type == 'edit' and \
        #     user.receipt_date <= date.today() and \
        #     datetime.strptime(user_form.data['receipt_date1'], '%d.%m.%Y').date() > date.today():
        #     flag = True
        changes.append(f"дату поступления <b>{user.receipt_date}</b> изменена на <u><b>{datetime.strptime(user_form.data['receipt_date1'], '%d.%m.%Y').strftime('%Y-%m-%d')}</b></u>")
    user.receipt_date = datetime.strptime(user_form.data['receipt_date1'], '%d.%m.%Y').strftime('%Y-%m-%d')

    if (user.receipt_time).strftime('%H:%M') != user_form.data['receipt_time1']:
        changes.append(f"время поступления <b>{(user.receipt_time).strftime('%H:%M')}</b> изменено на <u><b>{user_form.data['receipt_time1']}</b></u>")
    user.receipt_time = user_form.data['receipt_time1']

    if user.department != user_form.data['department1']:
        changes.append(f"отделение <b>{user.department}</b> изменено на <u><b>{user_form.data['department1']}</b></u>")
    user.department = user_form.data['department1']

    if user.room_number != user_form.data['room_number1']:
        changes.append(f"номер палаты <b>{user.room_number}</b> изменен на <u><b>{user_form.data['room_number1']}</b></u>")
    user.room_number = user_form.data['room_number1']

    if user.type_of_diet != user_form.data['type_of_diet1']:
        changes.append(f"тип диеты <b>{user.type_of_diet}</b> изменен на <u><b>{user_form.data['type_of_diet1']}</b></u>")
        if type == 'edit':
            is_change_diet = True
    user.type_of_diet = user_form.data['type_of_diet1']

    if user.comment != user_form.data['comment1']:
        # Если добавили коментарий, рашьше было без комментария
        flag_add_comment = True if len(user.comment) < 2 and\
                                   len(user_form.data['comment1']) > 2 else False

        changes.append(f'комметнарий "{user.comment if user.comment else "нет комментария"}" изменен на <u><b>"{user_form.data["comment1"]}"</b></u>')
    user.comment = user_form.data['comment1']
    # если надо восстановить учетную запись пациента
    if type == 'restore':
        user.status = 'patient'
    user.save()
    logging.info(f'Пациент отредактирован {user_form.data["full_name"]}')
    flag_is_change_diet = is_change_diet
    if type == 'restore':
        # ПОМЕНЯТЬ ФУНКЦИЮ
        add_default_menu(user)
        add_menu_three_days_ahead()
    elif flag_is_change_diet or flag_add_comment:
        update_menu_for_future(user, flag_is_change_diet)

    # date_order = date.today() + timedelta(days=1) if datetime.today().time().hour >= 19 else date.today()
    # # после 19 в заказ добавляем пользователей с датой госпитализации на след день
    # if parse(user.receipt_date).date() <= date_order or flag == True:
    #     if check_time():
    #         update_UsersToday(user)
    #     else:
    #         update_СhangesUsersToday(user)
    #     # отправить сообщение

    if datetime.today().time().hour >= 19:
        if parse(user.receipt_date).date() == (date.today() + timedelta(days=1)) and \
                (parse(user.receipt_date + ' ' + user.receipt_time).time() <= parse(
                    user.receipt_date + ' ' + '10:00').time()):
            update_UsersToday(user)
        else:
            if parse(user.receipt_date).date() == date.today():
                update_UsersToday(user)
    else:  # время меньше 19
        if parse(user.receipt_date).date() <= date.today():
            # Проверяем с какого приема пищи мы можем накормить пациента.
            meal_permissible, weight_meal_permissible = check_change('True')
            # Проверяем на какой прием пищи успевает пациент пациента.
            meal_user, weight_meal_user = check_meal_user(user, 'editing')
            # Прием пищи с которого пациент будет добавлен в заказ.
            meal_order = meal_permissible if weight_meal_permissible >= weight_meal_user else meal_user
            # Определяем, какой след прием пищи сейчас в печатных формах.
            now_show_meal = get_now_show_meal()
            if meal_order == now_show_meal and meal_order != 'завтра':
                update_UsersToday(user)
    if do_messang_send():  # c 17 до 7 утра не отправляем сообщения
        # TOKEN = '5533289712:AAEENvPBVrfXJH1xotRzoCCi24xFcoH9NY8'
        attention = u'\u2757\ufe0f'
        regard = u'\u26a0\ufe0f'
        # bot = telepot.Bot(TOKEN)
        # все номера chat_id
        if type == 'edit':
            messang = ''
            messang += f'{regard} <b>Изменение с {meal_order}</b>\n'
            messang += f'Отредактирован профиль пациента {formatting_full_name(user.full_name)}:\n\n'
            for change in changes:
                messang += f'- {change}\n'
        if type == 'restore':
            messang = ''
            messang += f'{regard} <b>Изменение с {meal_order}</b>\n'
            messang += f'Поступил пациент {formatting_full_name(user.full_name)} ({user.type_of_diet})\n'
            messang += f'Комментарий: "{user.comment}"' if user.comment else ''
        my_job_send_messang_changes.delay(messang)


def archiving_user(user):
    user.status = 'patient_archive'
    user.save()
    update_UsersToday(user)
    MenuByDay.objects.filter(user_id=user.id).delete()
    if user.receipt_date <= date.today():
        # Проверяем с какого приема пищи мы можем накормить пациента.
        meal_permissible, weight_meal_permissible = check_change('True')
        # Проверяем на какой прием пищи успевает пациент пациента.
        meal_user, weight_meal_user = check_meal_user(user, 'archiving')
        # Прием пищи с которого пациент будет добавлен в заказ.
        meal_order = meal_permissible if weight_meal_permissible >= weight_meal_user else meal_user

        if do_messang_send():  # c 17 до 7 утра не отправляем сообщения
            attention = u'\u26a0\ufe0f'
            messang = ''
            messang += f'{attention} <b>Изменение с {meal_order}</b>\n'
            messang += f'Пациент {formatting_full_name(user.full_name)} ({user.type_of_diet}) выписан\n'
            return my_job_send_messang_changes.delay(messang)



    # дата на которую создается заказ
    # receipt_date = str(user.receipt_date)
    # receipt_time = str(user.receipt_time)
    # if datetime.today().time().hour >= 19:
    #     if parse(receipt_date).date() == (date.today() + timedelta(days=1)) and \
    #             (parse(receipt_date + ' ' + receipt_time).time() <= parse(
    #                 receipt_date + ' ' + '10:00').time()):
    #         update_UsersToday(user)
    #     else:
    #         if parse(receipt_date).date() == date.today():
    #             update_UsersToday(user)
    # else:  # время меньше 19
    #     if parse(receipt_date).date() == date.today():
    #         # Проверяем с какого приема пищи мы можем накормить пациента.
    #         meal_permissible, weight_meal_permissible = check_change('True')
    #         # Проверяем на какой прием пищи успевает пациент пациента.
    #         meal_user, weight_meal_user = check_meal_user(user, 'archiving')
    #         # Прием пищи с которого пациент будет добавлен в заказ.
    #         meal_order = meal_permissible if weight_meal_permissible >= weight_meal_user else meal_user
    #         # Определяем, какой след прием пищи.
    #         now_show_meal = get_now_show_meal()
    #         if meal_order == now_show_meal and meal_order != 'завтра':
    #             update_UsersToday(user)
    #         if do_messang_send() and meal_order != 'завтра':  # c 17 до 7 утра не отправляем сообщения
    #             attention = u'\u2757\ufe0f'
    #             TOKEN = '5533289712:AAEENvPBVrfXJH1xotRzoCCi24xFcoH9NY8'
    #             bot = telepot.Bot(TOKEN)
    #             # все номера chat_id
    #             messang = ''
    #             messang += f'{attention} Изменение с <u><b>{check_change(user)}</b></u>{attention}\n'
    #             messang += f'Пациент <u><b>{formatting_full_name(user.full_name)} ({user.type_of_diet})</b></u> выписан\n'
    #             for item in BotChatId.objects.all():
    #                 bot.sendMessage(item.chat_id, messang, parse_mode="html")






def counting_diets(users):
    diets_name = ['ОВД', 'ОВД без сахара', 'ЩД', 'БД', 'ВБД', 'НБД', 'НКД', 'ВКД']
    diets_count = []
    for diet in diets_name:
        users_diet = users.filter(type_of_diet=diet)
        start_2nd_floor = 200
        end_2nd_floor = 299
        start_3nd_floor = 300
        end_3nd_floor = 399
        if len(users_diet) > 0:
            diets_count.append({
                "name": diet,
                "total": str(len(users_diet)),
                "2nd_floor": len([users_floor for users_floor in users_diet if (int(users_floor.room_number) >= start_2nd_floor) \
                                  and (int(users_floor.room_number) <= end_2nd_floor)]),
                "3nd_floor": len([users_floor for users_floor in users_diet if (int(users_floor.room_number) >= start_3nd_floor) \
                                  and (int(users_floor.room_number) <= end_3nd_floor)])
            })
    return diets_count



def creates_dict_test(id, id_fix_user, date_show, lp_or_cafe, meal, type_order):
    """ Создаем словарь с блюдами на конкретный прием пищи для пациента """
    if type_order == 'flex-order':
        menu_all = MenuByDay.objects.filter(user_id=id)
    else:
        menu_all = MenuByDayReadyOrder.objects.filter(user_id=id_fix_user)
    menu = {}
    menu_list = []
    # for meal in ['breakfast', 'lunch', 'afternoon', 'dinner']:
    menu = {
        'main': check_value_two(menu_all, date_show, meal, "main"),
        'garnish': check_value_two(menu_all, date_show, meal, "garnish"),
        'porridge': check_value_two(menu_all, date_show, meal, "porridge"),
        'soup': check_value_two(menu_all, date_show, meal, "soup"),
        'dessert': check_value_two(menu_all, date_show, meal, "dessert"),
        'fruit': check_value_two(menu_all, date_show, meal, "fruit"),
        'drink': check_value_two(menu_all, date_show, meal, "drink"),
        'salad': check_value_two(menu_all, date_show, meal, "salad"),
    }
    if lp_or_cafe == 'lp':
        for item in menu.values():
            if item:
                if 'cafe' not in item['id']:
                    menu_list.append(item.get('name'))
    if lp_or_cafe == 'cafe':
        for item in menu.values():
            if item:
                if 'cafe' in item['id']:
                    menu_list.append(item.get('name'))
    return menu_list


def create_list_users_on_floor(users, start, end, meal, date_create, type_order):
    users = [user for user in users if (int(user.room_number) >= start) \
                                  and (int(user.room_number) <= end)]
    users_on_floor = []
    for user in users:
        users_on_floor.append(
            {'name': user.full_name,
             'number': '',
             'room_number': user.room_number,
             'diet': user.type_of_diet,
             'products_lp': creates_dict_test(user.user_id, user.id, str(date_create), 'lp', meal, type_order),
             'products_cafe': creates_dict_test(user.user_id, user.id, str(date_create), 'cafe', meal, type_order),
             }
        )
    return users_on_floor

def what_meal():
    if datetime.today().time().hour < 9:
        return 'breakfast', None
    if datetime.today().time().hour >= 9 and datetime.today().time().hour < 12:
        return 'lunch', None
    if datetime.today().time().hour >= 12 and datetime.today().time().hour < 16:
        return 'afternoon', None
    if datetime.today().time().hour >= 16 and datetime.today().time().hour < 19:
        return 'dinner', None
    if datetime.today().time().hour >= 19:
        return 'breakfast', 'tomorrow'


def what_type_order():
    if (datetime.today().time().hour >= 7  and datetime.today().time().hour < 9)\
        or (datetime.today().time().hour >= 11  and datetime.today().time().hour < 12) \
        or (datetime.today().time().hour >= 14 and datetime.today().time().hour < 16) \
        or (datetime.today().time().hour >= 17 and datetime.today().time().hour < 19):
        return 'fix-order'
    return 'flex-order'
