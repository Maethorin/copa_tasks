# -*- coding: utf-8 -*-
from datetime import timedelta

__author__ = 'maethorin'

INSTALLED_APPS = (
    'hamsters.fazendo.classificacao',
)

CELERYBEAT_SCHEDULE = {
    'simples': {
        'task': 'classificacao.simples',
        'schedule': timedelta(seconds=3)
    },
}

BROKER_URL = 'redis://localhost:6379/0'
CELERY_TIMEZONE = 'America/Sao_Paulo'
CELERY_ACCEPT_CONTENT = ['pickle']
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_TASK_RESULT_EXPIRES = 1800
CELERY_DEFAULT_QUEUE = 'hamstersapp.    '

REDIS = {
    'HOST': 'localhost',
    'PORT': '6379'
}