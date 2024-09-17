# DinoGame

Réplica do "jogo do dinossauro" do google. A ideia do projeto consiste em clonar o repositório do jogo e, baseado nele, desenvolver uma inteligência artificial baseada em computação evolutiva para jogar automaticamente e alcançar o maior score possível.

# Algorimos escolhidos

Foram desenvolvidos algoritmos de Mutation e de Crossover + Mutation. Também houve a tentativa de implementar o crossover "puro", isto é, sem mutation. Contudo, devido à semelhança entre os dinossauros, principalmente no começo, onde diversos dinossauros realizam o mesmo comportamento, não foi possível obter uma variabilidade genética suficiente apenas com este método.

# Class NeuralNetwork

Para ambos os métodos, foi utilizada uma mesma classe NeuralNetwork, que consiste na rede neural que irá ser aplicada nos dinossauros. A classe consiste na criação de uma matriz com 11 valores de entrada e 3 saídas (up, down e forward), e a definição de valores aleatórios [-0.5; 0.5]. A classe também possui a função predict, que consiste na atribuição dos pesos na rede neural e na identificação de qual a melhor saída baseado nisso.

# Function GamePredict

loop que irá percorrer a lista que contém todos os dinossauros existentes no jogo e, para cada um deles, irá realizar a predição de qual a melhor saída (ação).


# Mutation

Para a aplicação do método Mutation, foram criadas duas funções, sendo elas "Mutate" e "GameWithMutate". 

A primeira delas consiste na aplicação da mutação de fato, na qual será gerada uma matriz aleatória multiplicada pelo mutation_rate e mistura com os pesos atuais, isto é, irá misturar a matriz de pesos do dinossauro escolhido com pequenos valores aleatórios definidos pelo "mutation_rate", que define o nível de mutação que será realizada.

Já o GameWithMutation consiste no loop principal de execução do jogo que utiliza o Mutation puro. Primeiro, será gerada uma lista de ações contendo a predição para cada dinossauro, utilizando o GamePredict(), depois irá executar cada ação e, por fim, quando der gameover, irá identificar o melhor dinossauro e gerar uma nova população tendo este como base, mas aplicando a função "mutate" para realizar a mutação em cada um.


# Crossover + Mutation

Seguindo uma lógica semelhante, para o Crossover + Mutation, foram criadas duas novas funções, sendo elas a "Crossover" e a "GameWithCrossover", além da utilização da função "Mutate" citada anteriormente.

A função Crossover receberá como parametros os dois dinossauros "pai", definir um ponto de crossover aleatório e definir que os pesos que vierem antes do ponto definido serão referentes ao pai 1 e o que vier após o ponto será referente ao pai 2.

Já a função GameWithCrossover segue uma lógica semelhante à GameWithMutate, tendo como unica diferença que, para criar a nova população, será feito um crossover entre o melhor dinossauro e algum dinossauro aleatório, aplicando a função Crossover explicada anteriormente. Após a realização do Crossover, será realizada uma mutação no novo indivíduo gerado, utilizando a função Mutate anterior.

# Análise de resultados

Foram realizados testes de ambos os algoritmos. Para cada um deles, foi feita a comparação, também, entre diferentes valores de "mutation_rate", que equivale ao quanto cada dinossauro gerado irá se diferir do seu predecessor. Para o Mutation, foram testados os valores de 0.1, 0.3 e 0.5, enquanto para o Crossover + Mutation, foram testados os valores de 0.1 e 0.3. Em todos os testes, foram atribuidos os valores de 240 FPS, que controlava basicamente a velocidade dos testes, e 100 dinossauros,. Todas as tentativas foram realizadas em um tempo de 3 minutos. Os resultados obtidos podem ser analisados abaixo.

|           | Mutate 0.1 | Mutate 0.3 | Mutate 0.5 | Crossover 0.1 | Crossover 0.3 |
|-----------|------------|------------|------------|---------------|---------------|
| Tentativa 1 | 304        | 510        | 209        | 556           | 563           |
| Tentativa 2 | 510        | 520        | 425        | 513           | 436           |
| Tentativa 3 | 499        | 606        | 449        | 308           | 456           |
| **MÉDIA**   | **437,67** | **545,33** | **361,00** | **459,00**    | **485,00**    |


A partir da análise dos resultados demonstrados acima, é possível identificar que, para ambos os métodos, o valor de mutation_rate ideal foi de 0.3. É importante destacar também que, apesar do esperado ser que o método mais completo tenha um resultado melhor, a utilização do Mutate "puro" obteve um resultado médio mais satisfatório do que a união do mesmo método com o crossover.
