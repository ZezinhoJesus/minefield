#
#Criando environment do jogo Mines no Gym

#TODO: Aplicar normalização para facilitar entrada na NN

'''
Espaço observado: x,y e (2*d+1)^2 sensores, onde d é o raio de visao
Ações: N, S, L, O
'''

import gym
import board
import utils
import numpy as np
import jogo

class MinefieldEnv(gym.Env):
	
	metadata = {'render.modes':['console', 'human']}
	BAIXO = jogo.BAIXO
	ESQ = jogo.ESQ
	DIR = jogo.DIR
	CIMA = jogo.CIMA
	
	def __init__(self, Na, Ma, pM, pl, d):
		
		super(MinefieldEnv,self).__init__()
	
		self.N = Na
		self.M = Ma
		self.pMina = pM
		self.pL = pl
		self.raio = d
		
		self.tabuleiro = jogo.Jogo(Na, Ma, pM, pl, d)
		
		self.tam_entrada = (2*d+1)**2 + 2

		#Limite para a penalidade
		self.maxPenalty = -1*(1+Na*Ma)*Na*Ma
		#Quantidade máxima de movimentos
		self.max_moves = (1+Na*Ma)*Na*Ma
		
		#4 movimentos possiveis: BAIXO, CIMA, ESQ, DIR
		self.action_space=gym.spaces.Discrete(4)
		#Espaco de observacao: eh um np array S onde:
		#S[0] = linha atual
		#S[1] = coluna atual
		#S[i > 1] = conjunto de (2*d+1)^2 sensores
		#Os sensores sao as posicoes ao redor do jogador
		self.observation_space = gym.spaces.Box(low=-5,high=8,shape=(1,self.tam_entrada,1),dtype=np.int8)
	
	def reset(self):
		
		#Tabuleiro
		self.tabuleiro = jogo.Jogo(self.N,self.M,self.pMina, self.pL, self.raio)
		
		#Reestabelece a quantidade maxima de movimentos
		self.max_moves = (1+self.N*self.M)*self.N*self.M
		
		sensor = utils.criar_sensor(self.tabuleiro.visao,self.tabuleiro.pos_i,self.tabuleiro.pos_j,self.tabuleiro.raio)
		return np.concatenate([np.array([self.tabuleiro.pos_i,self.tabuleiro.pos_j], dtype=np.int8),sensor])
		
	
	def step(self,action):
			 
		#Realizando o movimento
		res,cod = self.tabuleiro.mover(action)
		
		final = False
		
		if cod == board.LIMPO:
			#Se moveu e encontrou uma posicao segura
			#Premio negativo (living penalty)
			premio = -0.1
			#Um premio negativo incentiva uma quantidade mínima de movs
		elif cod == board.FIM:
			#Se moveu e encontrou o final
			#Finalizar o episodio
			final = True
			premio = 0
		elif cod == board.BOMBA:
			#Moveu em direcao a uma bomba
			#Punicao eh a quantidade de movimentos ja realizados
			premio = -1*self.tabuleiro.falhas
		elif cod == board.PAREDE or cod == board.FORA:
			#Tentou mover em direcao a parede
			premio = self.maxPenalty		
		
		#Controla a quantidade maxima de movimentos (steps)
		#evita loop infinito no agente (vai e volta)
		self.max_moves-=1
		if self.max_moves < 1:
			final = True
		
		#Cria os sensores com base na visao do jogador    
		sensor = utils.criar_sensor(self.tabuleiro.visao,self.tabuleiro.pos_i,self.tabuleiro.pos_j,self.raio)
		#Concatenando as coordenadas do jogador
		obs = np.concatenate([np.array([self.tabuleiro.pos_i,self.tabuleiro.pos_j], dtype=np.int8),sensor])
		info = {}
		
		return obs,premio,final,info
	
	def render(self, mode='console'):
		#if mode!='console':
		#	raise NotImplementedError()
		
		board.imprimir_visao(self.tabuleiro.campo,self.tabuleiro.visao,self.tabuleiro.pos_i,self.tabuleiro.pos_j)
		print('')

	def reconfigure(self,Na, Ma, pM, pl):
		#Reconfigura o agente para novos cenários
		self.N = Na
		self.M = Ma
		self.pMina = pM
		self.pL = pl
		self.reset()

class MinefieldEnvNorm(gym.Env):
	
	metadata = {'render.modes':['console', 'human']}
	BAIXO = jogo.BAIXO
	ESQ = jogo.ESQ
	DIR = jogo.DIR
	CIMA = jogo.CIMA
	
	def __init__(self, Na, Ma, pM, pl, d):
		
		super(MinefieldEnvNorm,self).__init__()
	
		self.N = Na
		self.M = Ma
		self.pMina = pM
		self.pL = pl
		self.raio = d
		
		self.tabuleiro = jogo.Jogo(Na, Ma, pM, pl, d)
		
		self.tam_entrada = (2*d+1)**2 + 2

		#Limite para a penalidade
		self.maxPenalty = -1*(1+Na*Ma)*Na*Ma
		self.max_moves = (1+Na*Ma)*Na*Ma
		
		#4 movimentos possiveis: BAIXO, CIMA, ESQ, DIR
		self.action_space=gym.spaces.Discrete(4)
		#Espaco de observacao: eh um np array S onde:
		#S[0] = linha atual
		#S[1] = coluna atual
		#S[i > 1] = conjunto de (2*d+1)^2 sensores
		#Os sensores sao as posicoes ao redor do jogador
		#self.observation_space = gym.spaces.Discrete((2*d+1)^2 + 2,dtype=np.int8)
		self.observation_space = gym.spaces.Box(low=-5,high=8,shape=(1,self.tam_entrada,1),dtype=np.float16)
	
	def reset(self):
		
		#Tabuleiro
		self.tabuleiro = jogo.Jogo(self.N,self.M,self.pMina, self.pL, self.raio)
		
		#Reestabelece a quantidade maxima de movimentos
		self.max_moves = (1+self.N*self.M)*self.N*self.M
		
		#Posicao do jogador
		x = float(self.tabuleiro.pos_i) / float(self.tabuleiro.visao.shape[0]-2) 
		y = float(self.tabuleiro.pos_j) / float(self.tabuleiro.visao.shape[1]-1)
		
		sensor = utils.criar_sensor(self.tabuleiro.visao,self.tabuleiro.pos_i,self.tabuleiro.pos_j,self.tabuleiro.raio, norm=True)
		return np.concatenate([np.array([x,y], dtype=np.float16),sensor])
	
	def step(self,action):
			 
		#Realizando o movimento
		res,cod = self.tabuleiro.mover(action)
		
		final = False
		
		if cod == board.LIMPO:
			#Se moveu e encontrou uma posicao segura
			#Premio negativo (living penalty)
			premio = -0.1
			#Um premio negativo incentiva uma quantidade mínima de movs
		elif cod == board.FIM:
			#Se moveu e encontrou o final
			#Finalizar o episodio
			final = True
			premio = 0
		elif cod == board.BOMBA:
			#Moveu em direcao a uma bomba
			#Punicao eh a quantidade de movimentos ja realizados
			premio = -1*self.tabuleiro.falhas
		elif cod == board.PAREDE or cod == board.FORA:
			#Tentou mover em direcao a parede
			premio = self.maxPenalty
		
		#Controla a quantidade maxima de movimentos (steps)
		#evita loop infinito no agente (vai e volta)
		self.max_moves-=1
		if self.max_moves < 1:
			final = True	
		
		#Posicao do jogador
		x = float(self.tabuleiro.pos_i) / float(self.tabuleiro.visao.shape[0]-2) 
		y = float(self.tabuleiro.pos_j) / float(self.tabuleiro.visao.shape[1]-1)
		
		#Cria os sensores com base na visao do jogador    
		sensor = utils.criar_sensor(self.tabuleiro.visao,self.tabuleiro.pos_i,self.tabuleiro.pos_j,self.raio, norm=True)
		#Concatenando as coordenadas do jogador
		obs = np.concatenate([np.array([x,y], dtype=np.float16),sensor])
		info = {}
		
		return obs,premio,final,info    
	
	
	def render(self, mode='console'):
		#if mode!='console':
		#	raise NotImplementedError()
		
		board.imprimir_visao(self.tabuleiro.campo,self.tabuleiro.visao,self.tabuleiro.pos_i,self.tabuleiro.pos_j)
		print('')

	def reconfigure(self,Na, Ma, pM, pl):
		#Reconfigura o agente para novos cenários
		self.N = Na
		self.M = Ma
		self.pMina = pM
		self.pL = pl
		self.reset()
