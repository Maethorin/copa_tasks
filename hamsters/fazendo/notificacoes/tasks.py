from celery.task import task
from celery.utils.log import get_task_logger

__author__ = 'maethorin'


logger = get_task_logger(__name__)


@task(name='notificacoes.inicio_jogo')
def inicio_jogo():
    pass


@task(name='notificacoes.placar_igual')
def placar_igual():
    pass


@task(name='notificacoes.fim_jogo')
def fim_jogo():
    pass

