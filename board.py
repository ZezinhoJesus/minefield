#Funcoes relacionadas a tabela

import numpy as np
import random
from termcolor import cprint
import colorama

colorama.init()

#Estados
FALHA = -6
DUVIDA = -5
FORA = -4
CAM = -2
FIM = -3
PAREDE = -1
LIMPO = 0
BOMBA = 1

def criar_tab(N,M):
	'''
	Cria uma tabela vazia com dimensoes N e M
	Retorna a tabela e a visao da tabela
	'''
	N = max(2,N)
	#criar tabuleiro N linhas x M colunas
	#retorna o tabuleiro do jogo e a visao do tabuleiro
	t = np.full((N+1,M),LIMPO,dtype=np.int8)
	t = np.concatenate( (np.full((1,M),PAREDE,dtype=np.int8),
		t,
		np.full((1,M),FIM,dtype=np.int8),
		np.full((1,M),PAREDE,dtype=np.int8)))
	#'''
	t = np.concatenate(
	(np.full((t.shape[0],1),PAREDE,dtype=np.int8),
	t,
	np.full((t.shape[0],1),PAREDE,dtype=np.int8)),
	axis = 1)
	
	v = criar_visao(t)
	#'''
	return t,v

def criar_visao(tab):
	v = tab.copy()
	v = np.where(v == LIMPO,DUVIDA,v)
	
	return v
	

def criar_caminho(tab, pLO=0.25, pN = 0.25):
	#pLO eh a probabilidade de ir para LESTE ou OESTE
	#pN eh a probabilidade de ir para NORTE
	N = tab.shape[0]
	M = tab.shape[1]
	#As coordenadas sao invertidas em x e y
	x = 2 #Linha NORTE SUL
	y = random.randint(1,M-2) #Coluna LESTE OESTE
	tab[x,y] = CAM
	x+=1
	tab[x,y] = CAM
	while(tab[x,y] != FIM):
		
		#prioriza a direcao SUL
		if (random.random() > pLO):
			#Tenta seguir ao SUL
			if (tab[x+1,y] == LIMPO):
				x=x+1
				tab[x,y] = CAM
			elif (tab[x+1,y] == FIM):
				x=x+1
				
		else:
		#Direcao LESTE ou OESTE 
			if (random.randint(0,1) == 0):
				#LESTE
				d = 1
			else:
				d = -1
			
			if (tab[x,y+d] == LIMPO):
				y+=d
				tab[x,y] = CAM
			elif (tab[x,y-d] == LIMPO):
				y-=d
				tab[x,y] = CAM
			
			'''
			#Direcao NORTE apenas apos LESTE ou OESTE
			if (random.random() < pN and x > 2):
				#Tenta seguir ao NORTE depois LESTE ou OESTE
				if (tab[x-1,y] == LIMPO):
					x=x-1
					tab[x,y] = CAM
			''' 

def minar(tab, prob = 1):
	#Coloca as minas no tabuleiro.
	if (prob < 1):
		for i in range(2,tab.shape[0]-1):
			for j in range(1,tab.shape[1]-1):
				if (tab[i,j] == CAM):
					tab[i,j] = LIMPO
				elif (tab[i,j] == LIMPO and random.random() < prob):
					tab[i,j] = BOMBA
	else:
		for i in range(2,tab.shape[0]-1):
			for j in range(1,tab.shape[1]-1):
				if (tab[i,j] == CAM):
					tab[i,j] = LIMPO
				elif (tab[i,j] == LIMPO):
					tab[i,j] = BOMBA

def inicializar_tab(N,M,*,probMina = 1, pLO=0.25, pN = 0.25):
	#Basicamente, cria o tabuleiro, ajusta o caminho e as minas
	#Retorna o tabuleiro e sua visao
	random.seed()
	
	tt,vv = criar_tab(N,M)
	criar_caminho(tt,pLO,pN)
	minar(tt,probMina)
	
	return tt,vv

def testar_posicao(tab,x,y):
	#Conta a quantidade de minas ao redor da posição (x,y)
	if (x < 1 or x > tab.shape[0] - 3):
		return PAREDE
	if (y < 1 or y > tab.shape[1] - 2):
		return PAREDE
	
	s = 0
	for dx in range(-1,2):
		for dy in range(-1,2):
			if (dx != 0 or dy != 0):
				if (tab[x+dx,y+dy] > 0): s+=tab[x+dx,y+dy]
	return s

def atualizar_visao(tab,visao,x,y):
	'''
	Conta a quantidade de minas ao redor da posição (x,y) da tabela
	atualiza a visao da tabela
	Retorna True se a visao foi atualizada
	'''
	
	'''
	if (x < 0 or y < 0 or x >= tab.shape[0] or y >= tab.shape[1]):
		#Nao atualiza
		#destino eh para fora
		return False
	'''
	
	if (visao[x,y] == DUVIDA):  
		r = testar_posicao(tab,x,y)
		if (r >= 0):
			visao[x,y] = r
			return True
	else:
		return False

def mover_para(tab,visao,x,y):
	'''
	Realiza um movimento para a posicao x,y
	Atualiza a visão dos vizinhos
	Atualiza a visao da posicao atual
	Retorna o resultado da operacao e um código de operacao
	'''
	if (x < 0 or y < 0 or x >= tab.shape[0] or y >= tab.shape[1]):
		#Nao realiza o movimento
		#destino eh para fora
		return False,FORA
	
	if (tab[x,y]==PAREDE):
		#Nao realiza o movimento
		#destino eh uma parede
		return False,PAREDE
		
	if (tab[x,y]==FIM):
		#Realiza o movimento
		#Destino eh uma posicao final
		return True,FIM
	
	if (tab[x,y]==BOMBA):
		#Realiza o movimento
		#Destino eh uma bomba
		visao[x,y]=FALHA
		return True,BOMBA
	
	if (tab[x,y]==LIMPO):
		#Realiza o movimento
		#Destino eh limpo
		atualizar_visao(tab,visao,x,y)
		return True,LIMPO
		
	return False,PAREDE

def dep_imprimir_visao(tab,visao,x,y):
	'''
	Mostra a visao do jogador com o jogador posicionado nas coordenadas x,y
	Sem usar cores.
	Depreciado.
	'''
	for i in range(tab.shape[0]):
		linha = ''
		for j in range(tab.shape[1]):
			linha+=' '
			if (x == i and y == j):
				#posicao do jogador
				if (tab[x,y] == BOMBA):
					linha+='X'
				else:
					linha+='T'
			else:
				if (tab[i,j] == PAREDE):
					linha+='#'
				elif (tab[i,j] == FIM):
					linha+='-'
				elif (visao[i,j] == DUVIDA):
					linha+='.'
				elif (visao[i,j] == FALHA):
					linha+='x'
				else:
					linha+=str(visao[i,j])
			
			linha+=' '
		
		print(linha)        
	
	return

def revelar_tabela(tab,visao,x,y):
	'''
	Mostra a tabela com o jogador posicionado nas coordenadas x,y
	Mostra todas as bombas.
	Usado no final do jogo.
	'''
	for i in range(tab.shape[0]):
		for j in range(tab.shape[1]):
			if (x == i and y == j):
				#posicao do jogador
				if (tab[x,y] == BOMBA):
					cprint(' X ','red','on_magenta', end=' ')
				else:
					if (tab[i,j] == PAREDE):
						cprint(' T ','white','on_green', end=' ')
					elif (tab[i,j] == FIM):
						cprint(' T ','cyan','on_green', end=' ')
					else:
						cprint(' '+str(visao[i,j])+' ','blue','on_cyan',end=' ')
			else:
				if (tab[i,j] == PAREDE):
					cprint('###','white','on_red', end=' ')
				elif (tab[i,j] == FIM):
					cprint('---','cyan','on_green', end=' ')
				elif (tab[i,j] == LIMPO):
					cprint('...','cyan','on_white', end=' ')
				elif (tab[i,j] == BOMBA):
					cprint(' x ','red','on_white', end=' ')
				else:
					cprint(' '+str(visao[i,j])+' ','blue','on_white', end=' ')
			
		
		print('')       
	
	return

def imprimir_visao(tab,visao,x,y):
	'''
	Mostra a visao do jogador com o jogador posicionado nas coordenadas x,y
	'''
	for i in range(tab.shape[0]):
		for j in range(tab.shape[1]):
			if (x == i and y == j):
				#posicao do jogador
				if (tab[x,y] == BOMBA):
					cprint(' X ','red','on_magenta', end=' ')
				else:
					if (tab[i,j] == PAREDE):
						cprint(' T ','white','on_green', end=' ')
					elif (tab[i,j] == FIM):
						cprint(' T ','cyan','on_green', end=' ')
					else:
						cprint(' '+str(visao[i,j])+' ','blue','on_cyan',end=' ')
			else:
				if (tab[i,j] == PAREDE):
					cprint('###','white','on_red', end=' ')
				elif (tab[i,j] == FIM):
					cprint('---','cyan','on_green', end=' ')
				elif (visao[i,j] == DUVIDA):
					cprint('...','cyan','on_white', end=' ')
				elif (visao[i,j] == FALHA):
					cprint(' x ','red','on_white', end=' ')
				else:
					cprint(' '+str(visao[i,j])+' ','blue','on_white', end=' ')
			
		
		print('')       
	
	return

def completar_visao(tab):
	'''
	Completa a visao do jogo, revelando todas localizacoes da tabela
	'''
	v = tab.copy()
	for i in range(tab.shape[0]):
		for j in range(tab.shape[1]):
			if (tab[i,j] == LIMPO):
				v[i,j] = testar_posicao(tab,i,j)
			elif (tab[i,j] == BOMBA):
				v[i,j] = FALHA
	
	return v

'''
t1,v1 = criar_tab(10,6)
t2,v2 = inicializar_tab(8,4, probMina = 0.6)


print("Vazio 10 x 8","\n",t1)
criar_caminho(t1,0.5)
print("Caminho 10 x 8","\n",t1)
minar(t1,0.8)
print("Minado 10 x 8","\n",t1)
print("Visao 10 x 8","\n",v1)


print("Minado 8 x 4","\n",t2)
#print("Visao 8 x 4","\n",v2)
#print("Teste [2,2]", atualizar_posicao(t2,v2,2,2))
#print("Visao 8 x 4","\n",v2)
for i in range(0,t2.shape[0]):
	for j in range(0,t2.shape[1]):
		atualizar_visao(t2,v2,i,j)

print("Vizinhanca 8 x 4","\n",v2)
'''
