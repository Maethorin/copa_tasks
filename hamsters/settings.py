# -*- coding: utf-8 -*-
from datetime import timedelta

__author__ = 'maethorin'

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
        'schedule': timedelta(seconds=20)
    },
}

CELERY_TIMEZONE = 'America/Sao_Paulo'
USE_TZ = True

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
