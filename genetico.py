import numpy as np
import random
import sys
sys.path.append('chrome_trex')

from chrome_trex import DinoGame


# Sinta-se livre para brincar com os valores abaixo

CHANCE_MUT = .03      # Chance de mutação de um peso qualquer
CHANCE_CO = .23      # Chance de crossing over de um peso qualquer
NUM_INDIVIDUOS = 100  # Tamanho da população
NUM_MELHORES = 4     # Número de indivíduos que são mantidos de uma geração para a próxima


def ordenar_lista(lista, ordenacao, decrescente=True):
    """
    Argumentos da Função:
        lista: lista de números a ser ordenada.
        ordenacao: lista auxiliar de números que define a prioridade da
        ordenação.
        decrescente: variável booleana para definir se a lista `ordenacao`
        deve ser ordenada em ordem crescente ou decrescente.
    Saída:
        Uma lista com o conteúdo de `lista` ordenada com base em `ordenacao`.
    Por exemplo,
        ordenar_lista([2, 4, 5, 6], [7, 2, 5, 4])
        # retorna [2, 5, 6, 4]
        ordenar_lista([1, 5, 4, 3], [3, 8, 2, 1])
        # retorna [5, 1, 4, 3]
    """
    return [x for _, x in sorted(zip(ordenacao, lista), key=lambda p: p[0], reverse=decrescente)]


def populacao_aleatoria(n):
    """
    Argumentos da Função:
        n: Número de indivíduos
    Saída:
        Uma população aleatória. População é uma lista de indivíduos,
        e cada indivíduo é uma matriz 3x10 de pesos (números).
        Os indivíduos podem tomar 3 ações (0, 1, 2) e cada linha da matriz
        contém os pesos associados a uma das ações.
    """
    # Referência: np.random.uniform()
    #             list.append()
    #             for loop (for x in lista:)
    populacao = []
    for i in range(n):
        individuo = np.random.uniform(-3,3,(3,10))
        populacao.append(individuo)
    return populacao


def valor_das_acoes(individuo, estado):
    """
    Argumentos da Função:
        individuo: matriz 3x10 com os pesos do indivíduo.
        estado: lista com 10 números que representam o estado do jogo.
    Saída:
        Uma lista com os valores das ações no estado `estado`. Calcula os valores
        das jogadas como combinações lineares dos valores do estado, ou seja,
        multiplica a matriz de pesos pelo estado.
    """
    # Referência: multiplicação de matrizes (A @ B)
    valores_das_acoes = np.array(individuo) @ np.array(estado)
    return valores_das_acoes


def melhor_jogada(individuo, estado):
    """
    Argumentos da Função:
        individuo: matriz 3x10 com os pesos do indivíduo.
        estado: lista com 10 números que representam o estado do jogo.
    Saída:
        A ação de maior valor (0, 1 ou 2) calculada pela função valor_das_acoes.
    """
    # Referência: np.argmax()
    return np.argmax(valor_das_acoes(individuo,estado))

def mutacao(individuo):
    """
    Argumentos da Função:
        individuo: matriz 3x10 com os pesos do indivíduo.
    Saída:
        Essa função não tem saída. Ela apenas modifica os pesos do indivíduo,
        de acordo com chance CHANCE_MUT para cada peso.
    """
    # Referência: for loop (for x in lista)
    #             np.random.uniform()
    # A modificação dos pesos pode ser feita de diversas formas (vide slides)
    for i in range(len(individuo)):
        for j in range(len(individuo[i])):
            if random.random() < CHANCE_MUT:
                individuo[i][j] = individuo[i][j] +  np.random.uniform(-10,10)


def crossover(individuo1, individuo2):
    """
    Argumentos da Função:
        individuoX: matriz 3x10 com os pesos do individuoX.
    Saída:
        Um novo indivíduo com pesos que podem vir do `individuo1`
        (com chance 1-CHANCE_CO) ou do `individuo2` (com chance CHANCE_CO),
        ou seja, é um cruzamento entre os dois indivíduos. Você também pode pensar
        que essa função cria uma cópia do `individuo1`, mas com chance CHANCE_CO,
        copia os respectivos pesos do `individuo2`.
    """
    # Referência: for loop (for x in lista)
    #             np.random.uniform()
    filho = []
    for i in range(len(individuo1)):
        pesos = []
        for j in range(len(individuo1[i])):         
            if random.random() < 1 - CHANCE_CO:
                pesos.append(individuo1[i][j])
            else:
                pesos.append(individuo2[i][j])
        filho.append(pesos)
    return filho


def calcular_fitness(jogo, individuo):
    """
    Argumentos da Função:
        jogo: objeto que representa o jogo.
        individuo: matriz 3x10 com os pesos do individuo.
    Saída:
        O fitness calculado de um indivíduo. Esse cálculo é feito simulando um
        jogo e calculando o fitness com base nessa simulação. O modo mais simples
        é usando fitness = score do jogo.
    """
    # Referência: while loop (while condition)
    #             np.random.uniform()

    # Você precisará da função melhor_jogada()

    # O jogo é simulado usando:
    #   jogo.reset()
    #   jogo.game_over
    #   jogo.step(acao)  # Toma a ação `acao` e vai para o próximo frame
    #   jogo.get_score()
    #   jogo.get_state()

    jogo.reset()
    while not jogo.game_over:
        acao = melhor_jogada(individuo,jogo.get_state())
        jogo.step(acao)
    return jogo.get_score()


def proxima_geracao(populacao, fitness):
    """
    Argumentos da Função:
        populacao: lista de indivíduos.
        fitness: lista de fitness, uma para cada indivíduo.
    Saída:
        A próxima geração com base na população atual.
        Para criar a próxima geração, segue-se o seguinte algoritmo:
          1. Colocar os melhores indivíduos da geração atual na próxima geração.
          2. Até que a população esteja completa:
             2.1. Escolher aleatoriamente dois indivíduos da geração atual.
             2.2. Criar um novo indivíduo a partir desses dois indivíduos usando
                  crossing over.
             2.3. Mutar esse indivíduo.
             2.4. Adicionar esse indivíduo na próxima geração
    """
    # Referência: random.choices()
    #             while loop (while condition)
    #             lista[a:b]

    # Dica: lembre-se da função `ordenar_lista(lista, ordenacao)`.

    proxima_ger = []

    # Adicionar os melhores indivíduos da geração atual na próxima geração
    melhores = ordenar_lista(populacao,fitness)
    proxima_ger = melhores[:NUM_MELHORES] 
    while len(proxima_ger) < NUM_INDIVIDUOS:
        # Selecionar 2 indivíduos, realizar crosover e mutação,
        # e adicionar o novo indivíduo à próxima geração
        #
        # Você pode usar a função random.choices(populacao, weights=None, k=2) para selecionar `k`
        # elementos aleatórios da população.
        #
        # Se vc passar o argumento `weights`, os indivíduos serão escolhidos com base nos pesos
        # especificados (elementos com pesos maiores são escolhidos mais frequentemente).
        # Uma ideia seria usar o fitness como peso.
        dois_individuos = random.choices(proxima_ger, k=2)
        for i in range(len(populacao)):
            mutacao(populacao[i]) 
        filho = crossover(dois_individuos[0],dois_individuos[1])
        
        proxima_ger.append(filho)
        
    return proxima_ger


def mostrar_melhor_individuo(jogo, populacao, fitness):
    """
    Argumentos da Função:
        jogo: objeto que representa o jogo.
        populacao: lista de indivíduos.
        fitness: lista de fitness, uma para cada indivíduo.
    Saída:
        Não há saída. Simplesmente mostra o melhor indivíduo de uma população.
    """
    # VOCÊ NÃO PRECISA MEXER NESSA FUNÇÂO

    fps_antigo = jogo.fps
    jogo.fps = 30
    ind = populacao[max(range(len(populacao)), key=lambda i: fitness[i])]
    print('Melhor individuo:', ind)
    while True:
        if input('Pressione enter para rodar o melhor agente. Digite q para sair. ') == 'q':
            jogo.fps = fps_antigo
            return
        fit = calcular_fitness(jogo, ind)
        print('Fitness: {:4.1f}'.format(jogo.get_score()))


###############################
# CÓDIGO QUE RODA O ALGORITMO #
###############################

# Referência: for loop (for x in lista)
#             list.append()

# OBS: Todos os prints dentro dessa função são opcionais.
#      Eles estão aqui para facilitar a visualização do algoritmo.

num_geracoes = 100
jogo = DinoGame(fps=0)

# Crie a população usando populacao_aleatoria(NUM_INDIVIDUOS)
populacao = populacao_aleatoria(NUM_INDIVIDUOS)

print('ger | fitness\n----+-' + '-'*5*NUM_INDIVIDUOS)

for ger in range(num_geracoes):
    # Crie uma lista `fitness` com o fitness de cada indivíduo da população
    # (usando a função calcular_fitness e um `for` loop).

    # Atualize a população usando a função próxima_geração.

    fitness = []
    for i in populacao:
        fitness.append(calcular_fitness(jogo,i))
    populacao = proxima_geracao(populacao, fitness )

    print('{:3} |'.format(ger),
          ' '.join('{:4d}'.format(s) for s in sorted(fitness, reverse=True)))

    # Opcional: parar se o fitness estiver acima de algum valor (p.ex. 300)

mostrar_melhor_individuo(jogo, populacao, fitness)
