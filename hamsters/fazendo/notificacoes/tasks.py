from celery.task import task
from celery.utils.log import get_task_logger

__author__ = 'maethorin'


logger = get_task_logger(__name__)


@task(name='notificacoes.avisa_inicio_jogo')
def avisa_inicio_jogo():
    pass