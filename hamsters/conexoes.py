# -*- coding: utf-8 -*-

from redis import Redis
import requests

from hamsters import settings
from hamsters.fazendo.imagens import cria_imagem_inicio_jogo, cria_imagem_gol, cria_imagem_fim_jogo
from hamsters.fazendo.models import Partida

MENSAGEM_INICIO = u"""
Comeeeeeça {times}!!!
Os palpites desse jogo estão encerrados. O resultado que os votadores esperam é:

{placar_palpites}
"""

MENSAGEM_GOL = u"""
{time} marcou um gol!!!

Placar atual: {placar_real}
Placar palpites: {placar_palpites}
"""

MENSAGEM_FIM = u"""
Termiiiina {times}!!!
Placar final: {placar_real}
Placar palpites: {placar_palpites}{palpite_certo}
"""

MENSAGEM_PALPITES_CERTOS = u"""
Até agora, os palpites registrados no Simulador da Copa do Mundo acertaram os seguintes resultados:
{}
Dê seu palpite também nos próximos jogos!
{}
"""

MENSAGEM_HAMSTERS_PREGUICOSOS = u"""
Os hamsters do Simulador da Copa do Mundo andam preguiços.
Já encomendamos 2 tonelada de semente de girassol!
Eem breve eles estarão informando corretamente sobre as partidas em andamento! :D
"""


class Repositorio(object):
    def __init__(self):
        self.repositorio = Redis(settings.REDIS['HOST'], settings.REDIS['PORT'])

    def __getitem__(self, item):
        return self.repositorio.get(item)

    def __setitem__(self, key, value):
        return self.repositorio.set(key, value)

    def existe(self, chave):
        return self.repositorio.exists(chave)

    def obtem_ou_cria(self, chave, valor):
        if self.existe(chave):
            return self[chave]
        self[chave] = valor
        return valor


class DebugRequest(object):
    def __init__(self):
        self.status_code = 200
        self.content = "Debug"


class Facebook(object):

    FEED_POST_URL = "{}/{}/feed?access_token={}".format(settings.FACEBOOK_GRAPH_API, settings.FACEBOOK_PAGE_ID, settings.FACEBOOK_PAGE_ACCESS_TOKEN)
    PHOTO_POST_URL = "{}/{}/photos?access_token={}".format(settings.FACEBOOK_GRAPH_API, settings.FACEBOOK_PAGE_ID, settings.FACEBOOK_PAGE_ACCESS_TOKEN)
    HAMSTERS_PREGUICOSOS = {
        "message": MENSAGEM_HAMSTERS_PREGUICOSOS,
        "link": "http://www.simuladorcopadomundo.com.br"
    }

    @classmethod
    def obtem_access_token(cls, temporary_access_token):
        url = "{}/oauth/access_token?grant_type=fb_exchange_token&client_id={}&client_secret={}&fb_exchange_token={}"
        app_id = settings.FACEBOOK_APP_ID
        app_scret = settings.FACEBOOK_APP_SECRET
        return requests.get(url.format(settings.FACEBOOK_GRAPH_API, app_id, app_scret, temporary_access_token))

    @classmethod
    def post(cls, data, image=False):
        if settings.DEBUG:
            print data
            return DebugRequest()
        if image:
            return requests.post(cls.PHOTO_POST_URL, data=data)
        return requests.post(cls.FEED_POST_URL, data=data)

    @classmethod
    def posta_mensagem(cls, mensagem="", path="", imagem=False):
        data = {
            "link": "{}{}".format(settings.HOST, path)
        }
        if mensagem:
            data['message'] = mensagem
        if imagem:
            data['url'] = imagem
            data['message'] = "Veja mais: {}".format(data['link'])
        return cls.post(data, image=imagem)

    @classmethod
    def pega_partida(cls, partida_id):
        try:
            return Partida.objects.get(id=partida_id)
        except Partida.DoesNotExist:
            return False

    @classmethod
    def partida_em_andamento(cls, partida_id):
        partida = cls.pega_partida(partida_id)
        if not partida:
            return False
        imagem = cria_imagem_inicio_jogo(partida)
        mensagem = ""
        if not imagem:
            mensagem = MENSAGEM_INICIO.format(**{
                "times": partida.formatado_para_placar(),
                "placar_palpites": partida.formatado_para_placar_com_gols()
            })

        return cls.posta_imagem_ou_mensagem(imagem, mensagem, "agenda")

    @classmethod
    def mudanca_de_placar(cls, partida_id, dados_placar):
        partida = cls.pega_partida(partida_id)
        if not partida:
            return False
        imagem = cria_imagem_gol(partida, dados_placar)
        mensagem = ""
        if not imagem:
            mensagem = MENSAGEM_GOL.format(**{
                "time": dados_placar['gol_de'],
                "placar_real": partida.formatado_para_placar_com_gols(palpites=False),
                "placar_palpites": partida.formatado_para_placar_com_gols()
            })

        return cls.posta_imagem_ou_mensagem(imagem, mensagem, "agenda")

    @classmethod
    def posta_imagem_ou_mensagem(cls, imagem, mensagem, path):
        try:
            if imagem:
                retorno = cls.posta_mensagem(imagem=imagem, path=path)
                return retorno, imagem
            retorno = cls.posta_mensagem(mensagem=mensagem, path=path)
            return retorno, mensagem
        except:
            return False

    @classmethod
    def partida_finalizada(cls, partida_id):
        partida = cls.pega_partida(partida_id)
        if not partida:
            return False

        imagem = cria_imagem_fim_jogo(partida)
        mensagem = ""
        if not imagem:
            mensagem = MENSAGEM_FIM.format(**{
                "times": partida.formatado_para_placar(),
                "placar_real": partida.formatado_para_placar_com_gols(palpites=False),
                "placar_palpites": partida.formatado_para_placar_com_gols(),
                "palpite_certo": "\n\nE os palpites acertaram esse placar! Confira!!!" if partida.palpite_certo() else ""
            })
        return cls.posta_imagem_ou_mensagem(imagem, mensagem, partida.time_1.grupo.path)

    @classmethod
    def palpites_certos(cls, partidas):
        partidas_certas = [partida.formatado_para_placar_com_gols() for partida in partidas]
        proximos_jogos = [partida.formatado_para_agenda() for partida in Partida.proximas()]
        mensagem = MENSAGEM_PALPITES_CERTOS.format("\n".join(partidas_certas), "\n".join(proximos_jogos))
        try:
            retorno = cls.posta_mensagem(mensagem)
            return retorno, mensagem
        except:
            return False


class CeleryClient(object):
    pass