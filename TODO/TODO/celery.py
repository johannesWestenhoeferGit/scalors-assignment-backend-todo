from __future__ import absolute_import
from celery import Celery
from django.conf import settings
#from TODOapp.tasks import send_reminder
import os

"""
 Celery setup by doc

 import django and django.setup() are supposed to fix a bug I'm having,
 but I coudln't get it to work yet with those.
"""


# set the default Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TODO.settings')


app = Celery('TODO')

app.config_from_object('django.conf:settings', namespace = 'CELERY' )
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))