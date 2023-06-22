"""
В этом файле функции, которые отвечают за формирование рациона у пациентов.
"""
import pdb

from doctor.functions.bot import check_change_set
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
    if time.hour >= 9 or (time.hour == 8 and time.minute >= 31):
        if time.hour < 12 or (time.hour == 12 and time.minute < 1):
            return ['lunch', 'afternoon', 'dinner']
    if time.hour > 12 or (time.hour == 12 and time.minute >= 1):
        if time.hour < 15 or (time.hour == 15 and time.minute <= 30):
            return ['afternoon', 'dinner']
    if time.hour > 15 or (time.hour == 15 and time.minute > 30):
            if time.hour < 19 or (time.hour == 19 and time.minute == 0):
                return ['dinner']
    return []


def get_next_meals_set(user) -> list:
    """Вернет следующий прием пищи, для пациента"""

    time = user.receipt_time

    if time.hour >= 0 and time.hour < 10 or (time.hour == 10 and time.minute == 0):
        return ['breakfast', 'lunch', 'afternoon', 'dinner']
    if time.hour > 10 or (time.hour == 10 and time.minute >= 1):
        if time.hour < 14 or (time.hour == 14 and time.minute == 0):
            return ['lunch', 'afternoon', 'dinner']
    if time.hour > 14 or (time.hour == 14 and time.minute >= 1):
        if time.hour < 17 or (time.hour == 17 and time.minute == 0):
            return ['afternoon', 'dinner']
    if time.hour > 17 or (time.hour == 17 and time.minute >= 1):
            if time.hour < 21 or (time.hour == 21 and time.minute == 0):
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
        # делаем проверку: входит ли дата и время регистрации в диапазон даты и времени приема пищи
        if user.receipt_date > change_day:
            continue
        # если дата регистрации совпадает с датой приема пищи и не сегодня,
        # тогда выясняем с какого приема пищи начинать формировать меню
        elif user.receipt_date == change_day and user.receipt_date != date.today():
            # тут функция, которая возвращает список с пиемами пищи,
            # с которого нужно начинать формировать меню
            next_meals = get_next_meals_set(user)
        elif user.receipt_date == change_day and user.receipt_date == date.today():
            # оставляем приемы пищи, которые вернули обе функции
            next_meals = list(set(get_next_meals_set(user)) & set(check_change_set()))

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


@transaction.atomic
def add_the_patient_emergency_food_to_the_database(user, date_add, meal, extra_bouillon):
    """

    Добавляет в БД экстренное питание для пациента на один прием пищи.
    """
    day: str = ''
    if user.type_of_diet == 'БД день 1':
        day = 'понедельник'
    if user.type_of_diet == 'БД день 2':
        day = 'вторник'

    if not day:
        day = get_day_of_the_week(date_add)
    # нужно удалить старое меню
    MenuByDay.objects.filter(user_id=user.id).filter(date=date.today()).filter(meal=meal).delete()
    MenuByDayReadyOrder.objects.filter(user_id=UsersReadyOrder.objects.filter(user_id=user.id).first()).filter(date=date.today()).filter(meal=meal).delete()
    products = ProductLp.objects.filter(Q(timetablelp__day_of_the_week=day) &
                                        Q(timetablelp__type_of_diet=user.type_of_diet) &
                                        Q(timetablelp__meals=meal))

    products_id: list = [] # список id продуктов, отсортированнвый по категориям
    category = ['каша', 'салат', 'суп', 'основной', 'гарнир', 'десерт', 'напиток', 'фрукты', 'товар', 'hidden']
    for cat in category:
        for product in products.filter(category=cat):
            products_id.append(product.id)

    # products_id
    MenuByDay(
        user_id=user,
        date=date_add,
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
        bouillon=f"{'426' if extra_bouillon else ''}"
    ).save()


    if UsersReadyOrder.objects.filter(user_id=user.id).exists():
        UsersReadyOrder(
                user_id=user.id,
                date_create=date.today(),
                full_name=user.full_name,
                floor=user.floor,
                bed=user.bed,
                receipt_date=user.receipt_date,
                receipt_time=user.receipt_time,
                department=user.department,
                room_number=user.room_number,
                type_of_diet=user.type_of_diet,
                comment=user.comment,
                status=user.status,
                is_accompanying=user.is_accompanying,
                is_probe=user.is_probe,
                is_without_salt=user.is_without_salt,
                is_without_lactose=user.is_without_lactose,
                is_pureed_nutrition=user.is_pureed_nutrition,
                type_pay=user.type_pay,
            ).save()
    else:
        UsersReadyOrder.objects.filter(user_id=user.id).update(type_of_diet=user.type_of_diet)

    menu = MenuByDay.objects.filter(user_id=user.id).filter(date=date.today()).filter(meal=meal)
    if menu.exists():
        MenuByDayReadyOrder(user_id=UsersReadyOrder.objects.filter(user_id=user.id).first(),
                            date_create=date.today(),
                            date=menu[0].date,
                            meal=menu[0].meal,
                            main=menu[0].main,
                            garnish=menu[0].garnish,
                            porridge=menu[0].porridge,
                            soup=menu[0].soup,
                            dessert=menu[0].dessert,
                            fruit=menu[0].fruit,
                            drink=menu[0].drink,
                            salad=menu[0].salad,
                            products=menu[0].products,
                            hidden=menu[0].hidden,
                            bouillon=menu[0].bouillon).save()
    return products_id

def get_meal_emergency_food(r_date, r_time):
    """
    Возвращает прием пищи на который можно заказать экстренное питание:
    8:30 до 10:00 - могут заказать завтрак
    12:00 до 14:00 - могут заказать обед
    15:30 до 16:30 - могут заказать полдник
    Нужно чтобы время и время регистации пациенат были в одном диапазоне
    """
    time = datetime.today().time()
    if r_date == date.today():
        if time.hour == 9 or (time.hour == 8 and time.minute >= 30) or (time.hour == 10 and time.minute == 00):
            if r_time.hour == 9 or (r_time.hour == 8 and r_time.minute >= 30) or \
                (r_time.hour == 10 and r_time.minute == 00):
                return 'breakfast'

        if time.hour >= 12 and time.hour < 14 or time.hour == 14 and time.minute == 00:
            if r_time.hour >= 12 and r_time.hour < 14 or (r_time.hour == 14 and r_time.minute == 00):
                return 'lunch'

        # pdb.set_trace()
        if (time.hour == 15 and time.minute >= 30) or (time.hour == 16 and time.minute <= 30):
            if r_time.hour == 15 and r_time.minute >= 30 or (r_time.hour == 16 and r_time.minute <= 30):
                return 'afternoon'
    return False

def get_meal_emergency_food(r_date=datetime.today().date(), r_time=datetime.today().time()):
    """
    Возвращает прием пищи на который можно заказать экстренное питание:
    8:30 до 10:00 - могут заказать завтрак
    12:00 до 14:00 - могут заказать обед
    15:30 до 16:30 - могут заказать полдник
    Нужно чтобы время и время регистации пациенат были в одном диапазоне
    """
    time = datetime.today().time()
    if r_date == date.today():
        if time.hour == 9 or (time.hour == 8 and time.minute >= 30) or (time.hour == 10 and time.minute == 00):
            if r_time.hour == 9 or (r_time.hour == 8 and r_time.minute >= 30) or \
                (r_time.hour == 10 and r_time.minute == 00):
                return 'breakfast'

        if time.hour >= 12 and time.hour < 14 or time.hour == 14 and time.minute == 00:
            if r_time.hour >= 12 and r_time.hour < 14 or (r_time.hour == 14 and r_time.minute == 00):
                return 'lunch'

        # pdb.set_trace()
        if (time.hour == 15 and time.minute >= 30) or (time.hour == 16 and time.minute <= 30):
            if r_time.hour == 15 and r_time.minute >= 30 or (r_time.hour == 16 and r_time.minute <= 30):
                return 'afternoon'
    return False
