#!/usr/bin/env python
# encoding: utf-8

from lxml import html as lhtml

from hamsters import settings


class InformacoesDePartida():
    def __init__(self, gols_time_1=0, gols_time_2=0, status="Tá Indo"):
        self.gols_time_1 = gols_time_1 or '0'
        self.gols_time_2 = gols_time_2 or '0'
        self.realizada = status == 'Finished'


def obter_informacoes_da_partida_em_jogo(partida):
    try:
        url = settings.URL_BASE_DE_RESULTADOS
        if partida.fase.slug == "classificacao":
            url_grupo = settings.URL_RESULTADOS_DE_CLASSIFICACAO.format(settings.URL_DE_GRUPOS[partida.time_1.grupo.nome], obter_rodada(partida))
            url = "{}{}".format(url, url_grupo)
        pagina_resultado = lhtml.parse(url).getroot()
    except IOError:
        return None
    if pagina_resultado is None:
        return None

    return obtem_placar_do_html(pagina_resultado, partida)


def obter_rodada(partida):
    if 12 <= partida.data.day <= 16:
        return "1"
    elif partida.data.day == 17 and partida.time_1.grupo.nome == "H":
        return "1"
    elif partida.data.day == 17 and partida.time_1.grupo.nome == "A":
        return "2"
    elif 18 <= partida.data.day <= 22:
            return "2"
    return "3"


def obtem_placar_do_html(pagina_resultado, partida):
    equipes = pagina_resultado.cssselect(".nome-equipe")
    gols_time_1 = 0
    gols_time_2 = 0
    for equipe in equipes:
        if equipe.text == partida.time_1.abreviatura:
            gols_time_1 = equipe.getparent().getparent().cssselect(".placar-mandante")[0].text
        elif equipe.text == partida.time_2.abreviatura:
            gols_time_2 = equipe.getparent().getparent().cssselect(".placar-visitante")[0].text
    return InformacoesDePartida(gols_time_1, gols_time_2)
