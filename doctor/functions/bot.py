import datetime
from datetime import datetime, date, timedelta


def check_change(flag):
    """Проверка с какого приема пищи изменения вступят в силу"""
    time = datetime.today().time()
    if time.hour > 0 and time.hour < 7:
        return ('зактрака', 0) if flag == 'True' else 'зактрака'
    if time.hour >= 7 and time.hour < 11:
        return ('обеда', 1) if flag == 'True' else 'обеда'
    if time.hour >= 11 and time.hour < 14:
        return ('полдника', 2) if flag == 'True' else 'полдника'
    if time.hour >= 14 and time.hour < 17:
        return ('ужина', 3) if flag == 'True' else 'ужина'
    if time.hour >= 17:
        return ('завтра', 4) if flag == 'True' else 'ужина'
    return ('завтра', 4) if flag == 'True' else 'завтра'


def formatting_full_name(full_name):
    list = full_name.split()
    res = ''
    for index, value in enumerate(list):
        if index == 0:
            res += value.capitalize() + ' '
            continue
        if index == 1:
            res += value[0:1].capitalize() + '.'
            continue
        else:
            res += value[0:1].capitalize() + '.'
    return res

def do_messang_send(name):
    if datetime.today().time().hour < 7 or datetime.today().time().hour >= 17 or name == 'Leslie William Nielsen':
        return False
    return True
