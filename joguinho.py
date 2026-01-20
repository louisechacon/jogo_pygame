import pygame
from pygame.locals import *
import random
import sys

pygame.init()

altura_botao = 220
largura_botao = 60
x_inicial_botao = 80
botao_facil   = pygame.Rect(x_inicial_botao, 270, altura_botao, largura_botao)
botao_medio   = pygame.Rect(x_inicial_botao, 350, altura_botao, largura_botao)
botao_dificil = pygame.Rect(x_inicial_botao, 430, altura_botao, largura_botao)

altura = 650
largura = 390
x_inicial_carta = 25
y_inicial_carta = 210
tamanho_carta = 100
espaco = 20

tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Cat's Memory")

clock = pygame.time.Clock()

pygame.font.init()
fonte_nivel = pygame.font.SysFont(None, 50)
fonte_botao = pygame.font.SysFont(None, 40)
fonte_titulo = pygame.font.SysFont(None, 56)

tamanho_carta = 100
imagens_gatinhos = []

for i in range(1, 9):
    img = pygame.image.load(f'imagens/gatinho{i}.png').convert_alpha()
    img = pygame.transform.scale(img, (tamanho_carta, tamanho_carta))
    imagens_gatinhos.append(img)


tela_menu = 0
tela_jogo = 1
estado_tela = tela_menu


def escolher_nivel(nivel):
    if nivel == 1:
        return 2, 3, "Nível 1"
    elif nivel == 2:
        return 4, 3, "Nível 2"
    elif nivel == 3:
        return 4, 4, "Nível 3"


nivel = 1
linhas = 0
colunas = 0
lista_ids = []
texto_nivel = ""
timer_espera = 0
cartas_viradas = []
cartas_escolhidas = []


def iniciar_jogo(nivel):

    linhas, colunas, texto_nivel = escolher_nivel(nivel)
    num_cartas = linhas * colunas

    lista_ids = list(range(num_cartas // 2)) * 2
    random.shuffle(lista_ids)

    cartas_viradas = [False] * num_cartas
    cartas_escolhidas = [] 

    return linhas, colunas, texto_nivel, lista_ids, cartas_viradas, cartas_escolhidas


def desenhar_menu():
    tela.fill((226, 139, 197))

    titulo = fonte_titulo.render("Cat's Memory", True, (201, 226, 249))
    tela.blit(titulo, titulo.get_rect(center=(largura // 2, 180)))

    pygame.draw.rect(tela, (218, 232, 244), botao_facil, border_radius = 8)
    pygame.draw.rect(tela, (159,210,255), botao_medio, border_radius= 8)
    pygame.draw.rect(tela, (91, 155, 213),  botao_dificil, border_radius= 8)

    texto_facil = fonte_botao.render("Fácil", True, (120, 40, 90))
    texto_medio = fonte_botao.render("Médio", True, (120, 40, 90))
    texto_dificil = fonte_botao.render("Difícil", True, (120, 40, 90))

    tela.blit(texto_facil, texto_facil.get_rect(center = botao_facil.center))
    tela.blit(texto_medio, texto_medio.get_rect(center = botao_medio.center))
    tela.blit(texto_dificil, texto_dificil.get_rect(center = botao_dificil.center))


while True:
    tempo = pygame.time.get_ticks()
    pos_mouse = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
            sys.exit()

        if estado_tela == tela_menu and event.type == MOUSEBUTTONDOWN:
            if botao_facil.collidepoint(event.pos):
                nivel = 1
            elif botao_medio.collidepoint(event.pos):
                nivel = 2
            elif botao_dificil.collidepoint(event.pos):
                nivel = 3
            else:
                continue
            
            linhas, colunas, texto_nivel, lista_ids, cartas_viradas, cartas_escolhidas = iniciar_jogo(nivel)
            estado_tela = tela_jogo


        elif estado_tela == tela_jogo and event.type == MOUSEBUTTONDOWN:
            if len(cartas_escolhidas) < 2:
                for i in range(len(lista_ids)):
                    col = i % colunas
                    lin = i // colunas
                    x = x_inicial_carta + col * (tamanho_carta + espaco)
                    y = y_inicial_carta + lin * (tamanho_carta + espaco)
                
                    rect = pygame.Rect(x, y, tamanho_carta, tamanho_carta)

                    if rect.collidepoint(event.pos) and not cartas_viradas[i]:
                        cartas_viradas[i] = True
                        cartas_escolhidas.append(i)

                        if len(cartas_escolhidas) == 2:
                            id1 = lista_ids[cartas_escolhidas[0]]
                            id2 = lista_ids[cartas_escolhidas[1]]

                            if id1 != id2:
                                timer_espera = tempo + 1000
                            else:
                                cartas_escolhidas = []
    
    if len(cartas_escolhidas) == 2 and tempo > timer_espera:
        for i in cartas_escolhidas:
            cartas_viradas[i] = False
        cartas_escolhidas = []

    if estado_tela == tela_menu:
            desenhar_menu()

    elif estado_tela == tela_jogo:
        tela.fill((218, 232, 244))
        texto_superficie = fonte_nivel.render(texto_nivel, True, (226, 139, 197))
        tela.blit(texto_superficie, (120, 120))

    for i in range(len(lista_ids)):
        col = i % colunas
        lin = i // colunas
        x = x_inicial_carta + col * (tamanho_carta + espaco)
        y = y_inicial_carta + lin * (tamanho_carta + espaco)

        if cartas_viradas[i]:
            id_gatinho = lista_ids[i]
            tela.blit(imagens_gatinhos[id_gatinho], (x, y))
        else:
            pygame.draw.rect(tela, (226, 139, 197), (x, y, tamanho_carta, tamanho_carta), border_radius=8)

    pygame.display.update()