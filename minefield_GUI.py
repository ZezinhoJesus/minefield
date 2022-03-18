import pygame
from pygame.locals import *
import board
import utils
import jogo

LARGURA_TOTAL = 1000
ALTURA_TOTAL = 600
#Divisao em duas telas
#Tela 1: mapa completo
#Tela 2: visao do jogador
TELA1_L = int(LARGURA_TOTAL*0.7)
TELA2_L = int(LARGURA_TOTAL*0.3)

MARGEM = 30
TELA1_X0 = MARGEM
TELA2_X0 = TELA1_L + MARGEM
TELA_Y0 = 30
#AREA_W = LARGURA_TOTAL - 2*TELA1_X0
#AREA_H = ALTURA_TOTAL - 2*MARGEM_H

class GUI():

	def __init__(self):
		'''
		Construtor.
		Inicializa o PyGame
		Configurações globais da tela
		'''
		pygame.init()

		#Parametros da Tela
		self.tela = pygame.display.set_mode((LARGURA_TOTAL,ALTURA_TOTAL))
		pygame.display.set_caption('Campo Minado')
		#Flag para controlar se existe jogo em andamento
		self.ativo = False
		self.jogo = None

	def __del__(self):
		pygame.quit()
		self.ativo = False

	def novoJogo(self,objJogo):
		'''
		Inicia um jogo novo, configurando um tabuleiro
		Recebe como parametro um objeto Jogo
		'''
		#Parametros do jogo
		self.jogo = objJogo
		self.ativo = True

		self.CELL_L = (TELA1_L - 2*MARGEM) // self.jogo.visao.shape[1]
		self.CELL_A = (ALTURA_TOTAL - 2*TELA_Y0) // self.jogo.visao.shape[0]

		self.SENS_L = (TELA2_L - 2*MARGEM) // (2*self.jogo.raio+1)
		self.SENS_A = (ALTURA_TOTAL - 2*TELA_Y0) // self.jogo.visao.shape[0]
		TELA2_Y0 = ALTURA_TOTAL//2-self.jogo.raio*self.SENS_A

		#Carregando imagens de jogador no campo
		self.pic_player = pygame.transform.scale(pygame.image.load('pic/jog_ok.png').convert_alpha(),(self.CELL_L,self.CELL_A))
		self.pic_fail = pygame.transform.scale(pygame.image.load('pic/jog_fail.png'),(self.CELL_L,self.CELL_A))

		#Criando lista de imagens no tabuleiro e no sensor
		self.list_key = []
		self.list_valor = []
		self.list_valor_sensor = []

		#Carregando imagens do tabuleiro e do sensor
		#O tamanho das imagens são ajustados ao tamanho de cada tela

		#Chao eh DUVIDA
		self.list_valor.append(pygame.transform.scale(pygame.image.load('pic/chao.png'),(self.CELL_L,self.CELL_A)))
		self.list_valor_sensor.append(pygame.transform.scale(pygame.image.load('pic/chao.png'),(self.SENS_L,self.SENS_A)))
		self.list_key.append(board.DUVIDA)
		#Mina eh FALHA
		self.list_valor.append(pygame.transform.scale(pygame.image.load('pic/mina.png'),(self.CELL_L,self.CELL_A)))
		self.list_valor_sensor.append(pygame.transform.scale(pygame.image.load('pic/mina.png'),(self.SENS_L,self.SENS_A)))
		self.list_key.append(board.FALHA)
		#Parede eh parede
		self.list_valor.append(pygame.transform.scale(pygame.image.load('pic/parede.png'),(self.CELL_L,self.CELL_A)))
		self.list_valor_sensor.append(pygame.transform.scale(pygame.image.load('pic/parede.png'),(self.SENS_L,self.SENS_A)))
		self.list_key.append(board.PAREDE)
		#Fim eh fim
		self.list_valor.append(pygame.transform.scale(pygame.image.load('pic/fim.png'),(self.CELL_L,self.CELL_A)))
		self.list_valor_sensor.append(pygame.transform.scale(pygame.image.load('pic/fim.png'),(self.SENS_L,self.SENS_A)))
		self.list_key.append(board.FIM)

		#Os campos LIMPO recebem a quantidade de minas ao redor
		for i in range(9):
			#Cada celula possui 8 vizinhos. Logo, a quantidade de minas ao redor vai de 0 a 8
			self.list_valor.append(pygame.transform.scale(pygame.image.load('pic/'+str(i)+'.png'),(self.CELL_L,self.CELL_A)))
			self.list_valor_sensor.append(pygame.transform.scale(pygame.image.load('pic/'+str(i)+'.png'),(self.SENS_L,self.SENS_A)))
			self.list_key.append(i)

		#Criando um dicionario para facilitar a escolha das imagens da celula
		self.img_dict = dict(zip(self.list_key,self.list_valor))

		#Criando um dicionario para facilitar a escolha das imagens da visao do sensor
		self.imgSens_dict = dict(zip(self.list_key,self.list_valor_sensor))

		#Fontes e textos
		self.font = pygame.font.SysFont('Castellar',24)
		self.renderizar()

	def renderizar(self, wait = 0):
		'''
		Renderiza a tela
		'''

		if (not self.ativo):
			texto = 'Não há jogo em andamento'
			self.tela.blit(font.render(texto, True,(100,100,100), (50,50,50)), (2*TELA1_X0,ALTURA_TOTAL-TELA_Y0))
			return

		self.tela.fill((50,50,50))
		#variaveis temporarias para simplificar o codigo
		pos_i = self.jogo.pos_i
		pos_j = self.jogo.pos_j
		raio = self.jogo.raio

		#Renderizando tabuleiro
		for i in range(self.jogo.visao.shape[0]):
			for j in range(self.jogo.visao.shape[1]):
				x = TELA1_X0 + j*self.CELL_L
				y = TELA_Y0 + i*self.CELL_A
				self.tela.blit(self.img_dict[self.jogo.visao[i,j]],(x,y))

		#Calculando posicao do jogador
		x = TELA1_X0 + pos_j*self.CELL_L
		y = TELA_Y0 + pos_i*self.CELL_A
		#Renderizando jogador
		if (self.jogo.visao[i,j]!=board.FALHA):
			self.tela.blit(self.pic_player,(x,y))
		else:
			self.tela.blit(self.pic_fail,(x,y))

		sensor = utils.criar_sensor(self.jogo.visao,pos_i,pos_j,raio).reshape(2*raio+1,2*raio+1)

		#Renderizando a Tela 2 com os sensores
		for i in range(sensor.shape[0]):
			for j in range(sensor.shape[1]):
				x = TELA2_X0 + j*self.SENS_L
				y = TELA_Y0 + i*self.SENS_A
				self.tela.blit(self.imgSens_dict[sensor[i,j]],(x,y))

		#Renderizando a pontuação
		texto = '  Movimentos: '+str(self.jogo.moves)+' '+'Falhas: '+str(self.jogo.falhas)+'     '
		self.tela.blit(self.font.render(texto, True,(100,100,100), (50,50,50)), (2*TELA1_X0,ALTURA_TOTAL-TELA_Y0))

		pygame.display.update()
		if (wait > 0):
			pygame.time.wait(wait)

	def executarAcoes(self,listaAcoes, espera = 500):
		'''
		Recebe uma lista de acoes
		Executa cada uma e renderiza o resultado na tela
		'''
		
		for acao in listaAcoes:
			res,cod = self.jogo.mover(acao)
			
			if res:
				#Movimento realizado
				self.renderizar()
				if espera > 0:
					pygame.time.wait(min(espera,2000))
				if cod == board.FIM:
					self.ativo = False


	def jogarInterativo(self, espera = 500):
		'''
		Executa uma partida com um jogador humano
		'''
		if espera > 0:
			tempo = min(2000,max(espera,500))
		
		self.renderizar(tempo)
		
		while(self.ativo):

			for event in pygame.event.get():
				res = False
				
				if event.type == QUIT:
					pygame.quit()
					quit()

				if event.type == pygame.KEYDOWN:
					
					if event.key == pygame.K_q:
						#Desistiu
						self.jogo.finalizar()
						self.renderizar(tempo)

					if event.key == pygame.K_RIGHT:
						res,cod = self.jogo.mover(jogo.DIR)
					if event.key == pygame.K_LEFT:
						res,cod = self.jogo.mover(jogo.ESQ)
					if event.key == pygame.K_UP:
						res,cod = self.jogo.mover(jogo.CIMA)
					if event.key == pygame.K_DOWN:
						res,cod = self.jogo.mover(jogo.BAIXO)
						
					if res:
						self.renderizar(tempo)
					
					if cod == board.FIM:
						self.ativo = False
