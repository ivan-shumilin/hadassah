import json

from celery import shared_task
import telepot, datetime

from nutritionist.functions.report import create_external_report, create_external_report_detailing, get_report
from nutritionist.models import BotChatId, CustomUser, MenuByDay, UsersReadyOrder, Report, IsReportCreate
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


def send_messang_changes(messang, only_chat_id=None):
    TOKEN = '5533289712:AAEENvPBVrfXJH1xotRzoCCi24xFcoH9NY8'
    # пробуем 20 раз отправить сообщение
    for attempt in range(1, 21):
        if only_chat_id:
            try:
                bot = telepot.Bot(TOKEN)
                bot.sendMessage(only_chat_id, messang, parse_mode="html")
                return attempt
            except:
                continue
        else:
            try:
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


# создание готовой заявки на прием пищи
@shared_task()
def my_job_create_ready_order_breakfast():
    create_ready_order('breakfast')


@shared_task()
def my_job_create_ready_order_lunch():
    create_ready_order('lunch')


@shared_task()
def my_job_create_ready_order_afternoon():
    create_ready_order('afternoon')

@shared_task()
def my_job_create_ready_order_dinner():
    create_ready_order('dinner')

# создание записей для отчета
@shared_task()
def my_job_create_report_breakfast():
    create_report('breakfast')


@shared_task()
def my_job_create_report_lunch():
    create_report('lunch')


@shared_task()
def my_job_create_report_afternoon():
    create_report('afternoon')

@shared_task()
def my_job_create_report_dinner():
    create_report('dinner')


# создаем таблицу с пользователями на сегодня
@shared_task()
def my_job_create_user_today():
    create_user_today()  # создаем таблицу с пользователями на сегодня

# создаем таблицу с пользователями на завтра
@shared_task()
def my_job_create_user_tomorrow():
    """Создаем таблицу с пользователями на завтра."""
    delete_menu_by_arhived_users()
    create_user_today('tomorrow')


@shared_task()
def my_job_send_messang_changes(messang, only_chat_id=None):
    return f'попытка - {send_messang_changes(messang, only_chat_id)}'

@shared_task()
def my_job_create_product_storage_breakfast():
    create_product_storage('breakfast')

@shared_task()
def my_job_create_product_storage_lunch():
    create_product_storage('lunch')

@shared_task()
def my_job_create_product_storage_dinner():
    create_product_storage('dinner')

@shared_task()
def my_job_update_diet_bd():
    update_diet_bd()

@shared_task()
def create_report_download(date_start, date_finish, id):

    filtered_report = Report.objects.filter(date_create__gte=date_start,
        date_create__lte=date_finish,
    ).exclude(
        user_id__type_pay='petrushka'
    )
    date_start = datetime.strptime(date_start, "%Y-%m-%d").date()
    date_finish = datetime.strptime(date_finish, "%Y-%m-%d").date()
    report = create_external_report(filtered_report)
    report_detailing = create_external_report_detailing(filtered_report)
    get_report(report, report_detailing, date_start, date_finish)

    item = IsReportCreate.objects.get(id=id)
    item.is_report_create = True
    item.save()

    return