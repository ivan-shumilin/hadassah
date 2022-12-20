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