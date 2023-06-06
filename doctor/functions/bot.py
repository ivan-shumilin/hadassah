import datetime
from datetime import datetime, date, timedelta


def check_change(flag):
    """Проверка с какого приема пищи изменения вступят в силу"""
    time = datetime.today().time()

    if (time.hour >= 0 and time.hour < 8) or (time.hour == 8 and time.minute <= 30):
        return ('завтрака', 0) if flag == 'True' else 'завтрака'
    if (time.hour == 8 and time.minute > 30) or (time.hour == 12 and time.minute == 0) or time.hour >= 9 and time.hour < 12:
        return ('обеда', 1) if flag == 'True' else 'обеда'
    if (time.hour == 12 and time.minute >= 1) or (time.hour == 15 and time.minute <= 30) or time.hour > 12 and time.hour < 15:
        return ('полдника', 2) if flag == 'True' else 'полдника'
    if (time.hour == 15 and time.minute > 30) or (time.hour == 18 and time.minute == 0) or time.hour > 15 and time.hour < 18:
        return ('ужина', 3) if flag == 'True' else 'ужина'
    if time.hour > 18 or (time.hour == 18 and time.minute >= 1):
        return ('завтра', 4) if flag == 'True' else 'завтра'
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
    return res.strip()

def do_messang_send(name):
    if datetime.today().time().hour < 7 or datetime.today().time().hour >= 17:
        return False
    return True
