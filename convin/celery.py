from __future__ import absolute_import
import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'convin.settings')

from django.conf import settings

app = Celery(broker=settings.CELERY_BROKER_URL, backend =settings.CELERY_RESULT_BACKEND)
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(settings.INSTALLED_APPS)
app.autodiscover_tasks(lambda:settings.INSTALLED_APPS,force=False)

if __name__ == '__main__':
    app.start()