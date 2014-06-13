# -*- coding: utf-8 -*-

from redis import Redis
import requests

from hamsters import settings


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

    @classmethod
    def post(cls, data):
        requests.post("{}/{}/feed?access_token={}".format(settings.FACEBOOK_GRAPH_API, settings.FACEBOOK_PAGE_ID, settings.FACEBOOK_PAGE_ACCESS_TOKEN), data=data)

    @classmethod
    def partida_em_andamento(cls, partida):
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
            cls.post(data)
            return mensagem
        except:
            return False
