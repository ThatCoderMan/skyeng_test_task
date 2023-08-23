import datetime

from celery import shared_task
from django_celery_beat.models import PeriodicTask

from core.pep8_checker import check_pep8_files
from reports.models import File
from celery.schedules import crontab
from celery import Celery


# app = Celery()


# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     print('start')
#     sender.add_periodic_task(10.0, repeat_file_checker.s(), name='add every 10')


@shared_task(name="repeat_file_checker")
def repeat_file_checker():
    print('start')
    unchecked_files = File.objects.filter(is_checked=False)
    file_paths = [file.file.path for file in unchecked_files]
    results = check_pep8_files(file_paths)
    unchecked_files[0].is_reported = True
    unchecked_files[0].save()
    print(results)

