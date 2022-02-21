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

#class Player(pygame.sprite.Sprite):
#	'''
#	O Jogador eh um sprite
#	'''
#	def __init__(self,startpos):
#		pygame.sprite.Sprite.__init__(self)
#		self.alive = True
		

#Parametros do jogo
N = 10
M = 5
campo,visao = board.inicializar_tab(N, M, probMina = 0.8, pLO=0.5)
jog_i = 0
jog_j = campo.shape[1] // 2
jog_vivo = True
falhas = 0
moves = 0
fim = False

#Parametros da Tela
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
tela = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
pygame.display.set_caption('Campo Minado')
tempo = pygame.time.Clock()

MARGEM_W = 60
MARGEM_H = 40
#AREA_W = WINDOW_WIDTH - 2*MARGEM_W
#AREA_H = WINDOW_HEIGHT - 2*MARGEM_H
CELL_W = (WINDOW_WIDTH - 2*MARGEM_W) // visao.shape[1]
CELL_H = (WINDOW_HEIGHT - 2*MARGEM_H) // visao.shape[0]

#Carregando imagens de jogador
pic_player = pygame.transform.scale(pygame.image.load('pic/jog_ok.png').convert_alpha(),(CELL_W,CELL_H))
pic_fail = pygame.transform.scale(pygame.image.load('pic/jog_fail.png'),(CELL_W,CELL_H))

#Criando lista de imagens no tabuleiro
list_key = []
list_valor = []


#Chao eh DUVIDA
list_valor.append(pygame.transform.scale(pygame.image.load('pic/chao.png'),(CELL_W,CELL_H)))
list_key.append(board.DUVIDA)
#Mina eh FALHA
list_valor.append(pygame.transform.scale(pygame.image.load('pic/mina.png'),(CELL_W,CELL_H)))
list_key.append(board.FALHA)
#Parede eh parede
list_valor.append(pygame.transform.scale(pygame.image.load('pic/parede.png'),(CELL_W,CELL_H)))
list_key.append(board.PAREDE)
#Fim eh fim
list_valor.append(pygame.transform.scale(pygame.image.load('pic/fim.png'),(CELL_W,CELL_H)))
list_key.append(board.FIM)

#Os campos LIMPO recebem a quantidade de minas ao redor
for i in range(9):
	list_valor.append(pygame.transform.scale(pygame.image.load('pic/'+str(i)+'.png'),(CELL_W,CELL_H)))
	list_key.append(i)

#Criando um dicionario para facilitar a escolha das imagens
img_dict = dict(zip(list_key,list_valor)) 

#Fontes e textos
font = pygame.font.SysFont('Castellar',24)

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
				x = MARGEM_W + j*CELL_W
				y = MARGEM_H + i*CELL_H
				rect = pygame.Rect(x, y, CELL_W, CELL_H)
				pygame.draw.rect(tela, (20,20,20), rect, 1)
				#DEBUG
				tela.blit(img_dict[visao[i,j]],(x,y))

	#Calculando posicao do jogador
	x = MARGEM_W + jog_j*CELL_W
	y = MARGEM_H + jog_i*CELL_H
	#Renderizando jogador
	if (jog_vivo):
		tela.blit(pic_player,(x,y))
	else:
		tela.blit(pic_fail,(x,y))
	
	#Renderizando a pontuação
	texto = '  Movimentos: '+str(moves)+' '+'Falhas: '+str(falhas)+'     '
	tela.blit(font.render(texto, True,(100,100,100), (50,50,50)), (2*MARGEM_W,WINDOW_HEIGHT-MARGEM_H))

	pygame.display.update()
	tempo.tick(60)

#DEV Teste inicial
#v = board.completar_visao(campo)
tela.fill((50,50,50))
renderizar()
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
						renderizar()
						pygame.time.wait(2000)
						jog_vivo=True
						jog_i = 0
						jog_j = campo.shape[1] // 2
			
				renderizar()
				pygame.time.wait(1000)
			
