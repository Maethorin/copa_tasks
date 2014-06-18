#!/usr/bin/env python
# encoding: utf-8
import logging
import urllib
import cStringIO
from os import path

from PIL import Image
from slugify import slugify

from hamsters.fazendo.models import Time, Partida
from hamsters.fazendo.imagens import cria_imagem_inicio_jogo

__author__ = 'maethorin'

logger = logging

def carregar():
    for time in Time.objects.all():
        try:
            nome = slugify(time.nome.lower())
            nome_bandeira = nome
            if nome.startswith('bosnia'):
                nome_bandeira = 'bosnia'
            if nome.startswith('estados'):
                nome_bandeira = 'eua'
            file_name = "/home/maethorin/projects/copa_tasks/hamsters/img_base/bandeiras/{}.png".format(nome)
            if path.exists(file_name):
                continue
            bandeira_url = "http://s.glbimg.com/es/sde/f/organizacoes/2014/05/30/{}_60x60.png".format(nome_bandeira)
            print "GET: {}".format(bandeira_url)
            bandeira_file = cStringIO.StringIO(urllib.urlopen(bandeira_url).read())
            bandeira = Image.open(bandeira_file)
            print "SAVING: {}".format(file_name)
            bandeira.save(file_name, "PNG")
        except:
            continue


def comeeeeca():
    for partida in Partida.objects.filter(realizada=False)[:1]:
        if partida.time_1 and partida.time_2:
            print "IMAGEM: {}".format(partida)
            cria_imagem_inicio_jogo(partida)

