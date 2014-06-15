from celery.task import task
from celery.utils.log import get_task_logger
from hamsters.conexoes import Repositorio, Facebook
from hamsters.fazendo.models import Partida

__author__ = 'maethorin'


logger = get_task_logger(__name__)


@task(name='notificacoes.inicio_jogo')
def inicio_jogo(partida_id):
    cache = Repositorio()
    if not cache["partida.{}.inicio_notificado".format(partida_id)]:
        sucesso = Facebook.partida_em_andamento(partida_id)
        logger.info(sucesso['message'].replace("\n", " "))
        cache["partida.{}.inicio_notificado".format(partida_id)] = True


@task(name='notificacoes.mudanca_de_placar')
def mudanca_de_placar(partida, informacoes):
    pass


@task(name='notificacoes.fim_jogo')
def fim_jogo():
    pass

