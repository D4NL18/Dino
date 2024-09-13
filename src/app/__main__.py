from chrome_trex import MultiDinoGame, ACTION_UP, ACTION_FORWARD, ACTION_DOWN
import numpy as np


#Criação da rede neural
class NeuralNetwork:
    def __init__(self):
        #Define os pesos iniciais de cada entrada como valores aleatorios 0 ou 1
        self.weights = np.random.rand(11, 3) - 0.5  #-0.5 para que valores sejam negativos ou positivos [-0.5, 0.5]

    #Função de predição
    def predict(self, state):
        #Faz a multiplicação das entradas do state pela matriz pesos, gerando 3 valores
        output = np.dot(state, self.weights)
        #Seleciona qual das 3 saídas do resultado da multiplicação anterior que tem o maior valor (escolha que a rede avaliou como certa)
        return np.argmax(output)

def GamePredict(game, actions, states, population):
    for i in range(game.dino_count):
                #Para cada dinossauro, realizar o predict da ação
                action = population[i].predict(states[i])
                #Inserir o predict da ação na lista de execução
                actions.append([ACTION_FORWARD, ACTION_UP, ACTION_DOWN][action])
    return actions

def mutate(weights, mutation_rate):
    #Gera uma matriz aleatória multiplicada pelo mutation_rate e mistura com os pesos atuais 
    return weights + mutation_rate * np.random.randn(*weights.shape)


def GameWithMutate(game, population, mutation_rate, quantDinos):

    #Loop principal do jogo
    while True:
        actions = []
        states = game.get_state()

        #Decidir ação de cada dinossauro
        actions = GamePredict(game, actions, states, population)

        #Realizar uma ação baseado na lista de ações a serem executadas
        game.step(actions)

        #Ao final de cada rodada
        if game.game_over:
            #Selecionar qual foi o melhor dinossauro
            best_index = np.argmax(game.get_scores())
            best_nn = population[best_index]

            #Criar nova população
            population = [NeuralNetwork() for _ in range(quantDinos)]
            for i in range(quantDinos):
                #Nova população vai ter os pesos do melhor dinossauro, sofrendo mutações
                population[i].weights = mutate(best_nn.weights, mutation_rate)

            #Proxima rodada
            game.reset()


def crossover(parent1, parent2):
    #Seleciona um ponto de corte aleatório do pai1
    crossover_point = np.random.randint(parent1.shape[0])
    #Cria o filho igual ao pai1
    child_weights = np.copy(parent1)
    #Mistura o  filho com o pai2 a partir do ponto de corte
    child_weights[crossover_point:] = parent2[crossover_point:]
    #Retorna o filho gerado
    return child_weights


def GameWithCrossover(game, population, mutation_rate, quantDinos):

    #Loop principal do jogo
    while True:
        actions = []
        states = game.get_state()

        #Decidir ação de cada dinossauro
        actions = GamePredict(game, actions, states, population)

        #Realizar uma ação baseado na lista de ações a serem executadas
        game.step(actions)

        #Ao final de cada rodada
        if game.game_over:
            #Obter as pontuações
            scores = game.get_scores()
            #Encontrar o melhor dinossauro
            best_index = np.argmax(scores)
            best_nn = population[best_index]
            # Selecionar um dinossauro aleatório
            indices = np.arange(len(population))
            random_indices = indices[indices != best_index]
            random_index = np.random.choice(random_indices)
            random_nn = population[random_index]

            # Criar nova população
            new_population = []
            for _ in range(quantDinos):
                #Realizar crossover entre o melhor e o segundo melhor dinossauro
                child_weights = crossover(best_nn.weights, random_nn.weights)
                child_nn = NeuralNetwork()
                child_nn.weights = mutate(child_weights, mutation_rate)
                new_population.append(child_nn)

            # Atualizar a população
            population[:] = new_population

            # Próxima rodada
            game.reset()


quantDinos = 300
FPS = 500

game = MultiDinoGame(dino_count=quantDinos, fps=FPS)   

#Gera a população com uma rede neural para cada dinossauro
population = [NeuralNetwork() for _ in range(quantDinos)]

#GameWithMutate(game, population, 0.5, quantDinos)
GameWithCrossover(game, population, 0.3, quantDinos)