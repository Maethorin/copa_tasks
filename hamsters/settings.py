# -*- coding: utf-8 -*-
from __future__ import absolute_import

from datetime import timedelta
import os
from celery.schedules import crontab

__author__ = 'maethorin'

HOST = "http://www.simuladorcopadomundo.com.br/"
SECRET_KEY = 't7i#g(6t%sp7&-4a$(hfderfa-b6(!i^z2^a)!a1#+8cpif6r)'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'tabela_copa',
        'USER': 'copa',
        'PASSWORD': 'AcopaéN0ssa!',
        'HOST': 'localhost',
        'PORT': '3306'
    }
}

SERVER_TIME_DIFF = 0

INSTALLED_APPS = (
    'hamsters.fazendo.classificacao',
)

CELERYBEAT_SCHEDULE = {
    'classificar-simulada': {
        'task': 'classificacao.classificar_times',
        'schedule': timedelta(seconds=40)
    },
    'classificar-real': {
        'task': 'classificacao.classificar_times',
        'schedule': timedelta(minutes=5),
        'args': (True, )
    },
    'definir-times-em-partidas': {
        'task': 'classificacao.definir_times_em_partidas',
        'schedule': timedelta(seconds=45)
    },
    'grava-partidas-em-andamento': {
        'task': 'classificacao.grava_partidas_em_andamento',
        'schedule': timedelta(seconds=45)
    },
    'palpites-certos': {
        'task': 'notificacoes.palpites_certos',
        'schedule': crontab(minute=0, hour='10,16')
    }
}

CELERY_TIMEZONE = 'America/Sao_Paulo'
TIME_ZONE = 'America/Sao_Paulo'

BROKER_URL = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['pickle']
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_TASK_RESULT_EXPIRES = 1800
CELERY_DEFAULT_QUEUE = 'hamstersapp.    '

REDIS = {
    'HOST': 'localhost',
    'PORT': '6379'
}

URL_BASE_DE_RESULTADOS = "http://globoesporte.globo.com/servico/esportes_campeonato/widget-uuid/c36d99dd-918a-459f-bf0c-648dec5773af/fases"
URL_TEMPO_REAL = "http://globoesporte.globo.com/futebol/copa-do-mundo/temporeal/{}/{}/"
URL_RESULTADOS_DE_CLASSIFICACAO = "/fase-grupos-copa-do-mundo-2014/grupo/{}/rodada/{}/jogos.html"
URL_RESULTADOS_DE_MATA_MATA = "/oitavas-copa-do-mundo-2014/classsificacao.html"
URL_DE_GRUPOS = {
    "A": "1069",
    "B": "1070",
    "C": "1071",
    "D": "1072",
    "E": "1073",
    "F": "1074",
    "G": "1075",
    "H": "1166",
}

URL_TEMPO_REAL_CENTRAL = "http://globoesporte.globo.com/temporeal/futebol/central.json"

FACEBOOK_GRAPH_API = "https://graph.facebook.com/v2.0"
FACEBOOK_APP_ID = os.environ.get('FACEBOOK_APP_ID', None)
FACEBOOK_APP_SECRET = os.environ.get('FACEBOOK_APP_SECRET', None)
FACEBOOK_USER_ID = os.environ.get('FACEBOOK_USER_ID', None)
FACEBOOK_PAGE_ID = os.environ.get('FACEBOOK_PAGE_ID', None)
FACEBOOK_PAGE_ACCESS_TOKEN = os.environ.get('FACEBOOK_PAGE_ACCESS_TOKEN', None)

DEBUG = False