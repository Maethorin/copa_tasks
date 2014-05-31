# -*- coding: utf-8 -*-
from __future__ import absolute_import

__author__ = 'maethorin'

from hamsters import settings

from celery import Celery

app = Celery('hamsters')

app.config_from_object(settings)

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)