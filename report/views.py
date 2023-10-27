import datetime
from datetime import datetime, date, timedelta
from django.utils import dateformat
import random



from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render

from doctor.functions.functions import get_order_status, check_value_two, formatting_full_name
from doctor.views import group_doctors_check
from nutritionist.models import UsersReadyOrder, MenuByDayReadyOrder, MenuByDay, UsersToday


def get_menu_for_patient_on_meal(menu_all, date_show, meal, id, order_status):
    menu = {
        'main': check_value_two(menu_all, date_show, meal, "main", id, is_public=False),
        'garnish': check_value_two(menu_all, date_show, meal, "garnish", id, is_public=False),
        'porridge': check_value_two(menu_all, date_show, meal, "porridge", id, is_public=False),
        'soup': check_value_two(menu_all, date_show, meal, "soup", id, is_public=False),
        'dessert': check_value_two(menu_all, date_show, meal, "dessert", id, is_public=False),
        'fruit': check_value_two(menu_all, date_show, meal, "fruit", id, is_public=False),
        'drink': check_value_two(menu_all, date_show, meal, "drink", id, is_public=False),
        'salad': check_value_two(menu_all, date_show, meal, "salad", id, is_public=False),
        'products': check_value_two(menu_all, date_show, meal, "products", id, is_public=False),
        'hidden': check_value_two(menu_all, date_show, meal, "hidden", id, is_public=False),
        'bouillon': check_value_two(menu_all, date_show, meal, "bouillon", id, is_public=False),
        'order_status': order_status,
    }

    # если основное блюдо с гарниром и тогда:
    # берем первое блюдо основное и прибавляем к нему все гарниры, которые есть
    try:
        if menu['main'][0]['with_garnish'] == False:
            for garnish in menu['garnish']:
                menu['main'][0]['name'] += f' + {garnish["name"]}'
            menu['garnish'] = [None]
    except:
        pass
    return menu


def combine_result(res: dict, intermediate_result: dict, patient) -> dict:
    """Обьединяет полученный результат (промежуточный) с основным."""
    floor = '0' if patient.floor == 'Не выбрано' else patient.floor
    CATEGOTYS = ['salad', 'soup', 'bouillon', 'main', 'garnish', 'porridge', 'dessert', 'fruit', 'drink', 'products',
                 'hidden']
    patient_data = f'{formatting_full_name(patient.full_name)}, {patient.type_of_diet}, {patient.floor} этаж'
    for cat in CATEGOTYS:
        for product in intermediate_result[cat]:
            if product:
                if product['name'] not in res[cat]:
                    product['id'] = random.randint(0, 10000000)
                    product['all_floor'] = 1
                    product[f'2nd_floor'] = 0
                    product[f'3nd_floor'] = 0
                    product[f'4nd_floor'] = 0
                    product[f'0nd_floor'] = 0
                    product['patient_name'] = [patient_data]
                    product[f'{floor}nd_floor'] = 1
                    res[cat][product['name']] = product
                else:
                    res[cat][product['name']]['patient_name'].append(patient_data)
                    res[cat][product['name']]['all_floor'] += 1
                    res[cat][product['name']][f'{floor}nd_floor'] += 1

    return res

def creates_dict_with_menu_patients_dish_assembly_report(date_show: datetime) -> dict:
    """"""
    menu: dict = {}

    MEALS = ['breakfast', 'lunch', 'afternoon', 'dinner']
    CATEGOTYS = ['salad', 'soup', 'bouillon', 'main', 'garnish', 'porridge', 'dessert', 'fruit', 'drink', 'products',
                  'hidden']

    # инициализируем словарь
    result: dict = {}
    for meal in MEALS:
        result[meal] = {}
        for cat in CATEGOTYS:
            result[meal][cat] = {}

    for meal in ['breakfast', 'lunch', 'afternoon', 'dinner']:
        menu[meal] = {}
        order_status: str = get_order_status(meal, date_show)

        if order_status == 'fix-order':
            menu_qs = MenuByDayReadyOrder.objects.all()
            users_qs = UsersReadyOrder.objects.all()

            for user in users_qs:
                key = user.user_id
                menu[meal][key] = {}
                menu_all = menu_qs.filter(user_id=user)
                menu[meal][key] = get_menu_for_patient_on_meal(menu_all, date_show, meal, id, order_status)
                result[meal] = combine_result(result[meal], menu[meal][key], user)

        if order_status in ['flex-order', 'done']:
            menu_qs = MenuByDay.objects.all()
            users_qs = UsersToday.objects.all()

            for user in users_qs:
                key = user.user_id
                menu[meal][key] = {}
                menu_all = menu_qs.filter(user_id=user.user_id)
                menu[meal][key] = get_menu_for_patient_on_meal(menu_all, date_show, meal, id, order_status)
                result[meal] = combine_result(result[meal], menu[meal][key], user)

    return result


@login_required(login_url='login')
@user_passes_test(group_doctors_check, login_url='login')
def dish_assembly_report(request):
    formatted_date_now = dateformat.format(date.fromisoformat(str(date.today())), 'd E, l')
    time_now = datetime.today().time().strftime("%H:%M")
    day = 'tomorrow' if datetime.now().time().hour >= 19 else 'today'
    date_create = date.today() + timedelta(days=1) if day == 'tomorrow' else date.today()
    CATEGOTYS = ['salad', 'soup', 'bouillon', 'main', 'garnish', 'porridge', 'dessert', 'fruit', 'drink', 'products',
                  'hidden']
    # нужно для каждого приема пищи определить type_order

    result = creates_dict_with_menu_patients_dish_assembly_report(date_create)

    # сортируем result по алфавиту
    for meal_key in result.keys():
        for cat_key in result[meal_key].keys():
            result[meal_key][cat_key] = dict(sorted(result[meal_key][cat_key].items()))

    data = {
        'result': result,
        'formatted_date': formatted_date_now,
        'time_now': time_now,
        'CATEGOTYS': CATEGOTYS,
        'day': day,
        'date_create': dateformat.format(date.fromisoformat(str(date_create)), 'd E')
    }
    return render(request, 'dish_assembly_report.html', context=data)