#!/usr/bin/env python
# encoding: utf-8
from celery.utils.log import get_task_logger

__author__ = 'maethorin'

from django.db.models import Q
from hamsters.fazendo.models import Time, Fase, Partida
from hamsters.fazendo.classificacao import simulador

logger = get_task_logger(__name__)


def obtem_times_do_grupo_ordenados_por_classificacao(nome_do_grupo, atual=False):
    times = Time.objects.filter(grupo__nome__exact=nome_do_grupo)
    tipo_classificacao = "R" if atual else "S"
    for time in times:
        time.zera_valores(tipo_classificacao)
    times_lista = []
    for time in times:
        fase = Fase.objects.get(slug='classificacao')
        filtros = Q(fase=fase) & (Q(time_1__id__exact=time.id) | Q(time_2__id__exact=time.id))
        if atual:
            filtros = filtros & Q(realizada=True)
        partidas = Partida.objects.filter(filtros)
        for partida in partidas:
            vitorioso, gols_time_1, gols_time_2 = simulador.obter_time_na_partida(partida)
            soma_gols_do_time(time, gols_time_1, gols_time_2, partida.time_1.id, tipo_classificacao)
            time.classificacao(tipo_classificacao).jogos += 1
            if vitorioso is None:
                time.classificacao(tipo_classificacao).pontos += 1
                time.classificacao(tipo_classificacao).empates += 1
            elif vitorioso.id == time.id:
                time.classificacao(tipo_classificacao).pontos += 3
                time.classificacao(tipo_classificacao).vitorias += 1
            time.classificacao(tipo_classificacao).saldo_de_gols = time.classificacao(tipo_classificacao).gols_feitos - time.classificacao(tipo_classificacao).gols_tomados
        times_lista.append(time)

    times_lista.sort(lambda x, y: cmp(y.classificacao(tipo_classificacao).pontos, x.classificacao(tipo_classificacao).pontos))
    normalizar_lista_com_saldo_de_gols(times_lista, tipo_classificacao)
    return times_lista


def soma_gols_do_time(time, gols_time_1, gols_time_2, time_1_id, tipo_classificacao):
    if time.id == time_1_id:
        time.classificacao(tipo_classificacao).gols_feitos += gols_time_1
        time.classificacao(tipo_classificacao).gols_tomados += gols_time_2
    else:
        time.classificacao(tipo_classificacao).gols_feitos += gols_time_2
        time.classificacao(tipo_classificacao).gols_tomados += gols_time_1


def normalizar_lista_com_saldo_de_gols(times, tipo_classificacao):
    for i in range(0, len(times)):
        times[i].classificacao(tipo_classificacao).posicao = i + 1
        times[i].classificacao(tipo_classificacao).save()
        times[i].save()
        logger.info(u"Gravado time {} no grupo {}".format(times[i].nome, times[i].grupo.nome))

    reordena = False
    lista_de_empates = []
    indices_com_pontos_iguais = []
    times_com_pontos_iguais = []
    indices_dos_empatados = []
    for i in range(0, len(times)):
        if (i + 1) < len(times) and times[i].classificacao(tipo_classificacao).pontos == times[i + 1].classificacao(tipo_classificacao).pontos:
            adiciona_item_a_lista(indices_com_pontos_iguais, i)
            adiciona_item_a_lista(indices_com_pontos_iguais, i + 1)
            adiciona_item_a_lista(times_com_pontos_iguais, times[i])
            adiciona_item_a_lista(times_com_pontos_iguais, times[i + 1])
            reordena = True
        else:
            if len(times_com_pontos_iguais) > 0:
                lista_de_empates.append(times_com_pontos_iguais)
                indices_dos_empatados.append(indices_com_pontos_iguais)
                times_com_pontos_iguais = []
                indices_com_pontos_iguais = []

    if reordena:
        ordenar_por_saldo_de_gols_removendo_empatados_da_original(lista_de_empates, times, tipo_classificacao)
        reposiciona_e_reordena_na_original(lista_de_empates, indices_dos_empatados, times, tipo_classificacao)


def adiciona_item_a_lista(lista, item):
    if not item in lista:
        lista.append(item)


def ordenar_por_saldo_de_gols_removendo_empatados_da_original(lista_de_empates, times, tipo_classificacao):
    for times_empatados in lista_de_empates:
        for time in times_empatados:
            times.remove(time)
        times_empatados.sort(lambda x, y: cmp(y.classificacao(tipo_classificacao).saldo_de_gols, x.classificacao(tipo_classificacao).saldo_de_gols))


def reposiciona_e_reordena_na_original(lista_de_empates, indices_dos_empatados, times, tipo_classificacao):
    for i in range(0, len(lista_de_empates)):
        for k in range(0, len(lista_de_empates[i])):
            lista_de_empates[i][k].classificacao(tipo_classificacao).posicao = indices_dos_empatados[i][k] + 1

        times.extend(lista_de_empates[i])
    times.sort(lambda x, y: cmp(x.classificacao(tipo_classificacao).posicao, y.classificacao(tipo_classificacao).posicao))
