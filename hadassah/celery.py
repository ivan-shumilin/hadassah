import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hadassah.settings")
app = Celery("hadassah")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'my_job_applies_changes_2': {
        'task': 'doctor.tasks.my_job_applies_changes_breakfast',
        'schedule': crontab(minute=23, hour='13'),
    },
    'my_job_applies_changes_3': {
        'task': 'doctor.tasks.my_job_applies_changes_breakfast',
        'schedule': crontab(minute=24, hour='13'),
    },
    'my_job_applies_changes_4': {
        'task': 'doctor.tasks.my_job_applies_changes_breakfast',
        'schedule': crontab(minute=25, hour='13'),
    },
    'my_job_applies_changes_5': {
        'task': 'doctor.tasks.my_job_applies_changes_breakfast',
        'schedule': crontab(minute=26, hour='13'),
    },
    'my_job_applies_changes_6': {
        'task': 'doctor.tasks.my_job_applies_changes_breakfast',
        'schedule': crontab(minute=27, hour='13'),
    },
}
app.conf.timezone = 'Europe/Moscow'