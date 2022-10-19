import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util

import telepot
from nutritionist.models import BotChatId
from doctor.functions.for_print_forms import create_user_today, applies_changes

logger = logging.getLogger(__name__)

def send_messang(meal):
    TOKEN = '5533289712:AAEENvPBVrfXJH1xotRzoCCi24xFcoH9NY8'
    bot = telepot.Bot(TOKEN)
    # все номера chat_id
    messang = f'Заказ на {meal} сформирован.'
    for item in BotChatId.objects.all():
        bot.sendMessage(item.chat_id, messang)

def my_job_applies_changes():
    applies_changes()

def my_job_applies_changes_breakfast():
    applies_changes() # накатываем изменения
    send_messang('завтрак')

def my_job_applies_changes_lunch():
    applies_changes() # накатываем изменения
    send_messang('обед')

def my_job_applies_changes_afternoon():
    applies_changes() # накатываем изменения
    send_messang('полдник')

def my_job_applies_changes_dinner():
    applies_changes() # накатываем изменения
    send_messang('ужин')

def my_job_create_user_today():
    create_user_today() # создаем таблицу с пользователями на сегодня



# The `close_old_connections` decorator ensures that database connections, that have become
# unusable or are obsolete, are closed before and after your job has run. You should use it
# to wrap any jobs that you schedule that access the Django database in any way.
@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """
    This job deletes APScheduler job execution entries older than `max_age` from the database.
    It helps to prevent the database from filling up with old historical records that are no
    longer useful.

    :param max_age: The maximum length of time to retain historical job execution records.
                    Defaults to 7 days.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job_create_user_today,
            trigger=CronTrigger(hour='00', minute='00'),
            id="my_job_create_user_today",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job_create_user_today'.")

        scheduler.add_job(
            my_job_applies_changes_breakfast,
            trigger=CronTrigger(hour='7', minute='00'),
            id="my_job_applies_changes_breakfast",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job_applies_changes_breakfast'.")

        scheduler.add_job(
            my_job_applies_changes_lunch,
            trigger=CronTrigger(hour='9', minute='00'),
            id="my_job_applies_changes_lunch",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job_applies_changes_lunch'.")

        scheduler.add_job(
            my_job_applies_changes_afternoon,
            trigger=CronTrigger(hour='12', minute='00'),
            id="my_job_applies_changes_afternoon",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job_applies_changes_afternoon'.")

        scheduler.add_job(
            my_job_applies_changes_dinner,
            trigger=CronTrigger(hour='16', minute='00'),
            id="my_job_applies_changes_dinner",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job_applies_changes_dinner'.")


        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Midnight on Monday, before start of the next work week.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")