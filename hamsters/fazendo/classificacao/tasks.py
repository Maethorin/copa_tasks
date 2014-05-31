# -*- coding: utf-8 -*-

import random
from celery.task import task

__author__ = 'maethorin'


@task(name='classificacao.simples')
def simples():
    return random.randint(0, 10)