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
    create_user_today('breakfast')
    send_messang('завтрак')

@shared_task()
def my_job_applies_changes_lunch():
    create_user_today('lunch')
    send_messang('обед')

@shared_task()
def my_job_applies_changes_afternoon():
    create_user_today('afternoon')
    send_messang('полдник')

@shared_task()
def my_job_applies_changes_dinner():
    create_user_today('dinner')
    send_messang('ужин')

@shared_task()
def my_job_create_user_today():
    create_user_today()  # создаем таблицу с пользователями на сегодня

@shared_task()
def my_job_create_user_tomorrow():
    """ Создаем таблицу с пользователями на завтра """
    create_user_today('tomorrow')
    # create_user_tomorrow()  # создаем таблицу с пользователями на завтра
    send_messang('завтра')

