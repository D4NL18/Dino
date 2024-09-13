from chrome_trex import DinoGame, ACTION_UP, ACTION_FORWARD, ACTION_DOWN
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


def mutate(weights):
    #Coeficiente de mutação. Indica o quanto o neurônio será mutado
    mutation_rate = 0.05
    #Gera uma matriz aleatória multiplicada pelo mutation_rate e mistura com os pesos atuais 
    return weights + mutation_rate * np.random.randn(*weights.shape)

#Criação do objeto do jogo com 100 dinossauros e 60 fps
game = MultiDinoGame(dino_count=100, fps=60)

#Gera a população com uma rede neural para cada dinossauro
population = [NeuralNetwork() for _ in range(100)]

#Loop principal do jogo
while True:
    actions = []
    states = game.get_state()

    # Decidir ação de cada dinossauro
    for i in range(game.dino_count):
        #Para cada dinossauro, realizar o predict da ação
        action = population[i].predict(states[i])
        #Inserir o predict da ação na lista de execução
        actions.append([ACTION_FORWARD, ACTION_UP, ACTION_DOWN][action])

    # Realizar uma ação baseado na lista de ações a serem executadas
    game.step(actions)

    #Ao final de cada rodada
    if game.game_over:
        # Selecionar qual foi o melhor dinossauro
        best_index = np.argmax(game.get_scores())
        best_nn = population[best_index]

        # Criar nova população
        population = [NeuralNetwork() for _ in range(100)]
        for i in range(100):
            #Nova população vai ter os pesos do melhor dinossauro, sofrendo mutações
            population[i].weights = mutate(best_nn.weights)

        # Proxima rodada
        game.reset()