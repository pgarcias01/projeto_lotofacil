from projeto_lotofacil.GerarCsv import update_result
from projeto_lotofacil.BuscaResultado import buscar_resultado


update_result()
numeros = [[1,4,5,6,7,11,14,16,17,18,20,21,22,23,25],
[1,3,4,7,9,10,12,13,14,15,16,19,23,24,25],
[1,4,6,8,12,14,15,16,17,18,20,21,22,23,25],
[1,3,5,9,11,12,13,14,15,16,18,19,20,21,22]]



def conferir(aposta, concurso):
    resultado = buscar_resultado(concurso)
    result_numeros = resultado['numbers']
    ganhos = 0
    acertos = []
    for jogo in aposta:
        pontuacao = 0
        for numero in jogo:
            if numero in result_numeros:
                pontuacao += 1
        acertos.append(pontuacao)
    for acerto in acertos:
        if acerto == 11:
            ganhos += resultado['p11']
        elif acerto == 12:
            ganhos += resultado['p12']
        elif acerto == 13:
            ganhos += resultado['p13']
        elif acerto == 14:
            ganhos += resultado['p14']
        elif acerto == 15:
            ganhos += resultado['p15']

    print(f'CONCURSO {concurso} da Lotofácil:')
    print(f'Números sorteados: {result_numeros}')
    print('PREMIOS DISTRIBUIDOS:.')
    print(f' 15 acertos: {resultado["p15"]}')
    print(f' 14 acertos: {resultado["p14"]}')
    print(f' 13 acertos: {resultado["p13"]}')
    print(f' 12 acertos: {resultado["p12"]}')
    print(f' 11 acertos: {resultado["p11"]}')
    print()
    print('-='*30)
    for x in range(0, len(aposta)):
        print(f'Jogo {x+1} números apostados:  {sorted(aposta[x])}  Acertou o total de: {acertos[x]} números')
    print('-='*30)
    if max(acertos) <= 10:
        print(f'Infelizmente você não ganhou nada')
    else:
        print(f'PARABÉNS VOCÊ GANHOU R${ganhos:.2f}')
