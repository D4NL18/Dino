from chrome_trex import MultiDinoGame, DinoGame, ACTION_UP, ACTION_FORWARD, ACTION_DOWN
import numpy as np

# Criação da rede neural
class NeuralNetwork:
    def __init__(self):
        # Define os pesos iniciais de cada entrada como valores aleatórios entre -0.5 e 0.5
        self.weights = np.random.rand(11, 3) - 0.5

    # Função de predição
    def predict(self, state):
        # Faz a multiplicação das entradas do state pela matriz pesos, gerando 3 valores
        output = np.dot(state, self.weights)
        # Aplica uma função de ativação (tanh) para deixar os valores entre -1 e 1
        activated_output = np.tanh(output)
        # Seleciona qual das 3 saídas tem o maior valor
        return np.argmax(activated_output)

# Função para prever ações para todos os dinossauros ou um dinossauro individual
def GamePredict(game, actions, states, population):
    if isinstance(population, list):  # Se for uma lista de redes neurais
        for i in range(game.dino_count):
            action = population[i].predict(states[i])
            if action < 0 or action >= len([ACTION_FORWARD, ACTION_UP, ACTION_DOWN]):
                action = ACTION_FORWARD
            actions.append([ACTION_FORWARD, ACTION_UP, ACTION_DOWN][action])
    else:  # Caso seja um único dinossauro
        action = population.predict(states)
        if action < 0 or action >= len([ACTION_FORWARD, ACTION_UP, ACTION_DOWN]):
            action = ACTION_FORWARD 
        actions.append([ACTION_FORWARD, ACTION_UP, ACTION_DOWN][action])
    return actions

def mutate(weights, mutation_rate):
    # Gera uma matriz aleatória multiplicada pelo mutation_rate e mistura com os pesos atuais
    return weights + mutation_rate * np.random.randn(*weights.shape)

def GameWithMutate(game, population, mutation_rate, quantDinos):
    best_score = -np.inf
    round_number = 0

    while True:
        actions = []
        states = game.get_state()

        actions = GamePredict(game, actions, states, population)
        game.step(actions)

        if game.game_over:
            scores = game.get_scores()
            best_index = np.argmax(scores)
            best_nn = population[best_index]
            best_score_current = scores[best_index]

            if best_score_current > best_score:
                best_score = best_score_current
                print("Matriz de pesos do melhor dinossauro:")
                print(best_nn.weights)

            population = [NeuralNetwork() for _ in range(quantDinos)]
            for i in range(quantDinos):
                population[i].weights = mutate(best_nn.weights, mutation_rate)

            round_number += 1
            print(f"Rodada: {round_number}")
            game.reset()

def crossover(parent1, parent2):
    crossover_point = np.random.randint(parent1.shape[0])
    child_weights = np.copy(parent1)
    child_weights[crossover_point:] = parent2[crossover_point:]
    return child_weights

def GameWithCrossover(game, population, mutation_rate, quantDinos):
    best_score = -np.inf
    round_number = 0

    while True:
        actions = []
        states = game.get_state()

        actions = GamePredict(game, actions, states, population)
        game.step(actions)

        if game.game_over:
            scores = game.get_scores()
            best_index = np.argmax(scores)
            best_nn = population[best_index]
            best_score_current = scores[best_index]

            if best_score_current > best_score:
                best_score = best_score_current
                print("Matriz de pesos do melhor dinossauro:")
                print(best_nn.weights)

            indices = np.arange(len(population))
            random_indices = indices[indices != best_index]
            random_index = np.random.choice(random_indices)
            random_nn = population[random_index]

            new_population = []
            for _ in range(quantDinos):
                child_weights = crossover(best_nn.weights, random_nn.weights)
                child_nn = NeuralNetwork()
                child_nn.weights = mutate(child_weights, mutation_rate)
                new_population.append(child_nn)

            population[:] = new_population

            round_number += 1
            print(f"Rodada: {round_number}")
            game.reset()

def PlayWithBestDino(game, best_weights):
    #Cria uma rede neural com os pesos do melhor dino
    best_nn = NeuralNetwork()
    best_nn.weights = best_weights
    round_number = 0

    while True:
        actions = []
        states = game.get_state()

        actions = GamePredict(game, actions, states, best_nn)
        game.step(actions)

        if game.game_over:
            round_number += 1
            print(f"Rodada: {round_number}")
            game.reset()

#Pesos do melhor dino
best_weights = np.array([
    [  8.0640569,    9.11712144, -16.4064385 ],
    [ 23.57264349, -14.94942409,   9.64703886],
    [  7.03968867,  -0.81293067,  -0.88890448],
    [-10.99236861,   1.03677696,  -6.24874142],
    [ -1.08200311,  -2.53855596,  -3.48121373],
    [ -7.03680494,  -5.23300955,  -4.92027629],
    [ -2.29960076,  -7.40798273,   9.47638314],
    [ -7.48486952,   2.02023094,   0.95415694],
    [  6.03186334,   6.84913901,  -1.25515494],
    [ -1.23575321,  -0.93629641,  -3.36262853],
    [  4.79784127,   5.36890202,  -9.3836535 ]
])

quantDinos = 100
FPS = 500

# Comente esta linha para jogar com o melhor dino
game = MultiDinoGame(dino_count=quantDinos, fps=FPS)

# Gera a população com uma rede neural para cada dinossauro
population = [NeuralNetwork() for _ in range(quantDinos)]

# Descomente a função que você deseja executar:

GameWithMutate(game, population, 0.3, quantDinos)
#GameWithCrossover(game, population, 0.3, quantDinos)

# Após terminar o algoritmo evolutivo, use a função abaixo para jogar com o melhor dinossauro encontrado:
#game2 = MultiDinoGame(dino_count=1, fps=FPS)
#PlayWithBestDino(game2, best_weights)
