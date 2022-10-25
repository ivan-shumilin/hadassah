from celery import shared_task
import telepot
from nutritionist.models import BotChatId
from doctor.functions.for_print_forms import create_user_today, applies_changes, create_user_tomorrow


def send_messang(meal):
    check = '\u2705'
    TOKEN = '5533289712:AAEENvPBVrfXJH1xotRzoCCi24xFcoH9NY8'
    bot = telepot.Bot(TOKEN)
    # все номера chat_id
    messang = f'{check} Заказ на <u><b>{meal}</b></u> сформирован.'
    for item in BotChatId.objects.all():
        bot.sendMessage(item.chat_id, messang, parse_mode="html")

@shared_task()
def my_job_applies_changes_():
    applies_changes()

@shared_task()
def my_job_applies_changes_breakfast():
    # applies_changes() # накатываем изменения
    send_messang('завтрак')

@shared_task()
def my_job_applies_changes_lunch():
    applies_changes() # накатываем изменения
    send_messang('обед')

@shared_task()
def my_job_applies_changes_afternoon():
    applies_changes() # накатываем изменения
    send_messang('полдник')

@shared_task()
def my_job_applies_changes_dinner():
    applies_changes() # накатываем изменения
    send_messang('ужин')

@shared_task()
def my_job_create_user_today():
    create_user_today() # создаем таблицу с пользователями на сегодня

@shared_task()
def my_job_create_user_tomorrow():
    """ Создаем таблицу с пользователями на завтра """
    create_user_tomorrow()  # создаем таблицу с пользователями на завтра
    # applies_changes()
    send_messang('завтра')



@shared_task()
def send_messang_1():
    TOKEN = '5533289712:AAEENvPBVrfXJH1xotRzoCCi24xFcoH9NY8'
    attention = u'\u2757\ufe0f'
    bot = telepot.Bot(TOKEN)
    # все номера chat_id
    messang = f'test_1'
    for item in BotChatId.objects.all():
        bot.sendMessage(item.chat_id, messang, parse_mode="html")

