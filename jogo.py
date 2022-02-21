#Jogo
import board
import utils
#from board import inicializar_tab, testar_posicao, ver_tabela
#from board import atualizar_visao, mover_para
from pynput import keyboard
from time import sleep

campo,visao = board.inicializar_tab(10,4,probMina = 0.4, pLO=0.5)

#Posicao atual do jogador
i = 0
j = campo.shape[1] // 2
#Falhas
falhas = 0
moves = 0
d=2

fim = False

board.imprimir_visao(campo,visao,i,j)
print('Use as teclas de navegação (ou pressione s para SAIR).')

while(not fim):
	
	dx = 0
	dy = 0
	sen = utils.criar_sensor(visao,i,j,d)
	utils.ver_sensor(sen,d)	
	with keyboard.Events() as events:
		event = events.get(1e6)
		if event.key == keyboard.KeyCode.from_char('s'):
			print("Sair")
			board.revelar_tabela(campo,visao,i,j)
			fim = True
		if event.key == keyboard.Key.right:
			dx = 1
		if event.key == keyboard.Key.left:
			dx = -1
		if event.key == keyboard.Key.up:
			dy = -1
		if event.key == keyboard.Key.down:
			dy = 1
	
	if (dx != 0 or dy != 0):
		res,cod = board.mover_para(campo,visao,i+dy,j+dx)
		if (res):
			#movimento realizado
			i+=dy
			j+=dx
			moves+=1
			
			if (cod == board.FIM):
				fim = True
				print('Você venceu! Falhas = ',falhas, '. Movimentos = ',moves)
				board.revelar_tabela(campo,visao,i,j)
				break
			else:
				if (cod == board.BOMBA):
					i = 0
					j = campo.shape[1] // 2
					falhas+=1
					print('Detonado!!')
				
		board.imprimir_visao(campo,visao,i,j)
		print('Use as teclas de navegação (ou pressione s para SAIR).')
		print('Falhas = ',falhas, '. Movimentos = ',moves)
		sleep(1)
