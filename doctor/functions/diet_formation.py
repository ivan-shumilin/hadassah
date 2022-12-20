"""
В этом файле функции, которые отвечают за формирование рациона у пациентов.
"""
from nutritionist.models import ProductLp, CustomUser, MenuByDay, Product, BotChatId,\
    UsersToday, MenuByDayReadyOrder, UsersReadyOrder
from doctor.functions.helpers import check_value, get_day_of_the_week
from django.db import transaction
from django.db.models import Q
from dateutil.parser import parse
from datetime import datetime, date, timedelta
from django.utils import dateformat


# def check_value(category, products):
#     value: str = ''
#     if category != 'товар' and category != 'напиток':
#         try:
#             value = products.get(category=category).id
#         except Exception:
#             value = None
#     else:
#         value = ','.join([str(item.id) for item in products.filter(category=category)])
#     return value
#
# def get_day_of_the_week(date_get):
#     """Дату в формате Y-M-D в день недели прописью"""
#
#     DAT_OF_THE_WEEK = {
#         'Monday': 'понедельник',
#         'Tuesday': 'вторник',
#         'Wednesday': 'среда',
#         'Thursday': 'четверг',
#         'Friday': 'пятница',
#         'Saturday': 'суббота',
#         'Sunday': 'воскресенье',
#     }
#     return DAT_OF_THE_WEEK[parse(date_get).strftime('%A')]
def add_menu_three_days_ahead():
    """ Добовляем меню на 3 дня. """
    users = CustomUser.objects.filter(status='patient')
    days = [date.today() + timedelta(days=delta) for delta in [0, 1, 2]]
    for user in users:
        menu_all = MenuByDay.objects.filter(user_id=user.id)
        for index, day in enumerate(days):
            if len(menu_all.filter(date=str(day))) == 0 and (day >= user.receipt_date):
                for change_day in days[index:]:
                    add_default_menu_on_one_day(change_day, user)
    return

def add_default_menu(user):
    """
    Заполняем MenuByDay.
    В MenuByDay хранится перечень блюд для пациента в определенный день, прием пищи.
    """
    # генератор списка return даты на след 3 дня
    days = [parse(user.receipt_date) + timedelta(days=delta) for delta in [0, 1, 2]]

    for index, day_of_the_week in enumerate(days):
        add_default_menu_on_one_day(day_of_the_week, user)
    return


@transaction.atomic
def add_default_menu_on_one_day(day_of_the_week, user):
    if user.type_of_diet in ['БД день 1', 'БД день 2']:
        is_even = (day_of_the_week - parse(user.receipt_date) + timedelta(days=1)).days % 2 == 0
        if user.type_of_diet == 'БД день 1':
            day = 'вторник' if is_even else 'понедельник'
            translated_diet = 'БД'
        if user.type_of_diet == 'БД день 2':
            day = 'понедельник' if is_even else 'вторник'
            translated_diet = 'БД'
    else:
        day = get_day_of_the_week(str(day_of_the_week))
        translated_diet = user.type_of_diet
    for meal in ['breakfast', 'lunch', 'afternoon', 'dinner']:
        products = ProductLp.objects.filter(Q(timetablelp__day_of_the_week=day) &
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
            products=check_value('товар', products),
            ))
        MenuByDay.objects.bulk_create(to_create)
    return