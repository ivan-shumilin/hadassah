import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hadassah.settings")
app = Celery("hadassah")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'my_job_applies_changes_breakfast': {
        'task': 'doctor.tasks.my_job_applies_changes_breakfast',
        'schedule': crontab(minute=0, hour='7'),
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
    # 'my_job_create_menu': {
    #     'task': 'doctor.tasks.my_job_create_menu',
    #     'schedule': crontab(minute=0, hour='0'),
    # }
}


# app.conf.beat_schedule = {
#     'my_job_applies_changes_breakfast': {
#         'task': 'doctor.tasks.my_job_applies_changes_breakfast',
#         'schedule': crontab(minute=42, hour='16'),
#     },
#     'my_job_applies_changes_lunch': {
#         'task': 'doctor.tasks.my_job_applies_changes_lunch',
#         'schedule': crontab(minute=43, hour='16'),
#     },
#     'my_job_applies_changes_afternoon': {
#         'task': 'doctor.tasks.my_job_applies_changes_afternoon',
#         'schedule': crontab(minute=44, hour='16'),
#     },
#     'my_job_applies_changes_dinner': {
#         'task': 'doctor.tasks.my_job_applies_changes_dinner',
#         'schedule': crontab(minute=45, hour='16'),
#     },
#     'my_job_create_user_tomorrow': {
#         'task': 'doctor.tasks.my_job_create_user_tomorrow',
#         'schedule': crontab(minute=59, hour='16'),
#     },
# }
app.conf.timezone = 'Europe/Moscow'