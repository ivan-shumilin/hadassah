from celery import shared_task
import telepot
from nutritionist.models import BotChatId, CustomUser, MenuByDay, UsersReadyOrder
from doctor.functions.diet_formation import add_menu_three_days_ahead, update_diet_bd
from doctor.functions.for_print_forms import create_user_today, applies_changes, create_user_tomorrow,\
    create_ready_order, create_report, create_product_storage
from doctor.functions.bot import check_change, formatting_full_name


def send_messang(messang):
    TOKEN = '5533289712:AAEENvPBVrfXJH1xotRzoCCi24xFcoH9NY8'
    bot = telepot.Bot(TOKEN)
    # все номера chat_id
    for item in BotChatId.objects.all():
        bot.sendMessage(item.chat_id, messang, parse_mode="html")


def send_messang_changes(messang):
    # пробуем 20 раз отправить сообщение
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
def my_job_add_menu_three_days_ahead():
    add_menu_three_days_ahead()

@shared_task()
def my_job_applies_changes_():
    applies_changes()

@shared_task()
def my_job_applies_changes_breakfast():
    delete_menu_by_arhived_users()
    create_user_today('breakfast')


@shared_task()
def my_job_applies_changes_lunch():
    delete_menu_by_arhived_users()
    create_user_today('lunch')


@shared_task()
def my_job_applies_changes_afternoon():
    delete_menu_by_arhived_users()
    create_user_today('afternoon')


@shared_task()
def my_job_applies_changes_dinner():
    delete_menu_by_arhived_users()
    create_user_today('dinner')


@shared_task()
def my_job_create_ready_order_breakfast():
    create_ready_order('breakfast')
    create_report('breakfast')


@shared_task()
def my_job_create_ready_order_lunch():
    create_ready_order('lunch')
    create_report('lunch')


@shared_task()
def my_job_create_ready_order_afternoon():
    create_ready_order('afternoon')
    create_report('afternoon')

@shared_task()
def my_job_create_ready_order_dinner():
    create_ready_order('dinner')
    create_report('dinner')

@shared_task()
def my_job_create_user_today():
    create_user_today()  # создаем таблицу с пользователями на сегодня

@shared_task()
def my_job_create_user_tomorrow():
    """Создаем таблицу с пользователями на завтра."""
    delele_menu_by_arhived_users()
    create_user_today('tomorrow')
    send_messang("Готово")


@shared_task()
def my_job_send_messang_changes(messang):
    return f'попытка - {send_messang_changes(messang)}'

@shared_task()
def my_job_create_product_storage_lunch():
    create_product_storage('lunch')

@shared_task()
def my_job_create_product_storage_dinner():
    create_product_storage('dinner')

@shared_task()
def my_job_update_diet_bd():
    update_diet_bd()
