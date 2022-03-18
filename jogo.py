#Jogo
import board
import utils
import copy
from pynput import keyboard
from time import sleep

BAIXO = 0
ESQ = 1
DIR = 2
CIMA = 3

class Jogo():
	def __init__(self,N,M,pM,pL,d):
		'''
		Cria uma nova instancia de jogo
		'''
		self.campo,self.visao = board.inicializar_tab(N,M,probMina = pM, pLO=pL)
		#Raio de visao
		self.raio = d

		#Posicao do jogador
		self.pos_i = 0
		self.pos_j = self.campo.shape[1] // 2
		self.falhas = 0
		self.moves = 0

		#Jogo finalizado
		self.fim = False

	def mover(self, acao):
		'''
		Realiza um movimento
		'''

		if self.fim:
			#O jogo ja finalizou
			#Movimento nao realizado
			return False,board.FORA

		di = 0
		dj = 0
		if acao == BAIXO:
			di=1
		elif acao == CIMA:
			di=-1
		elif acao == DIR:
			dj=1
		elif acao == ESQ:
			dj=-1

		#Realizando o movimento
		res,cod = board.mover_para(self.campo,self.visao,self.pos_i+di,self.pos_j+dj)

		if cod == board.LIMPO:
			#Se moveu e encontrou uma posicao segura
			#Contabiliza o movimento
			self.moves+=1
			self.pos_i+=di
			self.pos_j+=dj
		elif cod == board.FIM:
			#Se moveu e encontrou o final
			#Contabiliza o movimento
			self.moves+=1
			self.pos_i+=di
			self.pos_j+=dj
			self.fim = True
			self.visao = board.completar_visao(self.campo)
		elif cod == board.BOMBA:
			#Moveu em direcao a uma bomba
			#Contabiliza o movimento
			self.moves+=1
			self.falhas+=1
			#Volta para posicao inicial
			self.pos_i=0
			self.pos_j=self.visao.shape[1]//2

		return res,cod

	def copiar(self):
		'''
		Cria uma copia do jogo no seu estado atual
		Essa copia é independente da original
		'''
		#N = self.campo.shape[0]
		#M = self.campo.shape[1]
		#j = self.Jogo(N,M) #repensar isso, nao eh eficiente inicializar
		j = copy.copy(self)
		j.campo = self.campo.copy()
		j.visao = self.visao.copy()
		
		return j
		

	def imprimir(self):
		'''
		Imprime o jogo no console
		'''
		board.imprimir_visao(self.campo,self.visao,self.pos_i,self.pos_j)

	def finalizar(self):
		'''
		Finaliza um jogo
		'''
		self.fim = True
		self.visao = board.completar_visao(self.campo)

	def jogarInterativo(self):
		'''
		Realiza uma partida com jogador humano
		Saida no console
		'''

		board.imprimir_visao(self.campo,self.visao,self.pos_i,self.pos_j)
		print('Use as teclas de navegação (ou pressione s para SAIR).')

		while(not self.fim):

			dx = 0
			dy = 0
			sen = utils.criar_sensor(self.visao,self.pos_i,self.pos_j,self.raio)
			utils.ver_sensor(sen,self.raio)
			with keyboard.Events() as events:
				event = events.get(1e6)
				if event.key == keyboard.KeyCode.from_char('s'):
					print("Sair")
					board.revelar_tabela(self.campo,self.visao,self.pos_i,self.pos_j)
					self.fim = True
				if event.key == keyboard.Key.right:
					dx = 1
				if event.key == keyboard.Key.left:
					dx = -1
				if event.key == keyboard.Key.up:
					dy = -1
				if event.key == keyboard.Key.down:
					dy = 1

			if (dx != 0 or dy != 0):
				res,cod = board.mover_para(self.campo,self.visao,self.pos_i+dy,self.pos_j+dx)
				if (res):
					#movimento realizado
					self.pos_i+=dy
					self.pos_j+=dx
					self.moves+=1

					if (cod == board.FIM):
						self.fim = True
						print('Você venceu! Falhas = ',self.falhas, '. Movimentos = ',self.moves)
						board.revelar_tabela(self.campo,self.visao,self.pos_i,self.pos_j)
						break
					else:
						if (cod == board.BOMBA):
							self.pos_i = 0
							self.pos_j = self.campo.shape[1] // 2
							self.falhas+=1
							print('Detonado!!')

				board.imprimir_visao(self.campo,self.visao,self.pos_i,self.pos_j)
				print('Use as teclas de navegação (ou pressione s para SAIR).')
				print('Falhas = ',self.falhas, '. Movimentos = ',self.moves)
				sleep(1)

#j = Jogo(10,4,0.5,0.3,2)
#j.jogarInterativo()
