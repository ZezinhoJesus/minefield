#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  gameGUI.py
#  
#  Copyright 2021 josep <josep@VINGADORNOVO>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import pygame
from pygame.locals import *
pygame.init()
import board
import utils

#class Player(pygame.sprite.Sprite):
#	'''
#	O Jogador eh um sprite
#	'''
#	def __init__(self,startpos):
#		pygame.sprite.Sprite.__init__(self)
#		self.alive = True
		


#Parametros do jogo
N = 10
M = 3
campo,visao = board.inicializar_tab(N, M, probMina = 0.6, pLO=0.5)
jog_i = 0
jog_j = campo.shape[1] // 2
jog_vivo = True
#Distancia/raio do sensor
raio = 2
#sensor = utils.criar_sensor(visao,jog_i,jog_j,raio) 
falhas = 0
moves = 0
fim = False


#Parametros da Tela
LARGURA_TOTAL = 1000
ALTURA_TOTAL = 600
tela = pygame.display.set_mode((LARGURA_TOTAL,ALTURA_TOTAL))
pygame.display.set_caption('Campo Minado')
#tempo = pygame.time.Clock()

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
CELL_L = (TELA1_L - 2*MARGEM) // visao.shape[1]
CELL_A = (ALTURA_TOTAL - 2*TELA_Y0) // visao.shape[0]

SENS_L = (TELA2_L - 2*MARGEM) // (2*raio+1)
SENS_A = (ALTURA_TOTAL - 2*TELA_Y0) // visao.shape[0]
TELA2_Y0 = ALTURA_TOTAL//2-raio*SENS_A

#Carregando imagens de jogador no campo
pic_player = pygame.transform.scale(pygame.image.load('pic/jog_ok.png').convert_alpha(),(CELL_L,CELL_A))
pic_fail = pygame.transform.scale(pygame.image.load('pic/jog_fail.png'),(CELL_L,CELL_A))

#Criando lista de imagens no tabuleiro e no sensor
list_key = []
list_valor = []
list_valor_sensor = []

#Carregando imagens do tabuleiro e do sensor
#O tamanho das imagens são ajustados ao tamanho de cada tela

#Chao eh DUVIDA
list_valor.append(pygame.transform.scale(pygame.image.load('pic/chao.png'),(CELL_L,CELL_A)))
list_valor_sensor.append(pygame.transform.scale(pygame.image.load('pic/chao.png'),(SENS_L,SENS_A)))
list_key.append(board.DUVIDA)
#Mina eh FALHA
list_valor.append(pygame.transform.scale(pygame.image.load('pic/mina.png'),(CELL_L,CELL_A)))
list_valor_sensor.append(pygame.transform.scale(pygame.image.load('pic/mina.png'),(SENS_L,SENS_A)))
list_key.append(board.FALHA)
#Parede eh parede
list_valor.append(pygame.transform.scale(pygame.image.load('pic/parede.png'),(CELL_L,CELL_A)))
list_valor_sensor.append(pygame.transform.scale(pygame.image.load('pic/parede.png'),(SENS_L,SENS_A)))
list_key.append(board.PAREDE)
#Fim eh fim
list_valor.append(pygame.transform.scale(pygame.image.load('pic/fim.png'),(CELL_L,CELL_A)))
list_valor_sensor.append(pygame.transform.scale(pygame.image.load('pic/fim.png'),(SENS_L,SENS_A)))
list_key.append(board.FIM)

#Os campos LIMPO recebem a quantidade de minas ao redor
for i in range(9):
	list_valor.append(pygame.transform.scale(pygame.image.load('pic/'+str(i)+'.png'),(CELL_L,CELL_A)))
	list_valor_sensor.append(pygame.transform.scale(pygame.image.load('pic/'+str(i)+'.png'),(SENS_L,SENS_A)))
	list_key.append(i)

#Criando um dicionario para facilitar a escolha das imagens da celula
img_dict = dict(zip(list_key,list_valor)) 

#Criando um dicionario para facilitar a escolha das imagens da visao do sensor
imgSens_dict = dict(zip(list_key,list_valor_sensor))

#Fontes e textos
font = pygame.font.SysFont('Castellar',24)

def renderizar_visao():
	'''
	Renderiza apenas a visao do jogador.
	A posicao atual do jogador e as casas vizinhas
	'''
	sensor = utils.criar_sensor(visao,jog_i,jog_j,raio).reshape(2*raio+1,2*raio+1)

	#Renderizando tabuleiro
	for i in range(sensor.shape[0]):
		for j in range(sensor.shape[1]):
			x = TELA2_X0 + j*SENS_L
			y = TELA2_Y0 + i*SENS_A
			tela.blit(imgSens_dict[sensor[i,j]],(x,y))
	
	

def renderizar(total = True):
	'''
	Renderiza a tela
	Se total = True, renderiza tudo.
	Se total = False, renderiza apenas a posicao do jogador
	se
	'''
	
	if (total == True):
		
		#Renderizando tabuleiro
		for i in range(visao.shape[0]):
			for j in range(visao.shape[1]):
				x = TELA1_X0 + j*CELL_L
				y = TELA_Y0 + i*CELL_A
				#rect = pygame.Rect(x, y, CELL_L, CELL_A)
				#pygame.draw.rect(tela, (20,20,20), rect, 1)
				#DEBUG
				tela.blit(img_dict[visao[i,j]],(x,y))

	#Calculando posicao do jogador
	x = TELA1_X0 + jog_j*CELL_L
	y = TELA_Y0 + jog_i*CELL_A
	#Renderizando jogador
	if (jog_vivo):
		tela.blit(pic_player,(x,y))
	else:
		tela.blit(pic_fail,(x,y))
	
	#Renderizando a pontuação
	texto = '  Movimentos: '+str(moves)+' '+'Falhas: '+str(falhas)+'     '
	tela.blit(font.render(texto, True,(100,100,100), (50,50,50)), (2*TELA1_X0,ALTURA_TOTAL-TELA_Y0))

	pygame.display.update()
	#tempo.tick(60)

#DEV Teste inicial
#v = board.completar_visao(campo)
tela.fill((50,50,50))
renderizar()
renderizar_visao()
while(True):
		
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			quit()
		
		if not fim and event.type == pygame.KEYDOWN:
			dx = 0
			dy = 0
			if event.key == pygame.K_q:
				#Desistiu
				fim = True
				visao = board.completar_visao(campo)
				renderizar_visao()
				renderizar()
				
			if event.key == pygame.K_RIGHT:
				dx = 1
			if event.key == pygame.K_LEFT:
				dx = -1
			if event.key == pygame.K_UP:
				dy = -1
			if event.key == pygame.K_DOWN:
				dy = 1
	
			if (dx != 0 or dy != 0):
				res,cod = board.mover_para(campo,visao,jog_i+dy,jog_j+dx)
			
				if (res):
				#movimento realizado
					jog_i+=dy
					jog_j+=dx
					moves+=1
				
				if (cod == board.FIM):
					#Jogo finalizado
					fim = True
					visao = board.completar_visao(campo)
				else:
					if (cod == board.BOMBA):
						#Encontrou mina
						falhas+=1
						jog_vivo=False
						#Renderiza por 1 segundo
						renderizar_visao()
						renderizar()
						pygame.time.wait(2000)
						jog_vivo=True
						jog_i = 0
						jog_j = campo.shape[1] // 2
			
				renderizar_visao()
				renderizar()
				pygame.time.wait(1000)
			
