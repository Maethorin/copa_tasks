import sys

__author__ = 'maethorin'


def finaliza(partida_id):
    from hamsters.fazendo.classificacao.tasks import finaliza_partida
    finaliza_partida.delay(partida_id)

if __name__ == "main":
    args = sys.argv
    if len(args) <= 1:
        print "Faltou o id da partida"
    else:
        finaliza(args[1])