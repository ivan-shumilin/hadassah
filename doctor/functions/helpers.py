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

def formatting_full_name_mode_full(full_name_row):
    full_name_row_list = full_name_row.split(' ')
    full_name_list = [item.strip().capitalize() for item in full_name_row_list]
    return ' '.join(full_name_list)