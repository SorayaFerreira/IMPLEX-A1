# Módulos criados com os algoritmos de ordenação
import bubble_sort
import insertion_sort
# Bibliotecas para funções auxiliares
import random
import math
import sys
import time
# Bibliotecas para visualização do gráfico
import matplotlib.pyplot as plt
import numpy as np


#-------Funções para geração de vetores específicos-------#

def gerar_numeros_aleatorios(n: int) -> list:
    """
    Esta função recebe 'n' como o tamanho do vetor a ser 
    gerado e retorna uma lista com n números aleatórios, sendo
    que os valores dentro do vetor não podem ultrapassar o número 
    'n'.
    """ 
    # 'n' limitação para manter o tempo do counting sort linear
    numeros = [random.randint(0, n) for _ in range(n)]
    return numeros

  
def gerar_vetor_quase_ordenado(n: int) -> list:
    """
    Essa função recebe 'n' como o tamanho do vetor a ser gerado
    e retorna uma lista com n números aleatórios, 90% ordenados
    de modo crescente e 10% desordenados, escolhidos aleatoriamente. 
    """
    numeros = [random.randint(0, n) for _ in range(n)]

    numeros.sort()

    i_toshuffle = [random.randint(0, n-1) for _ in range(math.ceil(0.1 * n))]
    #lista de índices das posições que serão trocadas 

    for i in range(0, len(i_toshuffle)):
        numeros[i_toshuffle[i]] = random.randint(0, n)

    return numeros


def gerar_grafico(tamanhos, tempos_bubble, tempos_insertion, escolha: int, stp):
    """
    Essa função tem o objetivo de gerar o gráfico para melhor visualização dos tempos
    de execução dos algoritmos. Ela recebe um vetor com todos os tamanhos de vetor testados,
    listas com os tempos de execução de cada algoritmo, conforme o tamanho, um inteiro para
    exibir o título do gráfico de acordo com a escolha de teste, e o step para espaçar os pontos
    de medição do gráfico.
    """
    fig, ax = plt.subplots()

    ax.plot(tamanhos, tempos_bubble, label='Bubble', marker='o')
    ax.plot(tamanhos, tempos_insertion, label='Insertion', marker='o')

    xticks_interval = stp
    xticks = np.arange(min(tamanhos), max(tamanhos) + xticks_interval, xticks_interval)
    ax.set_xticks(xticks)

    ax.set_xlabel('Tamanho do Vetor')
    ax.set_ylabel('Tempo de Execução (segundos)')

    if escolha == 1 :
        ax.set_title('Vetor Aleatório')
    elif escolha == 2:
        ax.set_title('Vetor Quase Ordenado')
    elif escolha == 3:
        ax.set_title('Vetor Ordenado')
    else:
        # Se a escolha for 4
        ax.set_title('Vetor Reverso')
    ax.legend()
    ax.grid(True)

    plt.show()


#-------Funções para testar os algoritmos-------#

def testar_vetor_aleatorio(fim: int, inc: int, stp: int):
    """
    Esta função recebe os parâmetro escolhidos pelo usuário e realiza os testes
    apenas com o vetor aleatório, para a escolha 1. Ela mede os tempos de execução,
    calculando uma média de tempos, cria listas com todos as médias para cada algoritmo
    de ordenação, e exibe no terminal a tebela com as médias de tempo para cada tamanho
    de vetor testado. 
    """    
    rpt = int(input("\tParâmetro rpt (número de repetições para média): "))

    print()
    print(f"{'Tamanho':<10}{'Bubble':<10}{'Insertion':<10}")

    # É o número de pontos de medição que o gráfico deverá apresentar
    n_pontos = ((fim - inc) // stp)+ 1

    # Aqui são as listas de testes, em cada posição haverá a média dos tempos de execução 
    tempos_bubble = [0.0] * n_pontos
    tempos_insertion = [0.0] * n_pontos
    tamanhos = []

    indice_tempos = 0 # iterador para percorrer o número de pontos de medição

    for n in range(inc, fim + 1, stp):
        """
        Soma os valores de tamanho dos vetores para teste, a partir dos quais será construído o gráfico.
        Em outras palavras, percorre os pontos de medição, em que 'n' assume o tamanho atual do vetor.
        """
        tamanhos.append(n)
        
        for _ in range(0, rpt):
            """
            Roda o número de casos de teste para o vetor aleatório, a fim de obter, 
            ao final, uma média dos tempos de execução de cada algoritmo.
            """
            vetor = gerar_numeros_aleatorios(n)

            #cópias do vetor gerado aleatóriamente para passagem como parâmetro para cada algoritmo de ordenação
            copia_bubble = vetor.copy()
            copia_insertion = vetor.copy()

            # Medindo tempo do BUBBLE SORT
            start = time.time()
            bubble_sort.bubble_sort(copia_bubble, len(copia_bubble))
            end = time.time()
            tempos_bubble[indice_tempos] += (end - start)

            # Medindo tempo do INSERTION SORT
            start = time.time()
            insertion_sort.insertion_sort(copia_insertion)
            end = time.time()
            tempos_insertion[indice_tempos] += (end - start)
        
        # Coloca a média na posição corresponde da lista de testes, conforme o tamanho do vetor utilizado.
        tempos_bubble[indice_tempos] /= rpt
        tempos_insertion[indice_tempos] /= rpt

        # exibe uma linha da tabela no terminal
        print(f"{n:<10}{tempos_bubble[indice_tempos]:<10.6f}{tempos_insertion[indice_tempos]:<10.6f}")

        indice_tempos += 1

    gerar_grafico(tamanhos, tempos_bubble, tempos_insertion, 1, stp)
    print()


def testar_caso_unico(fim: int, inc: int, stp: int, escolha: int):
    """
    Gera os testes para cada caso que não necessita de repetições para
    realizar uma média de tempos - escolhas 2, 3 e 4. Recebe os parâmetros
    dados pelos usuário e o inteiro com a escolha.
    """
    print()
    print(f"{'Tamanho':<10}{'Bubble':<10}{'Insertion':<10}")

    # É o número de pontos de medição que o gráfico deverá apresentar
    n_pontos = ((fim - inc) // stp)+ 1

    # Aqui são as listas de testes, em cada posição haverá o tempo de execução de um algoritmo 
    tempos_bubble = [0.0] * n_pontos
    tempos_insertion = [0.0] * n_pontos
    tamanhos = [] # guarda a lista de valores n que o vetor

    indice_tempos = 0 # iterador para percorrer o número de pontos de medição

    for n in range(inc, fim + 1, stp):
        """
        Soma os valores de tamanho dos vetores para teste, a partir dos quais será construído o gráfico.
        Em outras palavras, percorre os pontos de medição, em que 'n' assume o tamanho atual do vetor.
        """

        tamanhos.append(n)
        

        if escolha == 2:
            # recebe um vetor com 10% de seus valores embaralhados entre si.
            vetor = gerar_vetor_quase_ordenado(n)
            
        elif escolha == 3:
            vetor = [value for value in range(0, n+1)]

        else: 
            # Gera o vetor decrescente
            vetor = [value for value in range(n, 0, -1)]

        #cópias do vetor gerado aleatóriamente para passagem como parâmetro para cada algoritmo de ordenação
        copia_bubble = vetor.copy()
        copia_insertion = vetor.copy()

        # Medindo tempo do BUBBLE SORT
        start = time.time()
        bubble_sort.bubble_sort(copia_bubble, len(copia_bubble))
        end = time.time()
        tempos_bubble[indice_tempos] += (end - start)

        # Medindo tempo do INSERTION SORT
        start = time.time()
        insertion_sort.insertion_sort(copia_insertion)
        end = time.time()
        tempos_insertion[indice_tempos] += (end - start)
        
        print(f"{n:<10}{tempos_bubble[indice_tempos]:<10.6f}{tempos_insertion[indice_tempos]:<10.6f}")

        indice_tempos += 1

    gerar_grafico(tamanhos, tempos_bubble, tempos_insertion, escolha, stp)
    print()

#----------- MAIN -----------#

def main():
    # Foi necessário aumentar o limite de chamadas recursivas
    sys.setrecursionlimit(100000)

    print("\n\
          \t[1] Testar caso vetor aleatório;\n\
           \t[2] Testar caso vetor quase ordenado;\n\
           \t[3] Testar caso vetor ordenado;\n\
           \t[4] Testar caso vetor reverso;\n\
           Escolha: ", end='')   
    escolha = int(input())

    inc = int(input("\tParâmetro inc (tamanho inicial do vetor): "))
    fim = int(input("\tParâmetro fim (tamanho final do vetor): "))
    stp = int(input("\tParâmetro stp (intervalos entre os tamanhos): "))

    if escolha == 1:
        start = time.time()
        testar_vetor_aleatorio(fim, inc, stp)
        end = time.time()
        print(f"\nTempo total: {(end-start)//60}")

    elif escolha == 2:
        start = time.time()
        testar_caso_unico(fim, inc, stp, 2)
        end = time.time()
        print(f"\nTempo total: {(end-start)//60}")

    elif escolha == 3:
        start = time.time()
        testar_caso_unico(fim, inc, stp, 3)
        end = time.time()
        print(f"\nTempo total: {(end-start)//60}")

    elif escolha == 4:
        start = time.time()
        testar_caso_unico(fim, inc, stp, 4)
        end = time.time()
        print(f"\nTempo total: {(end-start)//60}")

    else:
        print("Escolha inválida!")
           

if __name__ == '__main__':
    main()