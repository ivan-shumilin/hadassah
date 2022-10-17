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
    return