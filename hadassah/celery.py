import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hadassah.settings")
app = Celery("hadassah")

app.config_from_object("django.conf:settings", namespace="CELERY")


app.conf.beat_schedule = {
    'my_job_add_menu_three_days_ahead': {
        'task': 'doctor.tasks.my_job_add_menu_three_days_ahead',
        'schedule': crontab(minute=0, hour='0'),
    },
    'my_job_applies_changes_breakfast_one': {
        'task': 'doctor.tasks.my_job_applies_changes_breakfast',
        'schedule': crontab(minute=3, hour='0'),
    },
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
        'schedule': crontab(minute=0, hour='19'),
    },

    'my_job_create_ready_order_breakfast': {
        'task': 'doctor.tasks.my_job_create_ready_order_breakfast',
        'schedule': crontab(minute=0, hour='7'),
    },
    'my_job_create_ready_order_lunch': {
        'task': 'doctor.tasks.my_job_create_ready_order_lunch',
        'schedule': crontab(minute=0, hour='11'),
    },
    'my_job_create_ready_order_afternoon': {
        'task': 'doctor.tasks.my_job_create_ready_order_afternoon',
        'schedule': crontab(minute=0, hour='14'),
    },
    'my_job_create_ready_order_dinner': {
        'task': 'doctor.tasks.my_job_create_ready_order_dinner',
        'schedule': crontab(minute=0, hour='17'),
    },
}
app.conf.timezone = 'Europe/Moscow'
app.autodiscover_tasks()