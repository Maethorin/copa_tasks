# -*- coding: utf-8 -*-

from redis import Redis
import requests

from hamsters import settings
from hamsters.fazendo.models import Partida


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


class Facebook(object):

    FEED_POST_URL = "{}/{}/feed?access_token={}".format(settings.FACEBOOK_GRAPH_API, settings.FACEBOOK_PAGE_ID, settings.FACEBOOK_PAGE_ACCESS_TOKEN)
    HAMSTERS_PREGUICOSOS = {
        "message": "Os hamsters do Simulador da Copa do Mundo andam preguiços. Já encomendamos 2 tonelada de semente de girassol e em breve eles estarão informando corretamente sobre as partidas em andamento! :D",
        "link": "http://www.simuladorcopadomundo.com.br"
    }

    @classmethod
    def post(cls, data):
        return requests.post(cls.FEED_POST_URL, data=data)

    @classmethod
    def partida_em_andamento(cls, partida_id):
        try:
            partida = Partida.objects.get(id=partida_id)
        except Partida.DoesNotExist:
            return False

        mensagem = u"""
Comeeeeeça {times}!!!
Os palpites desse jogo estão encerrados. O resultado que os votadores esperam é:

{time_1_abreviatura} {palpites_time_1} x {palpites_time_2} {time_2_abreviatura}
""".format(**{
            "times": partida.formatado_para_placar(),
            "time_2": partida.time_2.nome,
            "time_1_abreviatura": partida.time_1.abreviatura,
            "time_2_abreviatura": partida.time_2.abreviatura,
            "palpites_time_1": partida.media_palpites_time_1(),
            "palpites_time_2": partida.media_palpites_time_2()
        })
        data = {
            "message": mensagem,
            "link": "{}{}".format(settings.HOST, partida.time_1.grupo.path)
        }
        try:
            retorno = cls.post(data)
            return retorno, mensagem
        except:
            return False

    @classmethod
    def obtem_access_token(cls, temporary_access_token):
        url = "{}/oauth/access_token?grant_type=fb_exchange_token&client_id={}&client_secret={}&fb_exchange_token={}"
        app_id = settings.FACEBOOK_APP_ID
        app_scret = settings.FACEBOOK_APP_SECRET
        return requests.get(url.format(settings.FACEBOOK_GRAPH_API, app_id, app_scret, temporary_access_token))


class CeleryClient(object):
    pass