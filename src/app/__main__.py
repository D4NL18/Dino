from newDinoGame import MultiDinoGame, ACTION_UP, ACTION_FORWARD, ACTION_DOWN
import numpy as np

# Criação da rede neural
class NeuralNetwork:
    def __init__(self):
        self.weights = np.random.rand(10, 3) - 0.5

    def predict(self, state):
        output = np.dot(state, self.weights)
        activated_output = np.tanh(output)
        return np.argmax(activated_output)

def GamePredict(game, actions, states, population):
    if isinstance(population, list):
        for i in range(game.dino_count):
            action = population[i].predict(states[i])
            if action < 0 or action >= len([ACTION_FORWARD, ACTION_UP, ACTION_DOWN]):
                action = ACTION_FORWARD
            actions.append([ACTION_FORWARD, ACTION_UP, ACTION_DOWN][action])
    else:
        action = population.predict(states)
        if action < 0 or action >= len([ACTION_FORWARD, ACTION_UP, ACTION_DOWN]):
            action = ACTION_FORWARD 
        actions.append([ACTION_FORWARD, ACTION_UP, ACTION_DOWN][action])
    return actions

def mutate(weights, mutation_rate):
    return weights + mutation_rate * np.random.randn(*weights.shape)

def GameWithMutate(game, population, mutation_rate, quantDinos):
    best_score = -np.inf
    round_number = 0
    best_nn = None
    best_weights = None

    while True:
        actions = []
        states = game.get_state()

        actions = GamePredict(game, actions, states, population)
        game.step(actions)

        if game.game_over or any(score >= 9999 for score in game.get_scores()):
            scores = game.get_scores()
            best_index = np.argmax(scores)
            best_nn = population[best_index]
            best_score_current = scores[best_index]

            if best_score_current > best_score:
                best_score = best_score_current
                best_weights = best_nn.weights  # Armazenar os pesos do melhor dinossauro
                print("Matriz de pesos do melhor dinossauro:")
                print(best_weights)

            population = [best_nn] + [NeuralNetwork() for _ in range(quantDinos-1)]
            for i in range(1, quantDinos):
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
    best_nn = None
    best_weights = None

    while True:
        actions = []
        states = game.get_state()

        actions = GamePredict(game, actions, states, population)
        game.step(actions)

        if game.game_over or any(score >= 9999 for score in game.get_scores()):
            scores = game.get_scores()
            best_index = np.argmax(scores)
            best_nn = population[best_index]
            best_score_current = scores[best_index]

            if best_score_current > best_score:
                best_score = best_score_current
                best_weights = best_nn.weights  # Armazenar os pesos do melhor dinossauro
                print("Matriz de pesos do melhor dinossauro:")
                print(best_weights)

            indices = np.arange(len(population))
            random_indices = indices[indices != best_index]
            random_index = np.random.choice(random_indices)
            random_nn = population[random_index]

            new_population = [best_nn]
            for _ in range(1, quantDinos):
                child_weights = crossover(best_nn.weights, random_nn.weights)
                child_nn = NeuralNetwork()
                child_nn.weights = mutate(child_weights, mutation_rate)
                new_population.append(child_nn)

            population[:] = new_population

            round_number += 1
            print(f"Rodada: {round_number}")
            game.reset()

def PlayWithBestDino(game, best_weights):
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

# Pesos do melhor dino
best_weights = np.array([
                    [ 0.05873744, -0.18737166,  0.15162923],
                    [ 0.37904898, -0.29948954, -0.208433  ],
                    [-0.22294232, -0.39653523, -0.30959169],
                    [-0.18026223,  0.31192445, -0.52114996],
                    [ 0.12461262,  0.44634745,  0.29608551],
                    [ 0.36585901,  0.52571237,  0.18866291],
                    [-0.20084327,  0.34464733,  0.1182346 ],
                    [ 0.1549635,   0.17118189,  0.14192513],
                    [-0.40021329, -0.01655103, -0.33633056],
                    [-0.1028232 , -0.31744194, -0.06333987]])

quantDinos = 100
FPS = 500
game = MultiDinoGame(dino_count=quantDinos, fps=FPS)
population = [NeuralNetwork() for _ in range(quantDinos)]

#GameWithMutate(game, population, 0.3, quantDinos)
#GameWithCrossover(game, population, 0.3, quantDinos)

# Após terminar o algoritmo evolutivo, use a função abaixo para jogar com o melhor dinossauro encontrado:
game2 = MultiDinoGame(dino_count=1, fps=FPS)
PlayWithBestDino(game2, best_weights)
