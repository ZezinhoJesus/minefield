#Utilitarios
import board
import numpy as np

def criar_sensor(visao,x,y,d):
	'''
	Analisa a visao do tabuleiro e retorna um conjunto de sensores
	O centro eh a posicao [x,y]. 
	
	Retorna um array 1d com tamanho (2*d + 1)^2 contendo a visao de
	cada posicao ao redor da coordenada [x,y] da esquerda para direita,
	de cima para baixo
	'''
	tam = (2*d + 1)**2
	sensor = np.full(tam, board.PAREDE, dtype=np.int8)
	
	z = 0
	for i in range(-d,d+1):
		for j in range(-d,d+1):
			if ( (x + i >= 0) and (x + i < visao.shape[0]) ):
				if ( (y + j >= 0) and (y + j < visao.shape[1]) ):
					sensor[z] = visao[x+i,y+j]
			z+=1
			

	return sensor

def ver_sensor(sensor,d):
	'''
	Exibe a visao do sensor com centro em [d,d]
	'''
	print(np.reshape(sensor,(2*d + 1, 2*d + 1)))
