from nutritionist.models import CustomUser, UsersToday, СhangesUsersToday
import datetime
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
            .filter(receipt_date__lte=date.today()) \
            .filter(receipt_time__lte='10:00')

    if meal == 'lunch':
        users = CustomUser.objects.filter(status='patient') \
            .filter(receipt_date__lte=date.today()) \
            .filter(receipt_time__lte='14:00')

    if meal == 'afternoon':
        users = CustomUser.objects.filter(status='patient') \
            .filter(receipt_date__lte=date.today()) \
            .filter(receipt_time__lte='17:00')

    if meal == 'dinner':
        users = CustomUser.objects.filter(status='patient') \
            .filter(receipt_date__lte=date.today()) \
            .filter(receipt_time__lte='21:00')

    if meal == 'tomorrow':
        tomorrow = date.today() + timedelta(days=1)
        users = CustomUser.objects.filter(status='patient').\
            filter(Q(receipt_date__lte=date.today()) | Q(receipt_date__lte=tomorrow) & Q(receipt_time__lte='10:00'))



    # users = CustomUser.objects.filter(status='patient')\
    #     .filter(receipt_date__lte=date.today())\
    #     .filter(receipt_time__lte=check_change_time())
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
        user_today = UsersToday.objects.get(user_id=user.id)
        user_today.delete()
    else:
        try:
            user_today = UsersToday.objects.get(user_id=user.id)
            user_today.user_id = user.id
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
            UsersToday(user_id=user.id,
                        date_create=date.today(),
                        full_name=user.full_name,
                        receipt_date=user.receipt_date,
                        receipt_time=user.receipt_time,
                        department=user.department,
                        room_number=user.room_number,
                        type_of_diet=user.type_of_diet,
                        comment=user.comment,
                        status=user.status).save()
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


