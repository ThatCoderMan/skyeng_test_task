import os

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

app = Celery('backend', broker_connection_retry_on_startup=True)

app.config_from_object('django.conf:settings')

app.conf.beat_schedule = {
    'every-15-seconds': {
        'task': 'repeat_file_checker',
        'schedule': 15,
        'args': ()
    }
}
app.conf.timezone = 'UTC'
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
