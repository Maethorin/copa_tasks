#!/usr/bin/env python
# encoding: utf-8

from django.core.exceptions import ObjectDoesNotExist
from hamsters.fazendo.classificacao import parser_regra
from hamsters.fazendo.models import Time, Partida


def obtem_times_de_partida_de_oitavas(regra, realizada):
    grupos = parser_regra.obtem_grupos_de_regra(regra)
    classificacoes = parser_regra.obtem_classificacoes_de_regra(regra)
    time1 = obtem_time_do_grupo_na_classificacao(grupos[0], classificacoes[0], realizada)
    time2 = obtem_time_do_grupo_na_classificacao(grupos[1], classificacoes[1], realizada)
    return time1, time2


def obtem_time_do_grupo_na_classificacao(nome_do_grupo, posicao, realizada):
    try:
        if realizada:
            return Time.objects.get(grupo__nome=nome_do_grupo, classificacao_real__posicao=int(posicao))
        else:
            return Time.objects.get(grupo__nome=nome_do_grupo, classificacao_simulada__posicao=int(posicao))
    except Time.DoesNotExist:
        return None


def obtem_times_de_partida_de_outras_fases(regra):
    ids = parser_regra.obtem_ids_de_partida_de_regra(regra)
    partida1 = Partida.objects.get(id=ids[0])
    partida2 = Partida.objects.get(id=ids[1])
    perdedor = parser_regra.eh_disputa_de_terceiro_lugar(regra)
    if partida1.fase.nome == 'Oitavas':
        partida1.time_1, partida1.time_2 = obtem_times_de_partida_de_oitavas(partida1.regra_para_times, partida1.realizada)
        partida2.time_1, partida2.time_2 = obtem_times_de_partida_de_oitavas(partida2.regra_para_times, partida2.realizada)
    else:
        partida1.time_1, partida1.time_2 = obtem_times_de_partida_de_outras_fases(partida1.regra_para_times)
        partida2.time_1, partida2.time_2 = obtem_times_de_partida_de_outras_fases(partida2.regra_para_times)
    time1, gols_time_1, gols_time_2 = obter_time_na_partida(partida1, perdedor)
    time2, gols_time_1, gols_time_2 = obter_time_na_partida(partida2, perdedor)

    return time1, time2


def obter_time_na_partida(partida, perdedor=False):
    if partida.realizada:
        return analiza_resultado_e_acumula_gols(partida.gols_time_1, partida.gols_time_2, 1, partida, perdedor)
    return analiza_resultado_e_acumula_gols(partida.palpites_time_1, partida.palpites_time_2, partida.votos, partida, perdedor)


def analiza_resultado_e_acumula_gols(valor_1, valor_2, votos, partida, perdedor):
    if not valor_1:
        valor_1 = 0
    if not valor_2:
        valor_2 = 0
    gols_time_1 = valor_1
    gols_time_2 = valor_2
    if votos > 0:
        gols_time_1 = valor_1 / votos
        gols_time_2 = valor_2 / votos

    if gols_time_1 == gols_time_2:
        return None, gols_time_1, gols_time_2
    if gols_time_1 > gols_time_2:
        if perdedor:
            return partida.time_2, gols_time_1, gols_time_2
        return partida.time_1, gols_time_1, gols_time_2

    if perdedor:
        return partida.time_1, gols_time_1, gols_time_2
    return partida.time_2, gols_time_1, gols_time_2
