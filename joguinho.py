import pygame
from pygame.locals import *
import random

pygame.init()

# - CARACTERÍSTICAS

altura = 650
largura = 390
x_inicial = 25
y_inicial = 210
tamanho_carta = 100
espaco = 20

tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Memória dos Gatinhos")
fonte = pygame.font.SysFont(None, 50)

# - IMAGENS

imagens_gatinhos = []
for i in range(1, 9):
    img = pygame.image.load(f'gatinho{i}.png').convert_alpha()
    img = pygame.transform.scale(img, (tamanho_carta, tamanho_carta))
    imagens_gatinhos.append(img)


# - NÍVEL 

def escolher_nivel(nivel):
    if nivel == 1: return 2, 3, "Nível 1"
    elif nivel == 2: return 4, 3, "Nível 2"
    elif nivel == 3: return 4, 4, "Nível 3"

# - LÓGICA 

nivel = 1
linhas, colunas, texto_nivel = escolher_nivel(nivel)
num_cartas = linhas * colunas
lista_ids = list(range(num_cartas // 2)) * 2
random.shuffle(lista_ids)

cartas_viradas = [False] * num_cartas
cartas_escolhidas = [] 
timer_espera = 0 

while True:
    tela.fill((218, 232, 244))
    tempo = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        
        if event.type == MOUSEBUTTONDOWN and len(cartas_escolhidas) < 2:
            pos_mouse = pygame.mouse.get_pos()
            

            for i in range(num_cartas):
                col = i % colunas
                lin = i // colunas
                x = x_inicial + col * (tamanho_carta + espaco)
                y = y_inicial + lin * (tamanho_carta + espaco)
                
                retangulo_carta = pygame.Rect(x, y, tamanho_carta, tamanho_carta)
                
                if retangulo_carta.collidepoint(pos_mouse) and not cartas_viradas[i]:
                    cartas_viradas[i] = True
                    cartas_escolhidas.append(i)
                    

                    if len(cartas_escolhidas) == 2:
                        id1 = lista_ids[cartas_escolhidas[0]]
                        id2 = lista_ids[cartas_escolhidas[1]]
                        
                        if id1 == id2: 
                            cartas_escolhidas = []
                        else: 
                            timer_espera = tempo + 1000 


    if len(cartas_escolhidas) == 2 and tempo > timer_espera:
        cartas_viradas[cartas_escolhidas[0]] = False
        cartas_viradas[cartas_escolhidas[1]] = False
        cartas_escolhidas = []

    texto_superficie = fonte.render(texto_nivel, True, (226, 139, 197))
    tela.blit(texto_superficie, (120, 120))

    for i in range(num_cartas):
        col = i % colunas
        lin = i // colunas
        x = x_inicial + col * (tamanho_carta + espaco)
        y = y_inicial + lin * (tamanho_carta + espaco)

        if cartas_viradas[i]:
            id_gatinho = lista_ids[i]
            tela.blit(imagens_gatinhos[id_gatinho], (x, y))
        else:
            pygame.draw.rect(tela, (226, 139, 197), (x, y, tamanho_carta, tamanho_carta), border_radius=8)

    pygame.display.update()