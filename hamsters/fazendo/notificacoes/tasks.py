from celery.task import task
from celery.utils.log import get_task_logger
from hamsters import settings
from hamsters.conexoes import Repositorio, Facebook
from hamsters.fazendo.models import Partida

__author__ = 'maethorin'


logger = get_task_logger(__name__)


@task(name='notificacoes.inicio_jogo')
def inicio_jogo(partida_id):
    cache = Repositorio()
    if not cache["partida.{}.inicio_notificado".format(partida_id)]:
        retorno, mensagem = Facebook.partida_em_andamento(partida_id)
        if retorno.status_code == 200:
            cache["partida.{}.inicio_notificado".format(partida_id)] = True
            logger.info(mensagem.replace("\n", " "))
        else:
            logger.error(retorno.content)
    return "Finalizado"

@task(name='notificacoes.mudanca_de_placar')
def mudanca_de_placar(partida, informacoes):
    pass


@task(name='notificacoes.fim_jogo')
def fim_jogo():
    pass

