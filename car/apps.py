import sys

from django.apps import AppConfig

from config.settings import SCHEDULER_AUTOSTART


class CarConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'car'

    def ready(self):
        if not ('makemigrations' in sys.argv or 'migrate' in sys.argv) and SCHEDULER_AUTOSTART:
            from car.tasks.test_task import start_aps
            start_aps()
