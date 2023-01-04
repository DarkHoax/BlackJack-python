import random, sys

COPAS = chr(9829)  # ♥
OUROS = chr(9830)  # ♦
ESPADAS = chr(9824)  # ♠
PAUS = chr(9827)  # ♣

BACKSIDE = 'backside'

def getBet(maxBet):
    # PERGUNTA AO JOGADOR O QUANTO ELE QUER GASTAR
    while True:
        print(f"Quanto quer apostar? 1 - {maxBet} or QUIT")
        bet = input('> ').upper().strip()
        if bet == 'QUIT':
            print("Obrigado por jogar")
            sys.exit()

        if not bet.isdecimal():
            continue

        bet = int(bet)
        if 1 <= bet <= maxBet:
            return bet


def getDeck():
    deck = []
    for suit in (COPAS, OUROS, ESPADAS, PAUS):
        for rank in range(2, 11):
            deck.append((str(rank), suit))

        for rank in ('J', 'Q', 'K', 'A'):
            deck.append((rank, suit))

    random.shuffle(deck)
    return deck


def mostrarMaos(jogadorMao, bancaMao, mostrarbancaMao):
    print()
    if mostrarbancaMao:
        print('Banca:', getValorMao(bancaMao))
        mostrarCartas(bancaMao)
    else:
        print('Banca: ???', getValorMao(bancaMao))
        mostrarCartas([BACKSIDE] + bancaMao[1:])

    print('JOGADOR:', mostrarMaos(jogadorMao))
    # DIZ QUE TEM UM ERRO AQUI, QUE É PARA MOSTRAR BANCA E O QUE A BANCA TEM NAS MAOS, POREM SO QUERO A MAO DO JOGADOR
    mostrarCartas(jogadorMao)


def getValorMao(cartas):
    valor = 0
    numdeAs = 0

    for carta in cartas:
        rank = carta[0]
        if rank == 'A':
            numdeAs += 1
        elif rank in ('K', 'Q', 'J'):
            valor += 10
        else:
            valor += int(rank)

    valor += numdeAs
    for i in range(numdeAs):
        if valor + 10 <= 21:
            valor += 10

    return valor


def mostrarCartas(cartas):
    linhas = ['', '', '', '']
    for i, carta in enumerate(cartas):
        linhas[0] += ' ___  '
        if carta == BACKSIDE:
            linhas[1] += '|## | '
            linhas[2] += '|###| '
            linhas[3] += '|_##| '
        else:
            rank, suit = carta
            linhas[1] += '|{} | '.format(rank.ljust(2))
            linhas[2] += '| {} | '.format(suit)
            linhas[3] += '|_{}| '.format(rank.rjust(2, '_'))

    for linha in linhas:
        print(linha)


def getMovimento(jogadorMao, dinheiro):
    while True:
        movimentos = ['(H)it', '(S)tand']
        if len(jogadorMao) == 2 and dinheiro > 0:
            movimentos.append('(D)ouble down')
        moverPrompt = ', '.join(movimentos) + '> '
        movimento = input(moverPrompt).upper()
        if movimento in ('H', 'S'):
            return movimento
        if movimento == 'D' and '(D)ouble down' in movimentos:
            return movimento

def main():
    """

    :rtype: object
    """
    print('''BLACKJACK também conhecido como 21 no Brasil.
        \nRegras do jogo: 
        \nTente chegar a 21 pontos ou próximo disso sem que a banca chegue primeiro
        \nReis (K), Rainhas (Q) e Valetes (J) valem 10 pontos cada um
        \nÁs (A) valem 1 ou 11 pontos
        \nDe (H)it para pegar outra carta, de (S)tand para ficar com o naipe e parar o jogo
        \nNa sua primeira jogada, você pode (D)obrar para aumentar sua aposta, mas deve acertar exatamente mais uma vez antes de parar.
        \nEm caso de empate, a aposta é devolvida ao jogador. A banca para de bater quando soma 17''')

    dinheiro = 5000

    while True:  # LOOP INFINITO DO JOGO
        if dinheiro <= 0:
            print("PARECE-ME QUE TU ESTÁS QUEBRADO")
            print("POR SORTE NAO JOGASTE COM DINHEIRO DE VERDADE")
            print("VALEU POR JOGAR")
            sys.exit()

        print("Saldo: R$", dinheiro)
        bet = getBet(dinheiro)

        # DANDO AO JOGADOR E A BANCA DUAS CARTAS DA MESA
        deck = getDeck()
        bancaMao = [deck.pop(), deck.pop()]
        jogadorMao = [deck.pop(), deck.pop()]

        print("Aposta: R$", bet)
        while True:
            mostrarMaos(jogadorMao, bancaMao, False)
            print()

            if getValorMao(jogadorMao) > 21:
                print("Voce perdeu... Banca estourada")
                break

            movimento = getMovimento(jogadorMao, dinheiro - bet)

            if movimento == 'D':
                adicionalBet = getBet(min(bet, dinheiro - bet))
                bet += adicionalBet
                print(f"Aposta aumentada para R${bet:<.2f}")
                print("Aposta: R$", bet)

            if movimento in ('H', 'D'):
                novaCarta = deck.pop()
                rank, suit = novaCarta
                print(f"Voce pegou {rank} de {suit}")
                jogadorMao.append(novaCarta)
                if getValorMao(jogadorMao) > 21:
                    print("Voce perdeu... Banca estourada")
                    continue

            if movimento in ('S', 'D'):
                break  # JOGADOR PARA DE JOGAR

        if getValorMao(jogadorMao) <= 21:
            while getValorMao(bancaMao) < 17:
                print("A banca pega uma carta")
                bancaMao.append(deck.pop())
                mostrarMaos(jogadorMao, bancaMao, False)

                if getValorMao(bancaMao) > 21:
                    print("A banca ultrapassou 21 pontos")
                    break
                input("Enter para continuar: ")
                print("\n\n")

        # MOSTRANDO O FINAL
        mostrarMaos(jogadorMao, bancaMao, True)

        jogadorValor = getValorMao(jogadorMao)
        bancaValor = getValorMao(bancaMao)

        if bancaValor > 21:
            print(f"Banca estourada. Voce ganhou R${bet:<.2f}")
            dinheiro += bet

        elif (jogadorValor > 21) or (jogadorValor < bancaValor):
            print("Tu perdestes")
            dinheiro -= bet

        elif jogadorValor > bancaValor:
            print(f"Voce ganhou R${bet:<.2f}")
            dinheiro += bet

        elif jogadorValor == bancaValor:
            print("Empate. Valor retornado")

        input("Enter para continuar")
        print("\n\n")

if __name__ == '__main__':
    main()
