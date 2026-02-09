import pygame
from pygame.locals import *
import random
import sys
import config
import dados
import recursos
import interface

pygame.init()

pygame.mixer.init()
pygame.mixer.music.load("sons/bright_stars.ogg")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)
som_ligado = True

tempo = 0
recordes = dados.carregar_recordes()

clock = pygame.time.Clock()

botao_facil = pygame.Rect(config.X_INICIAL_BOTAO, 315, config.LARGURA_BOTAO, config.ALTURA_BOTAO)
botao_medio = pygame.Rect(config.X_INICIAL_BOTAO, 395, config.LARGURA_BOTAO, config.ALTURA_BOTAO)
botao_dificil = pygame.Rect(config.X_INICIAL_BOTAO, 475, config.LARGURA_BOTAO, config.ALTURA_BOTAO)

tela = pygame.display.set_mode((config.LARGURA_TELA, config.ALTURA_TELA))
pygame.display.set_caption("Cat's Memory")

recursos.carregar_sons()
pygame.mixer.music.play(-1)

dicionario_imagens = recursos.carregar_imagens()
dicionario_fontes = recursos.carregar_fontes()

botao_facil = pygame.Rect(config.X_INICIAL_BOTAO, 315, config.LARGURA_BOTAO, config.ALTURA_BOTAO)
botao_medio = pygame.Rect(config.X_INICIAL_BOTAO, 395, config.LARGURA_BOTAO, config.ALTURA_BOTAO)
botao_dificil = pygame.Rect(config.X_INICIAL_BOTAO, 475, config.LARGURA_BOTAO, config.ALTURA_BOTAO)

som_rect_menu = dicionario_imagens['som_on'].get_rect(topleft=(12, 270))
som_rect_jogo = dicionario_imagens['som_on'].get_rect(topright=(380, 7))
medalha_rect = dicionario_imagens['medalha'].get_rect(topleft=(8, 213))

pygame.font.init()
fonte_nivel = pygame.font.SysFont(None, 60)
fonte_botao = pygame.font.SysFont(None, 40)
fonte_titulo = pygame.font.SysFont(None, 56)
fonte_cronometro = pygame.font.SysFont(None, 30)
fonte_bom = pygame.font.SysFont(None, 60)
fonte_novamente = pygame.font.SysFont(None, 30)
fonte_recordes = pygame.font.SysFont(None, 30)
fonte_pontuacoes = pygame.font.SysFont(None, 40)

estado_tela = config.TELA_MENU

nivel = 1
linhas = 0
colunas = 0
lista_ids = []
texto_nivel = ""
timer_espera = 0
cartas_viradas = []
cartas_escolhidas = []
cartas_resolvidas = []
tamanho_carta = 100

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


while True:
    tempo = pygame.time.get_ticks()
    pos_mouse = pygame.mouse.get_pos()
    
    for event in pygame.event.get():

        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == MOUSEBUTTONDOWN:
            if estado_tela == config.TELA_MENU and som_rect_menu.collidepoint(event.pos):
                som_ligado = not som_ligado

            elif estado_tela == config.TELA_JOGO and som_rect_jogo.collidepoint(event.pos):
                som_ligado = not som_ligado

            if som_ligado:
                pygame.mixer.music.unpause()
            else:
                pygame.mixer.music.pause()

        if estado_tela == config.TELA_MENU and event.type == MOUSEBUTTONDOWN:
            if (botao_facil.collidepoint(event.pos) or
            botao_medio.collidepoint(event.pos) or
            botao_dificil.collidepoint(event.pos)):

                if botao_facil.collidepoint(event.pos):
                    nivel = 1
                elif botao_medio.collidepoint(event.pos):
                    nivel = 2
                else:
                    nivel = 3

                linhas, colunas, texto_nivel, lista_ids, cartas_viradas, cartas_escolhidas = iniciar_jogo(nivel)
                tempo_inicio = pygame.time.get_ticks()
                estado_tela = config.TELA_JOGO

            elif medalha_rect.collidepoint(event.pos):
                estado_tela = config.TELA_RECORDES

        elif estado_tela == config.TELA_JOGO and event.type == MOUSEBUTTONDOWN:
            if botao_voltar.collidepoint(event.pos):
                estado_tela = config.TELA_MENU

            if len(cartas_escolhidas) < 2 and tempo > timer_espera:
                for i in range(len(lista_ids)):

                    if cartas_resolvidas[i]: continue 

                    col = i % colunas
                    lin = i // colunas
                    x = config.X_INICIAL_CARTA + col * (tamanho_carta + config.ESPACO_CARTAS)
                    y = config.Y_INICIAL_CARTA + lin * (tamanho_carta + config.ESPACO_CARTAS)

                    rect = pygame.Rect(x, y, tamanho_carta, tamanho_carta)

                    if rect.collidepoint(event.pos) and not cartas_viradas[i]:
                        cartas_viradas[i] = True
                        cartas_escolhidas.append(i)

                        if len(cartas_escolhidas) == 2:
                            timer_espera = tempo + 1000
        
        elif estado_tela == config.TELA_FINAL and event.type == MOUSEBUTTONDOWN:
            if botao_reiniciar.collidepoint(event.pos):
                estado_tela = config.TELA_MENU

        elif estado_tela == config.TELA_RECORDES and event.type == MOUSEBUTTONDOWN:
            if botao_voltar.collidepoint(event.pos):
                estado_tela = config.TELA_MENU
    
    if len(cartas_escolhidas) == 2 and tempo > timer_espera:
        id1 = lista_ids[cartas_escolhidas[0]]
        id2 = lista_ids[cartas_escolhidas[1]]

        if id1 == id2:
            cartas_resolvidas[cartas_escolhidas[0]] = True
            cartas_resolvidas[cartas_escolhidas[1]] = True

            if all(cartas_resolvidas):
                tempo_fim = pygame.time.get_ticks()
                tempo_total = (tempo_fim - tempo_inicio)

                if recordes[nivel - 1] is None or tempo_total < recordes[nivel-1]:
                    recordes[nivel-1] = tempo_total
                    dados.salvar_recordes(recordes)

                estado_tela = config.TELA_FINAL

        else:
            cartas_viradas[cartas_escolhidas[0]] = False
            cartas_viradas[cartas_escolhidas[1]] = False
        
        cartas_escolhidas = []

    if estado_tela == config.TELA_MENU:
        interface.desenhar_menu(tela, dicionario_imagens, dicionario_fontes, (botao_facil, botao_medio, botao_dificil))
        interface.desenhar_botao_som(tela, dicionario_imagens, som_rect_menu, som_ligado)

    elif estado_tela == config.TELA_JOGO:
        tela.fill((218, 232, 244))
        botao_voltar = interface.desenhar_botao_voltar(tela, dicionario_fontes, (159, 210, 255))
        interface.desenhar_botao_som(tela, dicionario_imagens, som_rect_jogo, som_ligado)

        if len(cartas_escolhidas) == 2 and tempo <= timer_espera:
            tempo_restante = (timer_espera - tempo) / 1000
            tempo_visto = 1.0 - tempo_restante 
            texto_cronometro= fonte_cronometro.render(f"{tempo_visto:.1f}s", True, (120, 40, 90))
            tela.blit(texto_cronometro, texto_cronometro.get_rect(center=(config.LARGURA_TELA // 2, 640)))

        for i in range(len(lista_ids)):
            if cartas_resolvidas[i]: continue 

            col = i % colunas
            lin = i // colunas
            x = config.X_INICIAL_CARTA + col * (tamanho_carta + config.ESPACO_CARTAS)
            y = config.Y_INICIAL_CARTA + lin * (tamanho_carta + config.ESPACO_CARTAS)

            if cartas_viradas[i]:
                gatinho_redimensionado = pygame.transform.scale(dicionario_imagens['gatinhos'][lista_ids[i]], (tamanho_carta, tamanho_carta))
                tela.blit(gatinho_redimensionado, (x, y))
                
            else:
                pygame.draw.rect(tela, (226, 139, 197), (x, y, tamanho_carta, tamanho_carta), border_radius=8)

    elif estado_tela == config.TELA_FINAL:
        botao_reiniciar = interface.desenhar_final(tela, dicionario_imagens, dicionario_fontes)

    elif estado_tela == config.TELA_RECORDES:
        interface.desenhar_recordes(tela, dicionario_imagens, dicionario_fontes, recordes)
        botao_voltar = interface.desenhar_botao_voltar(tela, dicionario_fontes, (159, 210, 255))

    pygame.display.update()
    clock.tick(60)