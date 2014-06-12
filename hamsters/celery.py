# -*- coding: utf-8 -*-
from __future__ import absolute_import
import site
import sys

__author__ = 'maethorin'
import os

from hamsters import settings
from celery import Celery

ROOT = os.path.dirname(os.path.abspath(__file__))
path = lambda *a: os.path.join(ROOT, *a)
prev_sys_path = list(sys.path)
site.addsitedir(path('../tasks'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hamsters.settings')
app = Celery('hamsters')
app.config_from_object(settings, force=True)
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))