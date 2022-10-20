import datetime
from datetime import datetime, date, timedelta


def check_change(user):
    """Проверка с какого приема пищи изменения вступят в силу"""
    if datetime.today().time().hour > 0 and datetime.today().time().hour < 7:
        return 'зактрака'
    if datetime.today().time().hour >= 7 and datetime.today().time().hour < 11:
        return 'обеда'
    if datetime.today().time().hour >= 11 and datetime.today().time().hour < 14:
        return 'полдника'
    if datetime.today().time().hour >= 14 and datetime.today().time().hour < 17:
        return 'ужина'
    return None


def formatting_full_name(full_name):
    list = full_name.split()
    res = ''
    for index, value in enumerate(list):
        print(index, len(list))
        if index == 0:
            res += value.capitalize() + ' '
            continue
        if index == len(list) - 1:
            res += value[0:1].capitalize()
            continue
        else:
            res += value[0:1].capitalize() + '.'
    return res

def do_messang_send():
    if datetime.today().time().hour < 7 or datetime.today().time().hour >= 17:
        return False
    return True
