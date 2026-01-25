import pygame
from pygame.locals import *
import random
import sys

pygame.init()

altura_tela = 700
largura_tela = 400
x_inicial_carta = 30
y_inicial_carta = 160
tamanho_carta = 100
espaco = 20

altura_botao = 60
largura_botao = 220
x_inicial_botao = 90
botao_facil = pygame.Rect(x_inicial_botao, 270, largura_botao, altura_botao)
botao_medio = pygame.Rect(x_inicial_botao, 350, largura_botao, altura_botao)
botao_dificil = pygame.Rect(x_inicial_botao, 430, largura_botao, altura_botao)

tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Cat's Memory")

clock = pygame.time.Clock()

pygame.font.init()
fonte_nivel = pygame.font.SysFont(None, 60)
fonte_botao = pygame.font.SysFont(None, 40)
fonte_titulo = pygame.font.SysFont(None, 56)
fonte_cronometro = pygame.font.SysFont(None, 30)


imagens_gatinhos = []

for i in range(1, 9):
    img = pygame.image.load(f'imagens/gatinho{i}.png').convert_alpha()
    imagens_gatinhos.append(img)

tela_menu = 0
tela_jogo = 1
estado_tela = tela_menu

linhas = 0
colunas = 0
lista_ids = []
texto_nivel = ""
timer_espera = 0
cartas_viradas = []
cartas_escolhidas = []
cartas_resolvidas = [] 

def escolher_carta(nivel):
    if nivel == 3:
        return 70
    else:
        return 100

def escolher_nivel(nivel):
    if nivel == 1:
        return 2, 3, "Nível 1"
    elif nivel == 2:
        return 4, 3, "Nível 2"
    elif nivel == 3:
        return 4, 4, "Nível 3"

def iniciar_jogo(nivel):

    global tamanho_carta, linhas, colunas, texto_nivel, lista_ids, cartas_viradas, cartas_escolhidas, cartas_resolvidas
    tamanho_carta = escolher_carta(nivel)
    linhas, colunas, texto_nivel = escolher_nivel(nivel)
    num_cartas = linhas * colunas

    lista_ids = list(range(num_cartas // 2)) * 2
    random.shuffle(lista_ids)

    cartas_viradas = [False] * num_cartas
    cartas_resolvidas = [False] * num_cartas
    cartas_escolhidas = []

    return linhas, colunas, texto_nivel, lista_ids, cartas_viradas, cartas_escolhidas

def desenhar_menu():
    tela.fill((226, 139, 197))

    titulo = fonte_titulo.render("Cat's Memory", True, (201, 226, 249))
    tela.blit(titulo, titulo.get_rect(center=(largura_tela // 2, 180)))

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
            botao_voltar = pygame.Rect(6, 8, 130, 40)
            if botao_voltar.collidepoint(event.pos):
                estado_tela = tela_menu

            if len(cartas_escolhidas) < 2 and tempo > timer_espera:
                for i in range(len(lista_ids)):

                    if cartas_resolvidas[i]: continue 

                    col = i % colunas
                    lin = i // colunas
                    x = x_inicial_carta + col * (tamanho_carta + espaco)
                    y = y_inicial_carta + lin * (tamanho_carta + espaco)

                    rect = pygame.Rect(x, y, tamanho_carta, tamanho_carta)

                    if rect.collidepoint(event.pos) and not cartas_viradas[i]:
                        cartas_viradas[i] = True
                        cartas_escolhidas.append(i)

                        if len(cartas_escolhidas) == 2:
                            timer_espera = tempo + 1000
    
    if len(cartas_escolhidas) == 2 and tempo > timer_espera:
        id1 = lista_ids[cartas_escolhidas[0]]
        id2 = lista_ids[cartas_escolhidas[1]]

        if id1 == id2:
            cartas_resolvidas[cartas_escolhidas[0]] = True
            cartas_resolvidas[cartas_escolhidas[1]] = True

        else:
            cartas_viradas[cartas_escolhidas[0]] = False
            cartas_viradas[cartas_escolhidas[1]] = False
        
        cartas_escolhidas = []


    if estado_tela == tela_menu:
        desenhar_menu()

    elif estado_tela == tela_jogo:

        tela.fill((218, 232, 244))
        texto_superficie = fonte_nivel.render(texto_nivel, True, (226, 139, 197))
        tela.blit(texto_superficie, texto_superficie.get_rect(center=(largura_tela // 2, 80)))

        botao_voltar = pygame.Rect(6, 8, 130, 40)
        pygame.draw.rect(tela, (159, 210, 255), botao_voltar, border_radius=8)
        texto_voltar = fonte_botao.render("Voltar", True, (255, 255, 255))
        tela.blit(texto_voltar, texto_voltar.get_rect(center=botao_voltar.center))

        if len(cartas_escolhidas) == 2 and tempo <= timer_espera:
            tempo_restante = (timer_espera - tempo) / 1000
            tempo_visto = 1.0 - tempo_restante 
            texto_cronometro= fonte_cronometro.render(f"{tempo_visto:.1f}s", True, (120, 40, 90))
            tela.blit(texto_cronometro, texto_cronometro.get_rect(center=(largura_tela // 2, 640)))


        for i in range(len(lista_ids)):

            if cartas_resolvidas[i]: continue 

            col = i % colunas
            lin = i // colunas
            x = x_inicial_carta + col * (tamanho_carta + espaco)
            y = y_inicial_carta + lin * (tamanho_carta + espaco)

            if cartas_viradas[i]:
                gatinho_redimensionado = pygame.transform.scale(imagens_gatinhos[lista_ids[i]], (tamanho_carta, tamanho_carta))
                tela.blit(gatinho_redimensionado, (x, y))
                
            else:
                pygame.draw.rect(tela, (226, 139, 197), (x, y, tamanho_carta, tamanho_carta), border_radius=8)

    pygame.display.update()
    clock.tick(60)