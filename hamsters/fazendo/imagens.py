#!/usr/bin/env python
# encoding: utf-8
import logging
from hamsters import settings

__author__ = 'maethorin'

from PIL import Image, ImageFont, ImageDraw
from slugify import slugify

logger = logging

class ImagemBase(object):
    def __init__(self, partida):
        self.partida = partida
        self.caminho_base = settings.CAMINHO_IMAGENS
        self._bandeira_1 = None
        self._bandeira_2 = None
        self._base = None
        self.arquivo_font = "{}Graduate-Regular.ttf".format(self.caminho_base)
        self.font_placar = ImageFont.truetype(self.arquivo_font, 43)
        self.nome_imagem_base = None
        self.pasta = None

    @property
    def base(self):
        if not self.nome_imagem_base:
            raise NotImplemented("Você só pode chamar esse método em uma especialização que definiu self.nome_imagem_base")
        if not self._base:
            self._base = Image.open("{}{}".format(self.caminho_base, self.nome_imagem_base))
        return self._base

    @property
    def nome_da_imagem(self):
        raise NotImplemented("Você só pode chamar esse método em uma especialização")

    @property
    def draw(self):
        return ImageDraw.Draw(self.base)

    @property
    def slug_nome_time_1(self):
        return slugify(self.partida.time_1.nome)

    @property
    def slug_nome_time_2(self):
        return slugify(self.partida.time_2.nome)

    @property
    def bandeira_time_1(self):
        if not self._bandeira_1:
            self._bandeira_1 = Image.open("{}bandeiras/{}.png".format(self.caminho_base, self.slug_nome_time_1))
        return self._bandeira_1

    @property
    def bandeira_time_2(self):
        if not self._bandeira_2:
            self._bandeira_2 = Image.open("{}bandeiras/{}.png".format(self.caminho_base, self.slug_nome_time_2))
        return self._bandeira_2

    def posiciona_bandeiras_em(self, posicao_bandeira_1, posicao_bandeira_2):
        self.base.paste(self.bandeira_time_1, posicao_bandeira_1, self.bandeira_time_1)
        self.base.paste(self.bandeira_time_2, posicao_bandeira_2, self.bandeira_time_2)

    def posiciona_placar_em(self, posicao_gols_1, posicao_gols_2, gols_1, gols_2):
        self.draw.text(posicao_gols_1, str(gols_1), font=self.font_placar, fill=(219, 216, 0))
        self.draw.text(posicao_gols_2, str(gols_2), font=self.font_placar, fill=(219, 216, 0))

    def monta_placar_rodape(self):
        self.posiciona_bandeiras_em((60, 275), (283, 275))
        self.posiciona_placar_em((138, 280), (233, 280), self.partida.media_palpites_time_1(), self.partida.media_palpites_time_2())

    def salva_e_retorna_url(self):
        if not self.pasta or not self.nome_da_imagem:
            raise NotImplemented("Você só pode chamar esse método em uma especialização que definiu self.pasta e self.nome_da_imagem")
        self.base.save("{}img/{}/{}".format(settings.STATIC_ROOT, self.pasta, self.nome_da_imagem))
        return "{}img/{}/{}".format(settings.STATIC_URL, self.pasta, self.nome_da_imagem)


class ImagemInicio(ImagemBase):
    def __init__(self, partida):
        super(ImagemInicio, self).__init__(partida=partida)
        self.nome_imagem_base = "base-inicio-jogo.png"
        self.pasta = 'inicio'

    @property
    def nome_da_imagem(self):
        return "inicio-{}x{}.png".format(self.slug_nome_time_1, self.slug_nome_time_2)

    def insere_nomes_de_times(self):
        font_nome = ImageFont.truetype(self.arquivo_font, 23)
        largura_nome_2, altura_nome_2 = self.draw.textsize(self.partida.time_2.nome, font=font_nome)
        left_2 = 400 - largura_nome_2 - 15
        self.draw.text((15, 110), self.partida.time_1.nome, font=font_nome, fill=(10, 75, 10))
        self.draw.text((left_2, 195), self.partida.time_2.nome, font=font_nome, fill=(10, 75, 10))


class ImagemFim(ImagemInicio):
    def __init__(self, partida):
        super(ImagemInicio, self).__init__(partida=partida)
        self.nome_imagem_base = "base-fim-jogo.png"
        self.pasta = 'fim'

    @property
    def nome_da_imagem(self):
        return "fim-{}x{}.png".format(self.slug_nome_time_1, self.slug_nome_time_2)

    def monta_placar_rodape(self):
        self.posiciona_bandeiras_em((60, 375), (283, 375))
        self.posiciona_placar_em((138, 377), (233, 377), self.partida.media_palpites_time_1(), self.partida.media_palpites_time_2())

    def monta_placar_final(self):
        self.posiciona_bandeiras_em((60, 275), (283, 277))
        self.posiciona_placar_em((138, 277), (233, 277), self.partida.gols_time_1, self.partida.gols_time_2)


class ImagemGol(ImagemBase):
    def __init__(self, partida, dados_de_placar):
        super(ImagemGol, self).__init__(partida=partida)
        self.dados_de_placar = dados_de_placar
        self.nome_imagem_base = "base-gooool.png"
        self.pasta = 'placar'

    @property
    def nome_da_imagem(self):
        return "placar-{}-{}x{}-{}.png".format(self.slug_nome_time_1, self.dados_de_placar['gols_time_1'], self.dados_de_placar['gols_time_2'], self.slug_nome_time_2)

    def monta_placar_atual(self):
        self.posiciona_bandeiras_em((60, 167), (283, 167))
        self.posiciona_placar_em((138, 172), (233, 172), self.dados_de_placar['gols_time_1'], self.dados_de_placar['gols_time_2'])

    def insere_nome_de_time_que_fez_gol(self):
        font_nome = ImageFont.truetype(self.arquivo_font, 29)
        self.draw.text((10, 111), u"{}!!!".format(self.dados_de_placar['gol_de']), font=font_nome, fill=(10, 75, 10))


def cria_imagem_inicio_jogo(partida):
    try:
        imagem = ImagemInicio(partida)
        imagem.insere_nomes_de_times()
        imagem.monta_placar_rodape()
        return imagem.salva_e_retorna_url()
    except Exception, ex:
        logger.error(ex)
        return None


def cria_imagem_fim_jogo(partida):
    try:
        imagem = ImagemFim(partida)
        imagem.insere_nomes_de_times()
        imagem.monta_placar_rodape()
        imagem.monta_placar_final()
        return imagem.salva_e_retorna_url()
    except Exception, ex:
        logger.error(ex)
        return None


def cria_imagem_gol(partida, dados_placar):
    try:
        imagem = ImagemGol(partida, dados_placar)
        imagem.monta_placar_rodape()
        imagem.monta_placar_atual()
        imagem.insere_nome_de_time_que_fez_gol()
        return imagem.salva_e_retorna_url()
    except Exception, ex:
        logger.error(ex)
        return None
