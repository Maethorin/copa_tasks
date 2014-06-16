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
    return "Jogo Iniciado"


@task(name='notificacoes.mudanca_de_placar')
def mudanca_de_placar(partida_id, dados_placar):
    retorno, mensagem = Facebook.mudanca_de_placar(partida_id, dados_placar)
    if retorno.status_code == 200:
        logger.info(mensagem.replace("\n", " "))
    else:
        logger.error(retorno.content)
    return "Finalizado"


@task(name='notificacoes.fim_jogo')
def fim_de_jogo(partida_id):
    cache = Repositorio()
    if not cache["partida.{}.fim_notificado".format(partida_id)]:
        retorno, mensagem = Facebook.partida_finalizada(partida_id)
        if retorno.status_code == 200:
            cache["partida.{}.fim_notificado".format(partida_id)] = True
            logger.info(mensagem.replace("\n", " "))
        else:
            logger.error(retorno.content)
    return "Jogo Finalizado"


@task(name='notificacoes.palpites_certos')
def palpites_certos():
    partidas = [partida for partida in Partida.objects.filter(realizada=True) if partida.palpite_certo()]
    if partidas:
        retorno, mensagem = Facebook.palpites_certos(partidas)
        if retorno.status_code == 200:
            logger.info(mensagem.replace("\n", " "))
        else:
            logger.error(retorno.content)
    return "Palpites certos notificados"
