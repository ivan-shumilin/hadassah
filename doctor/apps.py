from django.apps import AppConfig


class DoctorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'doctor'


class AppNameConfig(AppConfig):
    name = 'doctor'
    def ready(self):
        from scheduler import scheduler
        scheduler.start()
