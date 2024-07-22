import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hadassah.settings")
app = Celery("hadassah")

app.config_from_object("django.conf:settings", namespace="CELERY")


app.conf.beat_schedule = {
    # создаем Menubyday на три дня вперед
    'my_job_add_menu_three_days_ahead': {
        'task': 'doctor.tasks.my_job_add_menu_three_days_ahead',
        'schedule': crontab(minute=0, hour='0'),
    },
    # дописать
    'my_job_applies_changes_breakfast_one': {
        'task': 'doctor.tasks.my_job_applies_changes_breakfast',
        'schedule': crontab(minute=3, hour='0'),
    },
    # дописать
    'my_job_applies_changes_breakfast_two': {
        'task': 'doctor.tasks.my_job_applies_changes_breakfast',
        'schedule': crontab(minute=0, hour='4'),
    },

    'my_job_applies_changes_lunch': {
        'task': 'doctor.tasks.my_job_applies_changes_lunch',
        'schedule': crontab(minute=0, hour='9'),
    },
    'my_job_applies_changes_afternoon': {
        'task': 'doctor.tasks.my_job_applies_changes_afternoon',
        'schedule': crontab(minute=0, hour='12'),
    },
    'my_job_applies_changes_dinner': {
        'task': 'doctor.tasks.my_job_applies_changes_dinner',
        'schedule': crontab(minute=0, hour='16'),
    },
    'my_job_create_user_tomorrow': {
        'task': 'doctor.tasks.my_job_create_user_tomorrow',
        'schedule': crontab(minute=1, hour='19'),
    },
    'my_job_create_ready_order_breakfast': {
        'task': 'doctor.tasks.my_job_create_ready_order_breakfast',
        'schedule': crontab(minute=31, hour='8'),
    },
    'my_job_create_ready_order_lunch': {
        'task': 'doctor.tasks.my_job_create_ready_order_lunch',
        'schedule': crontab(minute=1, hour='12'),
    },
    'my_job_create_ready_order_afternoon': {
        'task': 'doctor.tasks.my_job_create_ready_order_afternoon',
        'schedule': crontab(minute=31, hour='15'),
    },
    'my_job_create_ready_order_dinner': {
        'task': 'doctor.tasks.my_job_create_ready_order_dinner',
        'schedule': crontab(minute=1, hour='18'),
    },
    'my_job_create_product_storage_breakfast': {
        'task': 'doctor.tasks.my_job_create_product_storage_breakfast',
        'schedule': crontab(minute=31, hour='8'),
    },
    'my_job_create_product_storage_lunch': {
        'task': 'doctor.tasks.my_job_create_product_storage_lunch',
        'schedule': crontab(minute=1, hour='12'),
    },
    'my_job_create_product_storage_dinner': {
        'task': 'doctor.tasks.my_job_create_product_storage_dinner',
        'schedule': crontab(minute=1, hour='18'),
    },
# Создание записей для отчета
    'my_job_create_report_breakfast': {
        'task': 'doctor.tasks.my_job_create_report_breakfast',
        'schedule': crontab(minute=40, hour='8'),
    },
    'my_job_create_report_lunch': {
        'task': 'doctor.tasks.my_job_create_report_lunch',
        'schedule': crontab(minute=3, hour='12'),
    },
    'my_job_create_report_afternoon': {
        'task': 'doctor.tasks.my_job_create_report_afternoon',
        'schedule': crontab(minute=40, hour='15'),
    },
    'my_job_create_report_dinner': {
        'task': 'doctor.tasks.my_job_create_report_dinner',
        'schedule': crontab(minute=5, hour='18'),
    },
# Обновление ТТК
#     'my_job_updata_ttk': {
#         'task': 'doctor.tasks.my_job_updata_ttk',
#         'schedule': crontab(minute=1, hour='1'),
#     },
# кеширеум ингредиеты и ттк
    'may_job_updata_cache': {
        'task': 'doctor.tasks.may_job_updata_cache',
        'schedule': crontab(minute=30, hour='0'),
    },
# проверяем базу данных ПО учета времени
#     'may_job_ping_db': {
#         'task': 'doctor.tasks.may_job_ping_db',
#         'schedule': crontab(minute='*'),
#     },

    # каждодневный бэкап
    'my_job_regular_backup': {
        'task': 'doctor.tasks.regular_db_dump',
        'schedule': crontab(minute=0, hour='5'),
    },
}
app.conf.timezone = 'Europe/Moscow'
app.autodiscover_tasks()
