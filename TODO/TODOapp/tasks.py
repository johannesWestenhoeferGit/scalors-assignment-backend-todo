from __future__ import absolute_import, unicode_literals
from django.core.mail import send_mail
from .serializers import ReminderSerializer
from celery import task

@task()
def send_reminder(toaddr, text): 
    # Gather data from serializer then send mail
    # using google smtp server
#    toaddr = data['email']
#    text = data['text']
    send_mail(
        'Reminder',
        text,
        'django.smtp.jw@gmail.com',
        [toaddr,],
        fail_silently = False,
    )