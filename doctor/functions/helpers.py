"""
В этом файле маленькие функции, которые используют другие функции.
"""
from nutritionist.models import ProductLp, CustomUser, MenuByDay, Product, BotChatId,\
    UsersToday, MenuByDayReadyOrder, UsersReadyOrder
from django.db import transaction
from django.db.models import Q
from dateutil.parser import parse
from datetime import datetime, date, timedelta
from django.utils import dateformat


def check_value(category, products):
    value: str = ''
    if category != 'товар' and category != 'напиток':
        try:
            value = products.get(category=category).id
        except Exception:
            value = None
    else:
        value = ','.join([str(item.id) for item in products.filter(category=category)])
    return value

def get_day_of_the_week(date_get):
    """Дату в формате Y-M-D в день недели прописью"""

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