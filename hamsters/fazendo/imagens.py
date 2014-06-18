#!/usr/bin/env python
# encoding: utf-8
from hamsters import settings

__author__ = 'maethorin'

from PIL import Image, ImageFont, ImageDraw
from slugify import slugify


def cria_imagem_inicio_jogo(partida):
    try:
        caminho_base = settings.CAMINHO_IMAGENS
        base = Image.open("{}base-inicio-jogo.png".format(caminho_base))
        nome_time_1 = slugify(partida.time_1.nome)
        nome_time_2 = slugify(partida.time_2.nome)
        bandeira1 = Image.open("{}bandeiras/{}.png".format(caminho_base, nome_time_1))
        bandeira2 = Image.open("{}bandeiras/{}.png".format(caminho_base, nome_time_2))
        base.paste(bandeira1, (60, 275), bandeira1)
        base.paste(bandeira2, (283, 275), bandeira2)
        font_nome = ImageFont.truetype("{}Graduate-Regular.ttf".format(caminho_base), 23)
        draw = ImageDraw.Draw(base)
        largura_nome_2, altura_nome_2 = draw.textsize(partida.time_2.nome, font=font_nome)
        left_2 = 400 - largura_nome_2 - 15
        draw.text((15, 110), partida.time_1.nome, font=font_nome, fill=(10, 75, 10))
        draw.text((left_2, 195), partida.time_2.nome, font=font_nome, fill=(10, 75, 10))

        font_placar = ImageFont.truetype("{}Graduate-Regular.ttf".format(caminho_base), 43)
        draw.text((138, 280), str(partida.media_palpites_time_1()), font=font_placar, fill=(219, 216, 0))
        draw.text((233, 280), str(partida.media_palpites_time_2()), font=font_placar, fill=(219, 216, 0))
        nome_da_imagem = "comeeeeca-{}-{}.png".format(nome_time_1, nome_time_2)
        base.save("{}img/comeeeca/{}".format(settings.STATIC_ROOT, nome_da_imagem))
        return "{}img/comeeeca/{}".format(settings.STATIC_URL, nome_da_imagem)
    except:
        return None