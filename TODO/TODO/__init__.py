"""
 As soon as these 3 lines are included the makemigration returns an error:
 django.core.exceptions.AppRegistryNotReady: Apps aren't loaded yet.
"""



from __future__ import absolute_import
from .celery import app as celery_app

__all__ =  [ 'celery_app' ]
