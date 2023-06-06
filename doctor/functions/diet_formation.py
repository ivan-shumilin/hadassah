"""
В этом файле функции, которые отвечают за формирование рациона у пациентов.
"""
import pdb

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
    """Вернет следующий прием пищи."""

    time = datetime.today().time()

    if time.hour >= 0 and time.hour < 8 or (time.hour == 8 and time.minute <= 30):
        return ['breakfast', 'lunch', 'afternoon', 'dinner']
    if time.hour > 9 or (time.hour == 8 and time.minute >= 31):
        if time.hour < 12 or (time.hour == 12 and time.minute < 1):
            return ['lunch', 'afternoon', 'dinner']
    if time.hour > 12 or (time.hour == 12 and time.minute >= 1):
        if time.hour < 15 or (time.hour == 15 and time.minute <= 30):
            return ['afternoon', 'dinner']
    if time.hour > 15 or (time.hour == 15 and time.minute > 30):
            if time.hour < 19 or (time.hour == 19 and time.minute == 0):
                return ['dinner']
    return []

def add_the_patient_menu(user, user_change_type, extra_bouillon):
    """
    Если поменялась диета или добавили комментарий.
    Удаляем все меню в будущем и добавляем новое.
    """
    extra_bouillon = extra_bouillon.split(", ")
    next_meals = get_next_meals()

    if next_meals == []:
        days = [date.today() + timedelta(days=delta) for delta in [0, 1, 2, 3]]
    else:
        days = [date.today() + timedelta(days=delta) for delta in [0, 1, 2]]

    if user_change_type == 'edit':
        delete_menu_for_future(user, days, next_meals)

    writes_the_patient_menu_to_the_database(user, days, next_meals, extra_bouillon)

def add_menu_three_days_ahead():
    """
    Добовляем меню на 3 дня.
    """
    users = CustomUser.objects.filter(status='patient')
    days = [date.today() + timedelta(days=delta) for delta in [0, 1, 2]]
    for user in users:
        menu_all = MenuByDay.objects.filter(user_id=user.id)
        # порядок дней для формирования меню (БД)
        if user.type_of_diet == 'БД день 1':
            days_for_bd = ['понедельник', 'понедельник', 'понедельник']
        elif user.type_of_diet == 'БД день 2':
            days_for_bd = ['вторник', 'вторник', 'вторник']
        else:
            days_for_bd = []
        for index, day in enumerate(days):
            if len(menu_all.filter(date=str(day))) == 0 and (day >= user.receipt_date):
                for change_day in days[index:]:
                    add_default_menu_on_one_day(change_day, user, index, days_for_bd)
    return

@transaction.atomic
def add_default_menu_on_one_day(day_of_the_week, user, index, days_for_bd):
    if days_for_bd:
        day = days_for_bd[index]
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
            hidden=check_value('hidden', products),
            bouillon=f'{"426" if meal in user.extra_bouillon.strip(", ") else ""}'
            ))
        MenuByDay.objects.bulk_create(to_create)
    return


@transaction.atomic
def writes_the_patient_menu_to_the_database(user, days, next_meals, extra_bouillon):
    # если пациент не попал на последний прием пищи (ужин) тогда на следующий день не
    # происходи чередование диет
    if next_meals == [] and user.type_of_diet in ['БД день 1', 'БД день 2']:
        # порядок дней для формирования меню (БД)
        if user.type_of_diet == 'БД день 1':
            days_for_bd = ['понедельник', 'понедельник', 'понедельник', 'понедельник']
        if user.type_of_diet == 'БД день 2':
            days_for_bd = ['вторник', 'вторник', 'вторник', 'вторник']
    if next_meals:
        # порядок дней для формирования меню (БД)
        if user.type_of_diet == 'БД день 1':
            days_for_bd = ['понедельник', 'понедельник', 'понедельник']
        if user.type_of_diet == 'БД день 2':
            days_for_bd = ['вторник', 'вторник', 'вторник']


    for index, change_day in enumerate(days):
        next_meals = next_meals if index == 0 else ['breakfast', 'lunch', 'afternoon', 'dinner']
        for meal in next_meals:
            if user.type_of_diet in ['БД день 1', 'БД день 2']:
                day = days_for_bd[index]
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
                bouillon=f"{'426' if meal in extra_bouillon else ''}"
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
    """
    Возвращает queryset c пациентами, которые попадают в заявку на приготовление блюд
    на конкретный прием пищи.
    """
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


def update_diet_bd():
    """
    Обновляет БД диету у пациента по след. правилам:
    1. меняется как и все диеты (можно менять за 2 часа до приема пищи)
    2. в 19:00 происходит чередование с БД-1 на БД-2 и наоборот.
    3. если поменяли после 17 (после попадания на последний прием), тогда на следующий день не меняем.
    Допустим поменяли в 16:30 с ОВД на БД-1, на ужин будет БД-1, на следующий день БД-2
    А если в 17:30 с ОВД на БД-1, тогда на следующий день будет БД-1 (не меняем)
    """

    patients = CustomUser.objects.filter(status="patient")
    patients_with_bd_diet = patients.filter(Q(type_of_diet="БД день 1") | Q(type_of_diet="БД день 2"))
    for patient in patients_with_bd_diet:
        if patient.is_change_diet_bd:
            patient.type_of_diet = "БД день 1" if patient.type_of_diet == "БД день 2" else "БД день 2"
        patient.save()

    for patient in patients:
        patient.is_change_diet_bd = True
        patient.save()
    return