from minefield_env import MinefieldEnvNorm
import random

random.seed(0) #reproduzir experimento

#%%
'''
A quantidade de entradas do modelo depende apenas do raio de visao
do agente. A entrada sempre será a posição do agente (x,y), normalizadas
e a quantidade de sensores (estado das casas ao redor do agente)
entradas = 2 + (2*raio + 1)^2
raio = 0 -> entradas = 3 (a posicao e o estado da sua propria casa)
raio = 1 -> entradas = 11 (a posicao e o estado dos vizinhos imediatos)
raio = 2 -> entradas = 27 (a posicao e o estado da vizinhança raio 2)

O ambiente aplica normalização a fim de melhorar o desempenho do modelo
'''


'''
CENÁRIO 1: CAMPO CURTO SEM MINAS
Motivação: treinar o agente a encontrar o final
'''

#criando ambiente
env = MinefieldEnvNorm(4,2,0.0,0.0,2)

env.reset()
#env.render()
#env.step(0)
estados = env.tam_entrada
estados2 = env.observation_space.shape[0]
acoes = env.action_space.n

#Esse ambiente pode ser reconfigurado para novos cenários
#parametros possíveis: tamanho e probabilidades
#O raio não pode ser alterado pois alteraria o tamanho da observacao

#%%
#Definindo modelo

from keras.layers import Dense,Flatten
from keras.models import Sequential
#from keras.optimizers import Adam

# model = Sequential()
# model.trainable = True
# model.add(Flatten(input_shape = (1, estados)))
# model.add(Dense(estados*2, activation='tanh'))
# model.add(Dense(estados*2, activation='tanh'))
# model.add(Dense(estados*2, activation='tanh'))
# model.add(Dense(acoes*2, activation='tanh'))
# model.add(Dense(acoes, activation='softmax'))
model = Sequential()
model.trainable = True
model.add(Flatten(input_shape = (1, estados)))
model.add(Dense(estados, activation='relu'))
model.add(Dense(estados, activation='relu'))
model.add(Dense(acoes*2, activation='relu'))
model.add(Dense(acoes, activation='relu'))
model.add(Dense(acoes, activation='relu'))

#%%
#Definindo política
from rl.agents import SARSAAgent
from rl.policy import EpsGreedyQPolicy
policy = EpsGreedyQPolicy()
sarsa = SARSAAgent(model = model, policy = policy, nb_actions = env.action_space.n)
sarsa.compile('adam', metrics = ['mse'])

#%%
'''
TREINAMENTO
CENÁRIO 1: CAMPO CURTO SEM MINAS
Motivação: treinar o agente a encontrar o final
'''

hist = sarsa.fit(env,nb_steps=200,verbose=2)

#%%
'''
Avaliando o comportamento do agente
'''
import numpy as np
#Avaliando a pontuacao em n tentativas, sem visualizacao
n_epi = 10
scores = sarsa.test(env, nb_episodes = n_epi, visualize= False)
print('Average score over 10 test games:{:.4}'.format(np.mean(scores.history['episode_reward'])))
print('Min score over 10 test games:{:.4}'.format(np.min(scores.history['episode_reward'])))
print('Max score over 10 test games:{:.4}'.format(np.max(scores.history['episode_reward'])))

#%%
#Faz o agente executar por duas vezes
nha = sarsa.test(env,nb_episodes = 2,visualize=True)

#%%
'''
EXPERIMENTO 1: AVALIANDO O AGENTE NUM ACAMPO MAIOR, SEM BOMBAS
Motivação: avaliar o treinamento do agente em encontrar o final
'''

env.reconfigure(20, 8, 0, 0)

#scores = sarsa.test(env, nb_episodes = 300, visualize= False)
#%%
env.reset()
scores = sarsa.test(env, nb_episodes = n_epi, visualize= False)
print('Average score over 10 test games:{:.4}'.format(np.mean(scores.history['episode_reward'])))
print('Min score over 10 test games:{:.4}'.format(np.min(scores.history['episode_reward'])))
print('Max score over 10 test games:{:.4}'.format(np.max(scores.history['episode_reward'])))

#%%
#Faz o agente executar por duas vezes
env.reset()
nha = sarsa.test(env,nb_episodes = 2,visualize=True)

#%%
#Treinando o agente para explorar melhor o ambiente
#sarsa.fit(env,nb_steps=3000,verbose=1)

#%%Salvando esse agente
sarsa.save_weights('sarsa_CENARIO1.h5f', overwrite=True)

#%%
'''
TREINAMENTO
CENÁRIO 2: UNICO CAMINHO EM LINHA RETA
Motivação: treinar o agente a encontrar em qual linha está o caminho. Note que
existem minas em toda casa fora do caminho
'''

env.reconfigure(10, 5, 1, 0.2)
env.reset()
#%%
hist = sarsa.fit(env,nb_steps=100000,visualize=False,verbose=2)

#%%
#Testando modelo
obs = env.reset()
acao = model.predict(obs.reshape(1,1,estados))

#%%
k = 0
final = False
while(k < 100 and not final):
    obs,premio,final,info = env.step(acao.argmax())
    print('Reward: ', premio, 'Acao ', acao.argmax(), acao[0,acao.argmax()])
    k+=1