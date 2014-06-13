from celery.task import task
from celery.utils.log import get_task_logger
from hamsters.conexoes import Repositorio, Facebook
from hamsters.fazendo.models import Partida

__author__ = 'maethorin'


logger = get_task_logger(__name__)


@task(name='notificacoes.inicio_jogo')
def inicio_jogo():
    cache = Repositorio()
    for partida in [partida for partida in Partida.objects.all() if partida.em_andamento()]:
        if not cache["partida.{}.avisada".format(partida.id)]:
            sucesso = Facebook.partida_em_andamento(partida)
            logger.info(sucesso['message'])
            cache["partida.{}.avisada".format(partida.id)] = True


@task(name='notificacoes.placar_igual')
def placar_igual():
    pass


@task(name='notificacoes.fim_jogo')
def fim_jogo():
    pass

