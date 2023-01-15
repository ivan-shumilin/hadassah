"""
В этом файле функции, которые отвечают за формирование рациона у пациентов.
"""
from nutritionist.models import ProductLp, CustomUser, MenuByDay, Product, BotChatId,\
    UsersToday, MenuByDayReadyOrder, UsersReadyOrder
from doctor.functions.helpers import check_value
from doctor.functions.translator import get_day_of_the_week
from django.db import transaction
from django.db.models import Q
from dateutil.parser import parse
from datetime import datetime, date, timedelta
from django.utils import dateformat


def get_next_meals():
    """ Вернет следующий прием пищи. """
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

def add_the_patient_menu(user, user_change_type):
    """ Если поменялась диета или добавили комментарий.
        Удаляем все меню в будущем и добавляем новое.
     """
    next_meals = get_next_meals()

    if next_meals == []:
        days = [date.today() + timedelta(days=delta) for delta in [0, 1, 2, 3]]
    else:
        days = [date.today() + timedelta(days=delta) for delta in [0, 1, 2]]

    if user_change_type == 'edit':
        delete_menu_for_future(user, days, next_meals)

    writes_the_patient_menu_to_the_database(user, days, next_meals)

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
    days = [user.receipt_date + timedelta(days=delta) for delta in [0, 1, 2]]

    for index, day_of_the_week in enumerate(days):
        add_default_menu_on_one_day(day_of_the_week, user)
    return

@transaction.atomic
def add_default_menu_on_one_day(day_of_the_week, user):
    if user.type_of_diet in ['БД день 1', 'БД день 2']:
        if type(user.receipt_date) == str:
            is_even = (day_of_the_week - parse(user.receipt_date) + timedelta(days=1)).days % 2 == 0
        else:
            is_even = (day_of_the_week - user.receipt_date + timedelta(days=1)).days % 2 == 0
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


@transaction.atomic
def writes_the_patient_menu_to_the_database(user, days, next_meals):
    for index, change_day in enumerate(days):
        next_meals = next_meals if index == 0 else ['breakfast', 'lunch', 'afternoon', 'dinner']
        for meal in next_meals:
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
    return

def delete_menu_for_future(user, days, next_meals):
    for index, change_day in enumerate(days):
        next_meals = next_meals if index == 0 else ['breakfast', 'lunch', 'afternoon', 'dinner']
        for meal in next_meals:
            set_menu_del = MenuByDay.objects.filter(user_id=user.id).filter(date=str(change_day)).filter(meal=meal)
            for menu_del in set_menu_del:
                menu_del.delete()


def get_users_on_the_meal(meal):
    """ Возвращает queryset c пациентами, которые попадают в заявку на приготовление блюд
        на конкретный прием пищи. """
    if meal == 'breakfast':
        users = CustomUser.objects.filter(status='patient') \
            .filter(Q(receipt_date__lt=date.today()) | Q(receipt_date=date.today()) & Q(receipt_time__lte='10:00'))

    if meal == 'lunch':
        users = CustomUser.objects.filter(status='patient') \
            .filter(Q(receipt_date__lt=date.today()) | Q(receipt_date=date.today()) & Q(receipt_time__lte='14:00'))

    if meal == 'afternoon':
        users = CustomUser.objects.filter(status='patient') \
            .filter(Q(receipt_date__lt=date.today()) | Q(receipt_date=date.today()) & Q(receipt_time__lte='17:00'))

    if meal == 'dinner':
        users = CustomUser.objects.filter(status='patient') \
            .filter(Q(receipt_date__lt=date.today()) | Q(receipt_date=date.today()) & Q(receipt_time__lte='21:00'))

    if meal == 'tomorrow':
        tomorrow = date.today() + timedelta(days=1)
        users = CustomUser.objects.filter(status='patient').\
            filter(Q(receipt_date__lte=date.today()) | Q(receipt_date__lte=tomorrow) & Q(receipt_time__lte='10:00'))

    return users
