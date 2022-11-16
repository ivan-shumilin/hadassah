from celery import shared_task
import telepot
from nutritionist.models import BotChatId, CustomUser, MenuByDay, UsersReadyOrder
from doctor.functions.for_print_forms import create_user_today, applies_changes, create_user_tomorrow,\
    create_ready_order, create_report
from doctor.functions.bot import check_change, formatting_full_name


def send_messang(messang):
    TOKEN = '5533289712:AAEENvPBVrfXJH1xotRzoCCi24xFcoH9NY8'
    bot = telepot.Bot(TOKEN)
    # все номера chat_id
    for item in BotChatId.objects.all():
        bot.sendMessage(item.chat_id, messang, parse_mode="html")


def send_messang_changes(messang):
    for attempt in range(1, 21):
        try:
            TOKEN = '5533289712:AAEENvPBVrfXJH1xotRzoCCi24xFcoH9NY8'
            bot = telepot.Bot(TOKEN)
            for item in BotChatId.objects.all():
                bot.sendMessage(item.chat_id, messang, parse_mode="html")
            return attempt
        except:
            continue

def delete_menu_by_arhived_users():
    users = CustomUser.objects.filter(status='patient_archive')
    for user in users:
        MenuByDay.objects.filter(user_id=user.id).delete()


@shared_task()
def my_job_applies_changes_():
    applies_changes()

@shared_task()
def my_job_applies_changes_breakfast():
    check = '\u2705'
    # messang = f'{check} Заказ на <u><b>завтрак</b></u> сформирован.'
    # send_messang(messang)
    delete_menu_by_arhived_users()
    create_user_today('breakfast')


@shared_task()
def my_job_applies_changes_lunch():
    check = '\u2705'
    # messang = f'{check} Заказ на <u><b>обед</b></u> сформирован.'
    # send_messang(messang)
    delete_menu_by_arhived_users()
    create_user_today('lunch')


@shared_task()
def my_job_applies_changes_afternoon():
    check = '\u2705'
    # messang = f'{check} Заказ на <u><b>полдник</b></u> сформирован.'
    # send_messang(messang)
    delete_menu_by_arhived_users()
    create_user_today('afternoon')


@shared_task()
def my_job_applies_changes_dinner():
    # check = '\u2705'
    # messang = f'{check} Заказ на <u><b>ужин</b></u> сформирован.'
    # send_messang(messang)
    delete_menu_by_arhived_users()
    create_user_today('dinner')


@shared_task()
def my_job_create_ready_order_breakfast():
    # check = '\u2705'
    # messang = f'{check} Изменения на <u><b>завтрак</b></u> не принимаются.'
    # send_messang(messang)
    create_ready_order('breakfast')
    create_report('breakfast')


@shared_task()
def my_job_create_ready_order_lunch():
    # check = '\u2705'
    # messang = f'{check} Изменения на <u><b>обед</b></u> не принимаются.'
    # send_messang(messang)
    create_ready_order('lunch')
    create_report('lunch')


@shared_task()
def my_job_create_ready_order_afternoon():
    # check = '\u2705'
    # messang = f'{check} Изменения на <u><b>полдник</b></u> не принимаются.'
    # send_messang(messang)
    create_ready_order('afternoon')
    create_report('afternoon')

@shared_task()
def my_job_applies_changes_dinner():
    # check = '\u2705'
    # messang = f'{check} Изменения на <u><b>ужин</b></u> не принимаются.'
    # send_messang(messang)
    create_ready_order('dinner')
    create_report('dinner')

@shared_task()
def my_job_create_user_today():
    create_user_today()  # создаем таблицу с пользователями на сегодня

@shared_task()
def my_job_create_user_tomorrow():
    """ Создаем таблицу с пользователями на завтра """
    delele_menu_by_arhived_users()
    create_user_today('tomorrow')
    # send_messang('завтра')

@shared_task()
def my_job_send_messang_changes(messang):
    return f'попытка - {send_messang_changes(messang)}'