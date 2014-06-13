# -*- coding: utf-8 -*-

from celery.task import task
from celery.utils.log import get_task_logger
from hamsters.fazendo.classificacao import classificador, simulador, em_andamento
from hamsters.fazendo.models import Partida, Grupo

__author__ = 'maethorin'


logger = get_task_logger(__name__)


@task(name='classificacao.classificar_times')
def classificar_times(atual=False):
    grupos = Grupo.objects.all()
    for grupo in grupos:
        classificador.obtem_times_do_grupo_ordenados_por_classificacao(grupo.nome, atual)
    return True


@task(name='classificacao.definir_times_em_partidas')
def definir_times_em_partidas():
    for partida in Partida.objects.all().exclude(fase__slug='classificacao'):
        logger.info("Obtendo times de {} - {}".format(partida.fase.nome, partida.regra_para_times))
        if partida.fase.slug == 'oitavas':
            time1, time2 = simulador.obtem_times_de_partida_de_oitavas(partida.regra_para_times, partida.realizada)
        else:
            time1, time2 = simulador.obtem_times_de_partida_de_outras_fases(partida.regra_para_times)

        if not partida.realizada:
            if partida.time_eh_diferente(time1, time2):
                partida.palpites_time_1 = 0
                partida.palpites_time_2 = 0
                partida.votos = 0
            partida.time_1 = time1
            partida.time_2 = time2
            logger.info("Gravando {} - {}".format(partida.fase.nome, partida.regra_para_times))
            partida.save()
    return True


@task(name='classificacao.grava_partidas_em_andamento')
def grava_partidas_em_andamento():
    logger.info(u"Verificando se tem partidas em andamento")
    for partida in Partida.objects.filter(realizada=False):
        if partida.em_andamento():
            informacoes = em_andamento.obter_informacoes_da_partida_em_jogo(partida)
            if informacoes:
                partida.gols_time_1 = informacoes.gols_time_1
                partida.gols_time_2 = informacoes.gols_time_2
                partida.realizada = informacoes.realizada
                partida.save()
                logger.info(u"Placar de {} atualizado".format(partida.formatado_para_placar()))
    return True
