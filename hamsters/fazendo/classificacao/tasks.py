# -*- coding: utf-8 -*-

from celery.task import task
from hamsters.fazendo.classificacao import classificador, simulador, em_andamento
from hamsters.fazendo.models import Partida

__author__ = 'maethorin'


@task(name='classificacao.classificar_times')
def classificar_times(grupos, atual=False):
    for grupo in grupos:
        for time in classificador.obtem_times_do_grupo_ordenados_por_classificacao(grupo.nome, atual):
            time.save()
    return True


@task(name='classificacao.definir_times_em_partidas')
def definir_times_em_partidas():
    for partida in Partida.objects.all():
        if partida.fase.nome == 'Oitavas':
            time1, time2 = simulador.obtem_times_de_partida_de_oitavas(partida.regra_para_times)
        else:
            time1, time2 = simulador.obtem_times_de_partida_de_outras_fases(partida.regra_para_times)

        if not partida.realizada:
            if partida.time_eh_diferente(time1, time2):
                partida.palpites_time_1 = 0
                partida.palpites_time_2 = 0
                partida.votos = 0

            partida.time_1 = time1
            partida.time_2 = time2
            partida.save()
    return True


@task(name='classificacao.grava_partidas_em_andamento')
def grava_partidas_em_andamento():
    for partida in Partida.objects.all():
        if partida.em_andamento():
            informacoes = em_andamento.obter_informacoes_da_partida_em_jogo(partida)
            if informacoes:
                partida.gols_time_1 = informacoes.gols_time_1
                partida.gols_time_2 = informacoes.gols_time_2
                partida.realizada = informacoes.realizada
            partida.save()
    return True
