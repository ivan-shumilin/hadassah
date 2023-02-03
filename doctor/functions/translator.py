"""
В этом файле функции, которые "переводят".
"""
from nutritionist.models import ProductLp, CustomUser, MenuByDay, Product, BotChatId,\
    UsersToday, MenuByDayReadyOrder, UsersReadyOrder
from django.db import transaction
from django.db.models import Q
from dateutil.parser import parse
from datetime import datetime, date, timedelta
from django.utils import dateformat

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

def translate_diet(diet):
    TYPE_DIET = {
        'ovd': 'ОВД',
        'ovd_sugarless': 'ОВД без сахара',
        'shd': 'ЩД',
        'shd_sugarless': 'ШД без сахара',
        'bd': 'БД',
        'vbd': 'ВБД',
        'nbd': 'НБД',
        'nkd': 'НКД',
        'vkd': 'ВКД',
        'ОВД': 'ovd',
        'ОВД без сахара': 'ovd_sugarless',
        'ЩД без сахара': 'ЩД без сахара',
        'ЩД': 'shd',
        'БД': 'БД',
        'ВБД': 'vbd',
        'НБД': 'nbd',
        'НКД': 'nkd',
        'ВКД': 'vkd',
        'ОВД веган (пост) без глютена': 'ОВД веган (пост) без глютена',
        'Нулевая диета': 'Нулевая диета',
        'БД день 1': 'bd',
        'БД день 2': 'bd',
    }
    return TYPE_DIET[diet]