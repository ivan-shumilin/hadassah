from nutritionist.models import ProductLp, CustomUser, MenuByDay, Product, BotChatId,\
    UsersToday, MenuByDayReadyOrder, UsersReadyOrder
from django.db import transaction
from django.contrib import messages
from django.contrib.messages import get_messages
from dateutil.parser import parse
from django.db.models import Q
from typing import List
from datetime import datetime, date, timedelta
from django.utils import dateformat
from django.db.models.functions import Lower
import logging, random, telepot
from doctor.functions.bot import check_change, formatting_full_name, do_messang_send
from doctor.functions.helpers import check_value, formatting_full_name_mode_full
from doctor.functions.translator import get_day_of_the_week
from doctor.functions.diet_formation import add_default_menu_on_one_day,\
    writes_the_patient_menu_to_the_database, add_the_patient_menu
from doctor.functions.for_print_forms import create_user_today, check_time, update_UsersToday, update_СhangesUsersToday, \
    applies_changes
from doctor.tasks import my_job_send_messang_changes

def get_is_change_diet(patient):
    """
    Устанавливает значение is_change_diet_bd.
    Если смена происходит с 17 до 19 тогда не меняем диету.
    """
    if datetime.today().time().hour >= 17 and datetime.today().time().hour < 19: # поменять на 17
        patient.is_change_diet_bd = False
        patient.save()


def sorting_dishes(meal, queryset_main_dishes, queryset_garnish, queryset_salad, queryset_soup):
    """Сортировка блюд по приемам пищи."""

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

def create_value(product, id, is_public):
    if is_public:
        try:
            name = product.public_name
        except:
            name = product.name
    else:
        name = product.name
    value = {
        'id': id,
        'name': name,
        'carbohydrate': round(float(0 if product.carbohydrate == None else product.carbohydrate), 1),
        'fat': round(float(0 if product.fat == None else product.fat), 1),
        'fiber': round(float(0 if product.fiber == None else product.fiber), 1),
        'energy': round(float(0 if product.energy == None else product.energy), 1),
        'image': product.image,
        'description': product.description,
        'category': product.category,
    }
    return value

def check_value_two(menu_all, date_str, meal, category, is_public):
    if category == 'salad':
        try:
            id = menu_all.filter(date=date_str).get(meal=meal).salad
            if id == '':
                return None
            if 'cafe' in id:
                product = Product.objects.get(id=id.split('-')[2])
            else:
                product = ProductLp.objects.get(id=id)
            value = create_value(product, id, is_public)
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
            value = create_value(product, id, is_public)
        except Exception:
            value = None
        return value
    if category == 'main':
        try:
            id = menu_all.filter(date=date_str).get(meal=meal).main
            if id == '':
                return None
            if 'cafe' in id:
                product = Product.objects.get(id=id.split('-')[2])
            else:
                product = ProductLp.objects.get(id=id)
            value = create_value(product, id, is_public)
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
            value = create_value(product, id, is_public)
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
            value = create_value(product, id, is_public)
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
            value = create_value(product, id, is_public)
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
            value = create_value(product, id, is_public)
        except Exception:
            value = None
        return value
    if category == 'drink':
        try:
            value: list = []
            id_set = (menu_all.filter(date=date_str).get(meal=meal).drink).split(',')
            if len(id_set) == 0:
                return [None]
            for id in id_set:
                if 'cafe' in id:
                    product = Product.objects.get(id=id.split('-')[2])
                else:
                    product = ProductLp.objects.get(id=id)
                value.append({
                    'id': id,
                    'name': product.public_name if is_public else product.name,
                    'carbohydrate': round(float(0 if product.carbohydrate == None else product.carbohydrate), 1),
                    'fat': round(float(0 if product.fat == None else product.fat), 1),
                    'fiber': round(float(0 if product.fiber == None else product.fiber), 1),
                    'energy': round(float(0 if product.energy == None else product.energy), 1),
                    'image': product.image,
                    'description': product.description,
                    'category': product.category,
                })
        except Exception:
            value = [None]
        return value
    if category == 'products':
        try:
            value: list = []
            id_set = (menu_all.filter(date=date_str).get(meal=meal).products).split(',')
            if len(id_set) == 0:
                return [None]
            for id in id_set:
                if 'cafe' in id:
                    product = Product.objects.get(id=id.split('-')[2])
                else:
                    product = ProductLp.objects.get(id=id)
                value.append({
                    'id': id,
                    'name': product.public_name if is_public else product.name,
                    'carbohydrate': round(float(0 if product.carbohydrate == None else product.carbohydrate), 1),
                    'fat': round(float(0 if product.fat == None else product.fat), 1),
                    'fiber': round(float(0 if product.fiber == None else product.fiber), 1),
                    'energy': round(float(0 if product.energy == None else product.energy), 1),
                    'image': product.image,
                    'description': product.description,
                    'category': product.category,
                })
        except Exception:
            value = [None]
        return value
    if category == 'bouillon':
        try:
            id = menu_all.filter(date=date_str).get(meal=meal).bouillon
            if id == '':
                return None
            if 'cafe' in id:
                product = Product.objects.get(id=id.split('-')[2])
            else:
                product = ProductLp.objects.get(id=id)
            value = create_value(product, id, is_public)
        except Exception:
            value = None
        return value

def creates_dict_with_menu_patients(id):
    """Создаем меню на 3 дня для вывода в ЛК врача."""
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
                'salad': check_value_two(menu_all, date_str, meal, "salad", is_public=True),
                'soup': check_value_two(menu_all, date_str, meal, "soup", is_public=True),
                'main': check_value_two(menu_all, date_str, meal, "main", is_public=True),
                'garnish': check_value_two(menu_all, date_str, meal, "garnish", is_public=True),
                'porridge': check_value_two(menu_all, date_str, meal, "porridge", is_public=True),
                'dessert': check_value_two(menu_all, date_str, meal, "dessert", is_public=True),
                'fruit': check_value_two(menu_all, date_str, meal, "fruit", is_public=True),
                'drink': check_value_two(menu_all, date_str, meal, "drink", is_public=True),
                'bouillon': check_value_two(menu_all, date_str, meal, "bouillon", is_public=True),
            }
            flag_no_products = True
            for category in ['main', 'garnish', 'porridge', 'soup', 'dessert', 'fruit', 'drink', 'salad']:
                if menu[day][meal][category] != None and menu[day][meal][category] != [None]:
                    flag_no_products = False
            if flag_no_products:
                menu[day][meal] = None

        menu[day]['date_human_style'] = dateformat.format(date.fromisoformat(date_str), 'd E, l').lower()
        menu[day]['date'] = dateformat.format(date.fromisoformat(date_str), 'Y-m-d')
    return menu

def creates_dict_with_menu_patients_on_day(id, date_show):
    """Создаем меню на день для вывода в ЛК пациента(история)."""
    menu_all = MenuByDay.objects.filter(user_id=id)
    menu = {}

    for meal in ['breakfast', 'lunch', 'afternoon', 'dinner']:
        drink = [product\
                 for product in check_value_two(menu_all, date_show, meal, "drink", is_public=True)\
                 if product != None]
        drink = [product for product in drink if str(product.get('id')) != '458']
        menu[meal] = {
            'main': check_value_two(menu_all, date_show, meal, "main", is_public=True),
            'garnish': check_value_two(menu_all, date_show, meal, "garnish", is_public=True),
            'porridge': check_value_two(menu_all, date_show, meal, "porridge", is_public=True),
            'soup': check_value_two(menu_all, date_show, meal, "soup", is_public=True),
            'dessert': check_value_two(menu_all, date_show, meal, "dessert", is_public=True),
            'fruit': check_value_two(menu_all, date_show, meal, "fruit", is_public=True),
            'drink': None if len(drink) == 0 else drink[0],
            'salad': check_value_two(menu_all, date_show, meal, "salad", is_public=True),
        }
    return menu

def creating_meal_menu_cafe(date_get, diet, meal):
    exception = ['ОВД веган (пост) без глютена', 'БД день 2', 'БД день 1', 'Нулевая диета', 'ЩД без сахара',
                 'Безйодовая']
    if diet in exception:
        return [], [], [], []
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
    products = ProductLp.objects.filter(Q(timetablelp__day_of_the_week=day_of_the_week) &
                                        Q(timetablelp__type_of_diet=translated_diet) &
                                        Q(timetablelp__meals=meal))

    products_porridge = list(products.filter(category='каша'))
    products_salad = list(products.filter(category='салат'))
    products_soup = list(products.filter(category='суп'))
    products_main = list(products.filter(category='основной'))
    products_garnish = list(products.filter(category='гарнир'))
    products_dessert = list(products.filter(category='десерт'))
    products_fruit = list(products.filter(category='фрукты'))
    products_drink = list(products.filter(category='напиток'))

    return products_main, products_garnish, products_salad, products_soup, products_porridge, products_dessert, products_fruit, products_drink

def delete_choices(CustomUserFormSet):
    """Удаляем два выбора из formset 'не выбрано', '-------'"""
    CustomUserFormSet.form.base_fields['department'].choices.remove(('', '---------'))
    for field in ['type_of_diet', 'room_number']:
        CustomUserFormSet.form.base_fields[field].choices.remove(('', '---------'))
        if ('Не выбрано', 'Не выбрано') in CustomUserFormSet.form.base_fields[field].choices:
            CustomUserFormSet.form.base_fields[field].choices.remove(('Не выбрано', 'Не выбрано'))
    CustomUserFormSet.form.base_fields['type_of_diet'].choices.remove(('БД', 'БД'))

    return CustomUserFormSet

logging.basicConfig(
    level=logging.DEBUG,
    filename="mylog.log",
    format="%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s",
    datefmt='%Y-%m-%d %H:%M:%S',
)

def check_meal_user(user):
    """Вернет на какой прием пищи успевает пациент."""
    receipt_time = user.receipt_time
    receipt_date = user.receipt_date
    # Если пользователь есть в UsersReadyOrder, тогда вернем "завтрак".
    if receipt_date >= date.today():
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
    """Вернет след прием пищи."""
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

def comment_formatting(comment):
    comment = comment.strip().capitalize()
    if comment != '':
        comment = comment.strip().capitalize()
        comment = comment if comment[-1] == '.' else comment + '.'
    return comment

def get_user_name(request):
    first_name = f'{request.user.last_name if request.user.last_name != None else "None"}'
    last_name = f'{request.user.first_name if request.user.first_name != None else "None"}'
    return formatting_full_name(f'{first_name} {last_name}')

def is_user_look(user_form, is_accompanying, type_pay, is_probe, is_without_salt, is_without_lactose, is_pureed_nutrition):
    users = CustomUser.objects.filter(full_name=user_form.data['full_name'], status='patient')
    for user in users:
        time = user_form.data['receipt_time'].split(':')
        if user.full_name == user_form.data['full_name'] and\
            str(user.birthdate) == datetime.strptime(user_form.data['birthdate'], '%d.%m.%Y').strftime('%Y-%m-%d') and\
            str(user.receipt_date) == datetime.strptime(user_form.data['receipt_date'], '%d.%m.%Y').strftime('%Y-%m-%d') and \
            user.receipt_time == datetime(2000, 12, 12, int(time[0]), int(time[1])).time() and\
            str(user.floor) == str(user_form.data['floor']) and\
            str(user.department) == str(user_form.data['department']) and\
            str(user.room_number) == str((user_form.data['room_number'] if user_form.data['room_number'] != '' else 'Не выбрано')) and\
            str(user.bed) == str((user_form.data['bed'] if user_form.data['bed'] != '' else 'Не выбрано')) and\
            str(user.type_of_diet) == str(user_form.data['type_of_diet']) and\
            str(user.comment) == str(comment_formatting(user_form.data['comment'])) and\
            str(user.is_accompanying) == str(is_accompanying) and\
            str(user.type_pay) == str(type_pay) and\
            str(user.is_probe) == str(is_probe) and\
            str(user.is_without_salt) == str(is_without_salt) and\
            str(user.is_without_lactose) == str(is_without_lactose) and \
            str(user.is_pureed_nutrition) == str(is_pureed_nutrition) and \
            str(user.status) == 'patient':
            return True

def create_user(user_form, request):
    is_accompanying = request.POST['is_accompanying']
    type_pay = request.POST['type_pay']
    is_probe = False if request.POST['is_probe'] == 'False' else True
    is_without_salt = False if request.POST['is_without_salt'] == 'False' else True
    is_without_lactose = False if request.POST['is_without_lactose'] == 'False' else True
    is_pureed_nutrition = False if request.POST['is_pureed_nutrition'] == 'False' else True
    extra_bouillon = []
    if request.POST['is_bouillon_add'] == 'True':
        for meal in [('breakfast', 'breakfast_add'),\
                     ('lunch', 'lunch_add'), \
                     ('afternoon','afternoon_add'), \
                     ('dinner', 'dinner_add')]:
            if request.POST[meal[1]] == 'True':
                extra_bouillon.append(meal[0])
    extra_bouillon = ", ".join(extra_bouillon)



    is_user = is_user_look(
        user_form,
        is_accompanying,
        type_pay,
        is_probe,
        is_without_salt,
        is_without_lactose,
        is_pureed_nutrition)
    if is_user:
        return

    # генерируем уникальный логин
    while True:
        login = ''.join([random.choice("123456789qwertyuiopasdfghjklzxcvbnm") for i in range(10)])
        try:
            CustomUser.objects.get(id=login)
            continue
        except Exception:
            break

    user = CustomUser.objects.create_user(login)
    user.full_name = formatting_full_name_mode_full(user_form.data['full_name'])
    user.birthdate = datetime.strptime(user_form.data['birthdate'], '%d.%m.%Y').date()
    user.receipt_date = datetime.strptime(user_form.data['receipt_date'], '%d.%m.%Y').date()
    time = user_form.data['receipt_time'].split(':')
    user.receipt_time = datetime(2000, 12, 12, int(time[0]), int(time[1])).time()
    user.floor = user_form.data['floor']
    user.department = user_form.data['department']
    user.room_number = user_form.data['room_number'] if user_form.data['room_number'] != '' else 'Не выбрано'
    user.bed = user_form.data['bed'] if user_form.data['bed'] != '' else 'Не выбрано'
    user.type_of_diet = user_form.data['type_of_diet']
    user.comment = comment_formatting(user_form.data['comment'])
    user.is_accompanying = is_accompanying
    user.type_pay = type_pay
    user.is_probe = is_probe
    user.is_without_salt = is_without_salt
    user.is_without_lactose = is_without_lactose
    user.is_pureed_nutrition = is_pureed_nutrition
    user.status = 'patient'
    user.extra_bouillon = extra_bouillon
    user.save()
    if user.type_of_diet in ["БД день 1", "БД день 2"]:
        get_is_change_diet(user)

    user_name = get_user_name(request) # получаем имя пользователя (вносит изменения в ЛК)
    logging_messang = f'пользователь ({user_name}), cоздан пациент {user_form.data["full_name"]} ({user_form.data["type_of_diet"]})'
    logging_messang += f', доп. бульон: {extra_bouillon}]'
    logging.info(logging_messang)
    add_the_patient_menu(user, 'creation', extra_bouillon)
    messang = ''
    if datetime.today().time().hour >= 19:
        if parse(str(user.receipt_date)).date() == (date.today() + timedelta(days=1)) and \
            (parse(str(user.receipt_date) + ' ' + str(user.receipt_time)).time() <= parse(str(user.receipt_date) + ' ' + '10:00').time()):
                update_UsersToday(user)
        else:
            if parse(str(user.receipt_date)).date() == date.today():
                update_UsersToday(user)
    else:  # время меньше 19
        if parse(str(user.receipt_date)).date() == date.today():
            # Проверяем с какого приема пищи мы можем накормить пациента.
            meal_permissible, weight_meal_permissible = check_change('True')
            # Проверяем на какой прием пищи успевает пациент пациента.
            meal_user, weight_meal_user = check_meal_user(user)
            # Прием пищи с которого пациент будет добавлен в заказ.
            meal_order = meal_permissible if weight_meal_permissible >= weight_meal_user else meal_user
            # Определяем, какой след прием пищи.
            now_show_meal = get_now_show_meal()
            if meal_order == now_show_meal and meal_order != 'завтра':
                update_UsersToday(user)
            if do_messang_send(user.full_name) and meal_order != 'завтра':  # c 17 до 7 утра не отправляем сообщения
                regard = u'\u26a0\ufe0f'
                messang += f'{regard} <b>Изменение с {meal_order}</b>\n'
    messang += f'Поступил пациент {formatting_full_name(user.full_name)}\n'
    comment = add_features(user.comment,
                 user.is_probe,
                 user.is_without_salt,
                 user.is_without_lactose,
                user.is_pureed_nutrition)
    if comment:
        messang += f'Комментарий: "{comment}"'
    messang += f'({user_name})'
    if user.full_name != "Leslie William Nielsen":
        my_job_send_messang_changes.delay(messang)

@transaction.atomic
def load_menu_for_future(user, meal, change_day):
    if user.type_of_diet in ['БД день 1', 'БД день 2']:
        if type(user.receipt_date) == str:
            is_even = (change_day - parse(user.receipt_date).date() + timedelta(days=1)).days % 2 == 0
        else:
            is_even = (change_day - user.receipt_date + timedelta(days=1)).days % 2 == 0
        if user.type_of_diet == 'БД день 1':
            day = 'вторник' if is_even else 'понедельник'
            translated_diet = 'БД'
        if user.type_of_diet == 'БД день 2':
            day = 'понедельник' if is_even else 'вторник'
            translated_diet = 'БД'
    else:
        day = get_day_of_the_week(str(change_day))
        translated_diet = user.type_of_diet

    products = ProductLp.objects.filter(Q(timetablelp__day_of_the_week=day) &
                                        Q(timetablelp__type_of_diet=translated_diet) &
                                        Q(timetablelp__meals=meal))
    to_create = []
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
        products=check_value('товар', products),
    ))
    MenuByDay.objects.bulk_create(to_create)

def create_message(extra_bouillon_old, extra_bouillon_new):
    meals = {
        'breakfast': 'завтрак',
        'lunch': 'обед',
        'afternoon': 'полдник',
        'dinner': 'ужин',
    }
    result = []
    for extra_bouillon in [extra_bouillon_old, extra_bouillon_new]:
        if extra_bouillon == '':
            result.append("без доп. бульона")
        else:
            result.append(f'доп. бульон: {", ".join([meals[item] for item in extra_bouillon.split(", ")])}')
    return f'{result[0]} изменен на {result[1]}'.capitalize()


def edit_user(user_form, type, request):
    changes = []
    is_change_diet = False
    flag_add_comment = False
    flag_change_bouillon = False
    user = CustomUser.objects.get(id=user_form.data['id_edit_user'])

    # если пациента уже восстоновлен из архива
    if type == 'restore' and user.status == 'patient' or\
        type == 'edit' and user.status == 'patient_archive':
        return False
    # обравляем CustomUser и состовляем список изменений
    if user.full_name != user_form.data['full_name1']:
        changes.append(f"ФИО <b>{user.full_name}</b> изменена на <b>{user_form.data['full_name1']}</b>")
    user.full_name = formatting_full_name_mode_full(user_form.data['full_name1'])
    if user.receipt_date != datetime.strptime(user_form.data['receipt_date1'], '%d.%m.%Y').date():
        changes.append(f"дату поступления <b>{user.receipt_date}</b> изменена на <b>{datetime.strptime(user_form.data['receipt_date1'], '%d.%m.%Y').strftime('%Y-%m-%d')}</b>")
    user.receipt_date = datetime.strptime(user_form.data['receipt_date1'], '%d.%m.%Y').date()

    if user.birthdate != datetime.strptime(user_form.data['birthdate1'], '%d.%m.%Y').date():
        changes.append(f"дата рождения <b>{user.birthdate}</b> изменена на <b>{datetime.strptime(user_form.data['birthdate1'], '%d.%m.%Y').strftime('%Y-%m-%d')}</b>")
    user.birthdate = datetime.strptime(user_form.data['birthdate1'], '%d.%m.%Y').date()

    if (user.receipt_time).strftime('%H:%M') != user_form.data['receipt_time1']:
        changes.append(f"время поступления <b>{(user.receipt_time).strftime('%H:%M')}</b> изменено на <b>{user_form.data['receipt_time1']}</b>")
    user.receipt_time = parse(user_form.data['receipt_time1']).time()

    if user.department != user_form.data['department1']:
        changes.append(f"отделение <b>{user.department}</b> изменено на <b>{user_form.data['department1']}</b>")
    user.department = user_form.data['department1']

    if user.floor != user_form.data['floor1']:
        changes.append(f"этаж <b>{user.floor if user.floor != 'Не выбрано' else 'не выбран'}</b> изменен на <b>{user_form.data['floor1'] if user_form.data['floor1'] != 'Не выбрано' else 'не выбран'}</b>")
    user.floor = user_form.data['floor1'] if user_form.data['floor1'] != '' else 'Не выбрано'

    if user.room_number != user_form.data['room_number1']:
        changes.append(f"номер палаты <b>{user.room_number if user.room_number != 'Не выбрано' else 'не выбран'}</b> изменен на <b>{user_form.data['room_number1'] if user_form.data['room_number1'] != 'Не выбрано' else 'не выбран'}</b>")
    user.room_number = user_form.data['room_number1'] if user_form.data['room_number1'] != '' else 'Не выбрано'

    if user.bed != user_form.data['bed1']:
        if user.room_number != 'Не выбрано':
            changes.append(f"номер койко-места <b>{user.bed if user.bed != 'Не выбрано' else 'не выбран'}</b> изменен на <b>{user_form.data['bed1'] if user_form.data['bed1'] != 'Не выбрано' else 'не выбран'}</b>")
    user.bed = 'Не выбрано' if user_form.data['bed1'] == '' or user_form.data['room_number1'] == 'Не выбрано' else user_form.data['bed1']

    if user.type_of_diet != user_form.data['type_of_diet1']:
        changes.append(f"тип диеты <b>{user.type_of_diet}</b> изменен на <b>{user_form.data['type_of_diet1']}</b>")
        if type == 'edit':
            is_change_diet = True
        # проверяем, нужно ли чередовать диету в 19 00
        if user_form.data['type_of_diet1'] in ["БД день 1", "БД день 2"]:
            get_is_change_diet(user)
        else:
            user.is_change_diet = True
    user.type_of_diet = user_form.data['type_of_diet1']

    is_probe = False if request.POST['edit_is_probe'] == 'False' else True
    is_without_salt = False if request.POST['edit_is_without_salt'] == 'False' else True
    is_without_lactose = False if request.POST['edit_is_without_lactose'] == 'False' else True
    is_pureed_nutrition = False if request.POST['edit_is_pureed_nutrition'] == 'False' else True


    comment_formated = comment_formatting(user_form.data["comment1"])
    comment_old = add_features(
        user.comment,
        user.is_probe,
        user.is_without_salt,
        user.is_without_lactose,
        user.is_pureed_nutrition
    )
    comment_new = add_features(
        comment_formated,
        is_probe,
        is_without_salt,
        is_without_lactose,
        is_pureed_nutrition
    )


    if comment_old != comment_new:
        # Если добавили коментарий, рашьше было без комментария
        flag_add_comment = True if len(comment_old) < 2 and\
                                   len(comment_new) > 2 else False

        # changes.append(f'комментарий <b>"{user.comment if user.comment else "нет комментария"}"</b> изменен на <b>"{user_form.data["comment1"]}"</b>')
        if comment_new == "" or comment_old == "":
            if user_form.data['comment1'] == "":
                changes.append(f'комментарий <b>"{comment_old}"</b> удален')
            if comment_old == "":
                changes.append(f'добавлен комментарий <b>"{comment_new}"</b>')
        else:
            changes.append(f'комментарий <b>"{comment_old}"</b> изменен на <b>"{comment_new}"</b>')

    user.comment = comment_formated

    user.is_probe = is_probe
    user.is_without_salt = is_without_salt
    user.is_without_lactose = is_without_lactose
    user.is_pureed_nutrition = is_pureed_nutrition
    if not user.is_accompanying and request.POST['edit_is_accompanying'] == 'True':
        if request.POST['edit_type_pay'] == "petrushka":
            changes.append(f'добавлен статус <b>\"Сопровождающий\"</b> с оплатой через кассу')
        if request.POST['edit_type_pay'] == "hadassah":
            changes.append(f'добавлен статус <b>\"Сопровождающий\"</b> с оплатой за счет клиники"</b>')
    if user.is_accompanying and request.POST['edit_is_accompanying'] == 'False':
            changes.append(f'удален статус <b>\"Сопровождающий\"</b>')
    if user.is_accompanying and request.POST['edit_is_accompanying'] == 'True':
        if user.type_pay != request.POST['edit_type_pay']:
            if request.POST['edit_type_pay'] == "petrushka":
                changes.append(f'<b>оплата за счет клиники</b> изменена на <b>оплату через кассу</b>')
            if request.POST['edit_type_pay'] == "hadassah":
                changes.append(f'<b>оплата через кассу</b> изменена на <b>оплату за счет клиники</b>')
    is_accompanying = request.POST['edit_is_accompanying']
    type_pay = request.POST['edit_type_pay']
    user.is_accompanying = is_accompanying
    user.type_pay = type_pay

    extra_bouillon = []
    if request.POST['is_bouillon'] == 'True':
        for meal in ['breakfast', 'lunch', 'afternoon', 'dinner']:
            if request.POST[meal] == 'True':
                extra_bouillon.append(meal)
    extra_bouillon = ", ".join(extra_bouillon)
    if user.extra_bouillon != extra_bouillon:
        changes.append(create_message(user.extra_bouillon, extra_bouillon))
        flag_change_bouillon = True

    user.extra_bouillon = extra_bouillon

    # если надо восстановить учетную запись пациента
    if type == 'restore':
        user.status = 'patient'
    user.save()

    user_name = get_user_name(request)  # получаем имя пользователя (вносит изменения в ЛК)
    logging.info(f'пользователь ({user_name}) пациент отредактирован {user_form.data["full_name1"]}')
    for change in changes:
        logging.info(f'{change}')

    flag_is_change_diet = is_change_diet

    if type == 'restore' or flag_is_change_diet or flag_add_comment or flag_change_bouillon:
        # если добавили коммент переписываем меню для пациента на
        # следующие приемы пищи тк если есть коммент, тогда не могут быть
        # выбранны блюда по меню кафе
        add_the_patient_menu(user, type, extra_bouillon)
    regard = u'\u26a0\ufe0f'
    messang = ''
    if datetime.today().time().hour >= 19:
        if user.receipt_date == (date.today() + timedelta(days=1)) and \
                (user.receipt_time <= datetime(1, 1, 1, 10, 00).time()):
            update_UsersToday(user)
        else:
            if user.receipt_date <= date.today():
                update_UsersToday(user)
    else:  # время меньше 19
        if user.receipt_date <= date.today():
            # Проверяем с какого приема пищи мы можем накормить пациента.
            meal_permissible, weight_meal_permissible = check_change('True')
            # Проверяем на какой прием пищи успевает пациент пациента.
            meal_user, weight_meal_user = check_meal_user(user)
            # Прием пищи с которого пациент будет добавлен в заказ.
            meal_order = meal_permissible if weight_meal_permissible >= weight_meal_user else meal_user
            # Определяем, какой след прием пищи сейчас в печатных формах.
            now_show_meal = get_now_show_meal()
            if meal_order == now_show_meal and meal_order != 'завтра':
                update_UsersToday(user)
            if do_messang_send(user.full_name):  # c 17 до 7 утра не отправляем сообщения
                messang += f'{regard} <b>Изменение с {meal_order}</b>\n'
    if type == 'edit' and len(changes) > 0:
        messang += f'Отредактирован профиль пациента {formatting_full_name(user.full_name)}:\n\n'
        for change in changes:
            messang += f'- {change}\n'
        if user.full_name != "Leslie William Nielsen":
            messang += f'({user_name})'
            my_job_send_messang_changes.delay(messang)
    if type == 'restore':
        messang += f'Поступил пациент {formatting_full_name(user.full_name)} ({user.type_of_diet})\n'
        messang += f'Комментарий: "{comment_new}"' if comment_new else ''
        if user.full_name != "Leslie William Nielsen":
            messang += f'({user_name})'
            my_job_send_messang_changes.delay(messang)
    return True

def archiving_user(user, request):
    if user.status == 'patient_archive':
        return
    user.status = 'patient_archive'
    user.save()
    if user.type_of_diet in ["БД день 1", "БД день 2"]:
        get_is_change_diet(user)
    user_name = get_user_name(request)  # получаем имя пользователя (вносит изменения в ЛК)
    logging.info(f'пользователь ({user_name}), пациент перенесен в архив {user.full_name} ({user.type_of_diet})')
    update_UsersToday(user)
    MenuByDay.objects.filter(user_id=user.id).delete()
    messang = ''
    if user.receipt_date <= date.today():
        # Проверяем с какого приема пищи мы можем накормить пациента.
        meal_permissible, weight_meal_permissible = check_change('True')
        # Проверяем на какой прием пищи успевает пациент пациента.
        meal_user, weight_meal_user = check_meal_user(user)
        # Прием пищи с которого пациент будет добавлен в заказ.
        meal_order = meal_permissible if weight_meal_permissible >= weight_meal_user else meal_user

        if do_messang_send(user.full_name):  # c 17 до 7 утра не отправляем сообщения
            regard = u'\u26a0\ufe0f'
            messang += f'{regard} <b>Изменение с {meal_order}</b>\n'
    messang += f'Пациент {formatting_full_name(user.full_name)} ({user.type_of_diet}) выписан\n'
    if user.full_name != "Leslie William Nielsen":
        messang += f'({user_name})'
        my_job_send_messang_changes.delay(messang)
    return 'archived'

def add_features(comment, is_probe, is_without_salt, is_without_lactose, is_pureed_nutrition):
    """Добавляем к комментраию признаки для вывода в Сводный отчет."""
    items_comment = [f"{None if comment == '' else comment}",
                     f"{None if not is_probe else 'Питание через зонд.'}",
                     f"{None if not is_without_salt else 'Без соли.'}",
                     f"{None if not is_without_lactose else 'Без лактозы.'}",
                     f"{None if not is_pureed_nutrition else 'Протертое питание.'}",
                    ]
    items_comment = [item for item in items_comment if item != 'None']
    return  ' '.join(items_comment)

def create_with_comment(users_diet, floors):
    with_comment = []
    users_diet_with_comment = [user for user in users_diet if len(user.comment) >= 1\
                               or user.is_probe\
                               or user.is_without_salt\
                               or user.is_without_lactose\
                               or user.is_pureed_nutrition]
    for user_diet_with_comment in users_diet_with_comment:
        with_comment.append({
        "name": add_features(user_diet_with_comment.comment,
                             user_diet_with_comment.is_probe,
                             user_diet_with_comment.is_without_salt,
                             user_diet_with_comment.is_without_lactose,
                             user_diet_with_comment.is_pureed_nutrition),
        "total": 1,
        "2nd_floor": len([users_floor for users_floor in [user_diet_with_comment] \
                                  if users_floor.room_number in floors['second']]),
        "3nd_floor": len([users_floor for users_floor in [user_diet_with_comment] \
                                  if users_floor.room_number in floors['third']]),
        "4nd_floor": len([users_floor for users_floor in [user_diet_with_comment] \
                                  if users_floor.room_number in floors['fourtha']]),
        "not_floor": len([users_floor for users_floor in [user_diet_with_comment] \
                                  if users_floor.room_number in ['Не выбрано']])
    })
    list_result = []
    for index1 in range(0, len(with_comment)):
        if with_comment[index1]['name'] == None:
            continue
        result = {
            "name": with_comment[index1]['name'],
            "total": with_comment[index1]["total"],
            "2nd_floor": with_comment[index1]["2nd_floor"],
            "3nd_floor": with_comment[index1]["3nd_floor"],
            "4nd_floor": with_comment[index1]["4nd_floor"],
            "not_floor": with_comment[index1]["not_floor"],
        }
        for index2 in range(index1 + 1, len(with_comment)):
            if result['name'] == with_comment[index2]['name'] and with_comment[index2]['name'] != None:
                result["total"] = result["total"] + with_comment[index2]["total"]
                result["2nd_floor"] = result["2nd_floor"] + with_comment[index2]["2nd_floor"]
                result["3nd_floor"] = result["3nd_floor"] + with_comment[index2]["3nd_floor"]
                result["4nd_floor"] = result["4nd_floor"] + with_comment[index2]["4nd_floor"]
                result["not_floor"] = result["not_floor"] + with_comment[index2]["not_floor"]
                with_comment[index2]['name'] = None
        if result["name"] != '':
            list_result.append(result)
    return list_result

def create_without_comment(users_diet, floors, diet):
    without_comment = []
    users_diet_without_comment = [user for user in users_diet if user.comment == ''\
                                  and not user.is_probe and not user.is_without_salt\
                                  and not user.is_without_lactose and not user.is_pureed_nutrition]
    if len(users_diet) == len(users_diet_without_comment) or \
        len(users_diet_without_comment) == 0:
        return ''
    without_comment.append({
        "name": diet,
        "total": len(users_diet_without_comment),
        "2nd_floor": len([users_floor for users_floor in users_diet_without_comment \
                                  if users_floor.room_number in floors['second']]),
        "3nd_floor": len([users_floor for users_floor in users_diet_without_comment \
                                  if users_floor.room_number in floors['third']]),
        "4nd_floor": len([users_floor for users_floor in users_diet_without_comment \
                                  if users_floor.room_number in floors['fourtha']]),
        "not_floor": len([users_floor for users_floor in users_diet_without_comment \
                                  if users_floor.room_number in ['Не выбрано']])
    })
    return without_comment

def counting_diets(users, floors):
    diets_name = ['ОВД', 'ОВД без сахара', 'ЩД', 'ЩД без сахара', 'БД день 1', 'БД день 2', 'ОВД веган (пост) без глютена', 'Нулевая диета', 'ВБД', 'НКД', 'ВКД', 'Безйодовая']
    diets_count = []
    for diet in diets_name:
        users_diet = users.filter(type_of_diet=diet)
        # users_diet_with_count = [users_diet
        if len(users_diet) > 0:
            diets_count.append({
                "name": diet,
                "total": str(len(users_diet)),
                "2nd_floor": len([users_floor for users_floor in users_diet \
                                  if users_floor.room_number in floors['second']]),
                "3nd_floor": len([users_floor for users_floor in users_diet \
                                  if users_floor.room_number in floors['third']]),
                "4nd_floor": len([users_floor for users_floor in users_diet \
                                  if users_floor.room_number in floors['fourtha']]),
                "not_floor": len([users_floor for users_floor in users_diet \
                                  if users_floor.room_number in ['Не выбрано']]),
                "without_comment": create_without_comment(users_diet, floors, diet),
                "with_comment": create_with_comment(users_diet, floors)
            })

    return diets_count

def creates_dict_test(id, id_fix_user, date_show, lp_or_cafe, meal, type_order, is_public):
    """Создаем словарь с блюдами на конкретный прием пищи для пациента."""

    if type_order == 'flex-order':
        menu_all = MenuByDay.objects.filter(user_id=id)
    else:
        menu_all = MenuByDayReadyOrder.objects.filter(user_id=id_fix_user)
    menu_list = []
    menu = {
        'salad': [check_value_two(menu_all, date_show, meal, "salad", is_public)],
        'soup': [check_value_two(menu_all, date_show, meal, "soup", is_public)]+ [check_value_two(menu_all,
                                                                                                  date_show, meal,
                                                                                                  "bouillon",
                                                                                                  is_public)],
        'main': [check_value_two(menu_all, date_show, meal, "main", is_public)],
        'garnish': [check_value_two(menu_all, date_show, meal, "garnish", is_public)],
        'porridge': [check_value_two(menu_all, date_show, meal, "porridge", is_public)],
        'dessert': [check_value_two(menu_all, date_show, meal, "dessert", is_public)],
        'fruit': [check_value_two(menu_all, date_show, meal, "fruit", is_public)],
        'drink': check_value_two(menu_all, date_show, meal, "drink", is_public),
        'products': check_value_two(menu_all, date_show, meal, "products", is_public),
    }
    if lp_or_cafe == 'cafe':
        for item_category in menu.values():
            if item_category:
                for item in item_category:
                    if item:
                        if 'cafe' in item['id']:
                            menu_list.append(item.get('name'))

    if lp_or_cafe == 'lp':
        for item_category in menu.values():
            if item_category:
                for item in item_category:
                    if item:
                        if 'cafe' not in item['id']:
                            menu_list.append(item.get('name'))
    return menu_list

def create_list_users_on_floor(users, floors, meal, date_create, type_order, is_public):
    users = [user for user in users if user.room_number in floors]
    users_on_floor = []
    for user in users:
        users_on_floor.append(
            {'name': user.full_name,
             'number': '',
             'comment': add_features(user.comment,
                             user.is_probe,
                             user.is_without_salt,
                             user.is_without_lactose,
                             user.is_pureed_nutrition),
             'room_number': user.room_number,
             'bed': user.bed,
             'diet': user.type_of_diet,
             'department': user.department,
             'products_lp': creates_dict_test(user.user_id, user.id, str(date_create), 'lp', meal, type_order, is_public),
             'products_cafe': creates_dict_test(user.user_id, user.id, str(date_create), 'cafe', meal, type_order, is_public),
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

def is_active_user(user):
    """
    до 9:00 утра можно редактировать пациента с временем регистрации после 11:00
    с 9:00 до 12:00 можно редактировать пациента с временем регистрации после 14:00
    с 12:00 до 16 можно редактировать пациента с временем регистрации после 17:00
    с 16:00 до 24:00 можно редактировать пациента с временем регистрации после 21:00
    """
    receipt_datetime = parse(str(user.receipt_date) + ' ' + str(user.receipt_time))
    datetime_today = datetime.today()
    if receipt_datetime.date() > datetime_today.date():
        return user.id
    if datetime_today.hour >= 0 and datetime_today.hour < 9 and\
            receipt_datetime.time() >= datetime(1, 1, 1, 11, 0).time():
            return user.id
    if datetime_today.hour >= 9 and datetime_today.hour < 12 and\
            receipt_datetime.time() >= datetime(1, 1, 1, 14, 0).time():
            return user.id
    if datetime_today.hour >= 12 and datetime_today.hour < 16 and\
            receipt_datetime.time() >= datetime(1, 1, 1, 17, 0).time():
            return user.id
    if datetime_today.hour >= 16 and datetime_today.hour <= 24 and \
            receipt_datetime.time() >= datetime(1, 1, 1, 21, 0).time():
            return user.id

def get_not_active_users_set():
    """
    Проверяем является ли пациент активным
    в 9:00 после завтрака все пациенты которые успевают на обед(время регистрации раньше 14:00) становятся активными\
    (нет возможности редактировать дату и время)
    В кейсе (1), когда у нас заранее известно время госпитализации.
    00:00 - 10:00 вкл. поступает – с завтрака
    10:00 - 14:00 вкл. поступает – с обеда,
    14:00 - 17:00 вкл. поступает – с полдника,
    17:00 - 21:00 вкл. поступает – с ужина
    """
    users = CustomUser.objects.filter(status='patient').filter(receipt_date__gte=date.today())
    not_active_users_set = ''
    for user in users:
        if is_active_user(user):
            not_active_users_set += str(user.id) + ','
    return not_active_users_set[:-1] if len(not_active_users_set) != 0 else 'none'

def get_occupied_rooms(user_script):
    """Возвращает список с занятыми палатами."""
    double_rooms = ['2а-2', '2а-3', '2а-4', '2а-16', '2а-17', '3а-2',
                    '3а-3', '3а-4', '3а-16', '3а-17', '4а-2', '4а-3',
                    '4а-4', '4а-5', '4а-15', '4а-16']
    users = CustomUser.objects.filter(status='patient')
    not_active_users = get_not_active_users_set()
    not_active_users = not_active_users.split(',')
    # словарь с занятыми комнатами и койками
    occupied_rooms = {}
    for user in users:
        if user.bed != 'Не выбрано':
            occupied_rooms.setdefault(user.room_number, []).append(user.bed)
    if user_script == 'easy_mode':
        return occupied_rooms
     # словарь с double rooms с одной свободной койкой
    one_bed_free = {}
    for key, value in occupied_rooms.items():
        if key in double_rooms and len(value) == 1:
            one_bed_free[key] = 'К1' if value[0] == 'К2' else 'К2'

    for key in one_bed_free.keys():
        occupied_rooms.pop(key)

    if user_script == 'departments':
        return list(occupied_rooms.keys())
    if user_script == 'rooms':
        return one_bed_free
    if user_script == 'easy_mode':
        return occupied_rooms
