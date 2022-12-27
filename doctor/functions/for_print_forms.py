from nutritionist.models import CustomUser, UsersToday, СhangesUsersToday, UsersReadyOrder,\
    MenuByDayReadyOrder, MenuByDay, Report, ProductLp, TimetableLp
import datetime, json
from datetime import datetime, date, timedelta
from django.db import transaction
from django.db.models import Q

def check_change_time(user):
    """Проверка с какого приема пищи изменения вступят в силу"""
    if datetime.today().time().hour >= 0 and datetime.today().time().hour < 10:
        return 'зактрака'
    if datetime.today().time().hour >= 10 and datetime.today().time().hour < 13:
        return 'обеда'
    if datetime.today().time().hour >= 13 and datetime.today().time().hour < 17:
        return 'полдника'
    if datetime.today().time().hour >= 17 and datetime.today().time().hour < 21:
        return 'ужина'
    return None


@transaction.atomic
def create_user_today(meal):
    # сделать в 00:00 каждый день
    """Создает таблицу со всеми пользователями,
       которые уже поступили или поступят сегодня.
       В 7, 9, 12, 16
       0 - 10 поступает с завтрака,
       10 - 13 поступает с обеда,
       13 - 17 поступает с полдника,
       17 - 00 поступает с ужина """
    to_create = []
    # В зависимости от приема пищи добавляем разных пациентов в UsersToday
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


    UsersToday.objects.all().delete()
    for user in users:
        to_create.append(UsersToday(
            user_id=user.id,
            date_create=date.today(),
            full_name=user.full_name,
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
            ))
    UsersToday.objects.bulk_create(to_create)

@transaction.atomic
def create_ready_order(meal):
    to_create = []
    # В зависимости от приема пищи добавляем разных пациентов в UsersToday
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


    UsersReadyOrder.objects.all().delete()
    for user in users:
        to_create.append(UsersReadyOrder(
            user_id=user.id,
            date_create=date.today(),
            full_name=user.full_name,
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
            ))
    UsersReadyOrder.objects.bulk_create(to_create)
    to_create = []
    for user in users:
        menu = MenuByDay.objects.filter(user_id=user.id).filter(date=date.today()).filter(meal=meal)
        to_create.append(MenuByDayReadyOrder(user_id=UsersReadyOrder.objects.get(user_id=user.id),
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
                                products=menu[0].products))
    MenuByDayReadyOrder.objects.bulk_create(to_create)


@transaction.atomic
def create_report(meal):
    """
    Принимает: название приема пищи.
    Создает отчет по проданным блюдам.
    """
    to_create = []
    # В зависимости от приема пищи добавляем разных пациентов в UsersToday
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

    report_dict = {}
    for user in users:
        menu = MenuByDay.objects.filter(user_id=user.id).filter(date=date.today()).filter(meal=meal)
        products = [menu[0].main, menu[0].garnish, menu[0].porridge, menu[0].soup, menu[0].dessert, menu[0].fruit, menu[0].drink, menu[0].salad]
        products = [product for product in products if product not in ['', None, 'None']]
        report_dict[user.id] = {'type_of_diet': user.type_of_diet,
                                  'meal': meal,
                                  'products': products}

    to_create = []
    for user, value in report_dict.items():
        for product in value['products']:
            to_create.append(Report(user_id=CustomUser.objects.get(id=user),
                                    date_create=date.today(),
                                    meal=value['meal'],
                                    product_id=product,
                                    type_of_diet=value['type_of_diet']))
    Report.objects.bulk_create(to_create)




@transaction.atomic
def create_user_tomorrow():
    """Создает таблицу со всеми пользователями,
       которые уже поступили или поступят завтра."""
    to_create = []
    tomorrow = date.today() + timedelta(days=1)
    users = CustomUser.objects.filter(status='patient').filter(receipt_date__lte=tomorrow)
    users = users.filter(receipt_time__lte='10:00')
    UsersToday.objects.all().delete()
    for user in users:
        to_create.append(UsersToday(
            user_id=user.id,
            date_create=date.today(),
            full_name=user.full_name,
            receipt_date=user.receipt_date,
            receipt_time=user.receipt_time,
            department=user.department,
            room_number=user.room_number,
            type_of_diet=user.type_of_diet,
            comment=user.comment,
            status=user.status,
            ))
    UsersToday.objects.bulk_create(to_create)

def check_time():
    """
    Проверяет время, есть два варианта:
    True: изменения внести сразу,
    False: изменения внести потом.
    00 00 - 07 00 True
    07 00 - 09 00 False
    09 00 - 11 00 True
    11 00 - 13 00 False
    13 00 - 14 00 True
    14 00 - 16 00 False
    16 00 - 17 00 True
    17 00 - 19 00 False
    19 00 - 00 00 True
    """
    time = datetime.today().time().hour
    if (time >= 7 and time < 9) \
        or (time >= 11 and time < 13) \
        or (time >= 14 and time < 16) \
        or (time >= 17 and time < 19):
        return False
    return True

def update_UsersToday(user):
    if user.status == 'patient_archive':
        try:
            user_today = UsersToday.objects.get(user_id=user.id)
            user_today.delete()
        except:
            pass
    else:
        try:
            user_today = UsersToday.objects.get(user_id=user.id)
            user_today.date_create=date.today()
            user_today.full_name=user.full_name
            user_today.bed=user.bed
            user_today.receipt_date=user.receipt_date
            user_today.receipt_time=user.receipt_time
            user_today.department=user.department
            user_today.room_number=user.room_number
            user_today.type_of_diet=user.type_of_diet
            user_today.comment=user.comment
            user_today.status=user.status
            user_today.is_accompanying=user.is_accompanying
            user_today.is_probe=user.is_probe
            user_today.is_without_salt=user.is_without_salt
            user_today.is_without_lactose=user.is_without_lactose
            user_today.is_pureed_nutrition = user.is_pureed_nutrition
            user_today.type_pay=user.type_pay
            user_today.save()
        except:
            UsersToday(user_id=user.id,
            date_create=date.today(),
            full_name=user.full_name,
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
            type_pay=user.type_pay).save()
    return


@transaction.atomic
def update_СhangesUsersToday(user):
    to_create = []
    to_create.append(СhangesUsersToday(
        user_id=user.id,
        date_create=date.today(),
        full_name=user.full_name,
        receipt_date=user.receipt_date,
        receipt_time=user.receipt_time,
        department=user.department,
        room_number=user.room_number,
        type_of_diet=user.type_of_diet,
        comment=user.comment,
        status=user.status
        ))
    СhangesUsersToday.objects.bulk_create(to_create)


def applies_changes():
    """Изменения из СhangesUsersToday применяеться к UsersToday."""
    users_changes = СhangesUsersToday.objects.all()
    users_today = UsersToday.objects.all()
    for user in users_changes:
        try:
            user_today = users_today.get(user_id=user.user_id)
            if user.status == 'patient_archive' or user.receipt_date > date.today():
                user_today.delete()
                continue
            user_today.user_id = user.user_id
            user_today.date_create = user.date_create
            user_today.full_name = user.full_name
            user_today.receipt_date = user.receipt_date
            user_today.receipt_time = user.receipt_time
            user_today.department = user.department
            user_today.room_number = user.room_number
            user_today.type_of_diet = user.type_of_diet
            user_today.comment = user.comment
            user_today.status = user.status
            user_today.save()
        except:
            UsersToday(user_id=user.user_id,
                       date_create=user.date_create,
                       full_name=user.full_name,
                       receipt_date=user.receipt_date,
                       receipt_time=user.receipt_time,
                       department=user.department,
                       room_number=user.room_number,
                       type_of_diet=user.type_of_diet,
                       comment=user.comment,
                       status=user.status).save()
    users_changes.delete()


@transaction.atomic
def create_products_lp():
    """Создает таблицу продуктами лечебного питания."""
    # записать json в python-обьект
    with open('products_lp.json') as json_file:
        products = json.load(json_file)
    to_create = []

    # ProductLp.objects.all().delete()
    for product in products:
        to_create.append(ProductLp(
            name=product['name'],
            fat=product['fat'] if 'fat' in product else 0,
            carbohydrate=product['carbohydrate'] if 'carbohydrate' in product else 0,
            fiber=product['fiber'] if 'fiber' in product else 0,
            energy=product['energy'] if 'energy' in product else 0,
            image=None,
            description=product['composition'],
            category=product['category'],
            comment=None,
            weight=product['weight'] if 'weight' in product else 0,
            number_tk=product['number_tk'],
            status='1'
            ))
    ProductLp.objects.bulk_create(to_create)


@transaction.atomic
def add_products_lp():
    """Создает таблицу продуктами лечебного питания."""
    to_create = []
    days = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье']
    meals = ['breakfast', 'lunch', 'afternoon', 'dinner']
    diets = ['ОВД', 'ОВД без сахара', 'ОВД веган (пост) без глютена', 'Нулевая диета', 'БД день 1', 'БД день 2', 'ЩД', 'ВБД', 'НКД', 'ВКД']
    product = ProductLp.objects.get(name='Вода "Jеvea" 0,51л.')
    for diet in diets:
        for day in days:
            for meal in meals:
                    to_create.append(TimetableLp(
                        item=product,
                        type_of_diet=diet,
                        day_of_the_week=day,
                        meals=meal,
                        ))
    # TimetableLp.objects.bulk_create(to_create)
    # добавляем джем
    product = ProductLp.objects.get(name='Джем порционный 20 гр. в асс.')
    for diet in ['ОВД', 'ОВД веган (пост) без глютена', 'ЩД', 'ВБД', 'ВКД']:
        for day in days:
            for meal in ['breakfast']:
                    to_create.append(TimetableLp(
                        item=product,
                        type_of_diet=diet,
                        day_of_the_week=day,
                        meals=meal,
                        ))
    # TimetableLp.objects.bulk_create(to_create)
    # добавляем черный хлеб
    product = ProductLp.objects.get(name='Хлеб бородинский/ржаной 20 гр.')
    for diet in ['ОВД', 'ОВД без сахара', 'ОВД веган (пост) без глютена', 'ВБД', 'ВКД']:
        for day in days:
            for meal in ['breakfast', 'lunch', 'dinner']:
                    to_create.append(TimetableLp(
                        item=product,
                        type_of_diet=diet,
                        day_of_the_week=day,
                        meals=meal,
                        ))
    # TimetableLp.objects.bulk_create(to_create)
    for diet in ['НКД']:
        for day in days:
            for meal in ['lunch']:
                    to_create.append(TimetableLp(
                        item=product,
                        type_of_diet=diet,
                        day_of_the_week=day,
                        meals=meal,
                        ))
    # TimetableLp.objects.bulk_create(to_create)
    # добавляем белый хлеб
    product = ProductLp.objects.get(name='Булочка французская 35гр. в асс.')
    for diet in ['ОВД', 'ЩД', 'ВБД', 'ВКД']:
        for day in days:
            for meal in ['breakfast', 'lunch', 'dinner']:
                    to_create.append(TimetableLp(
                        item=product,
                        type_of_diet=diet,
                        day_of_the_week=day,
                        meals=meal,
                        ))
    # TimetableLp.objects.bulk_create(to_create)
    # добавляем масло
    product = ProductLp.objects.get(name='Масло сливочное порц.10г')
    for diet in ['ОВД', 'ОВД без сахара', 'ЩД','ВБД', 'ВКД']:
        for day in days:
            for meal in ['breakfast']:
                    to_create.append(TimetableLp(
                        item=product,
                        type_of_diet=diet,
                        day_of_the_week=day,
                        meals=meal,
                        ))
    TimetableLp.objects.bulk_create(to_create)
