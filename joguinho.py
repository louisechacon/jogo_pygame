import pygame
from pygame.locals import *
import random
import sys

pygame.init()

pygame.mixer.init()
pygame.mixer.music.load("sons/bright_stars.ogg")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)
som_ligado = True

tempo = 0
recordes = [None, None, None]

clock = pygame.time.Clock()

altura_tela = 700
largura_tela = 400
x_inicial_carta = 30
y_inicial_carta = 160
tamanho_carta = 100
espaco = 20

altura_botao = 60
largura_botao = 220
x_inicial_botao = 90
botao_facil = pygame.Rect(x_inicial_botao, 315, largura_botao, altura_botao)
botao_medio = pygame.Rect(x_inicial_botao, 395, largura_botao, altura_botao)
botao_dificil = pygame.Rect(x_inicial_botao, 475, largura_botao, altura_botao)

tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Cat's Memory")

pygame.font.init()
fonte_nivel = pygame.font.SysFont(None, 60)
fonte_botao = pygame.font.SysFont(None, 40)
fonte_titulo = pygame.font.SysFont(None, 56)
fonte_cronometro = pygame.font.SysFont(None, 30)
fonte_bom = pygame.font.SysFont(None, 60)
fonte_novamente = pygame.font.SysFont(None, 30)
fonte_recordes = pygame.font.SysFont(None, 30)
fonte_pontuacoes = pygame.font.SysFont(None, 40)

imagens_gatinhos = []

for i in range(1, 9):
    img = pygame.image.load(f'imagens/gatinho{i}.png').convert_alpha()
    imagens_gatinhos.append(img)

logo_img = pygame.image.load("imagens/logo.png").convert_alpha()
logo_img = pygame.transform.smoothscale(logo_img, (230, 230))
logo_rect = logo_img.get_rect(center=(largura_tela // 2, 170))

recordes_img = pygame.image.load("imagens/recordes.png").convert_alpha()
recordes_img = pygame.transform.smoothscale(recordes_img, (250, 250))
recordes_rect = recordes_img.get_rect(center=(largura_tela // 2, 350))

medalha_img = pygame.image.load("imagens/medalha.png").convert_alpha()
medalha_img = pygame.transform.scale(medalha_img, (52, 52))
medalha_rect = medalha_img.get_rect(topleft=(8, 213))

bg_menu = pygame.image.load("imagens/fundomenu.png").convert_alpha()
bg_menu = pygame.transform.scale(bg_menu, (largura_tela, altura_tela))

bg_final = pygame.image.load("imagens/fundofinal.png").convert_alpha()
bg_final = pygame.transform.scale(bg_final, (largura_tela, altura_tela))

bg_recordes = pygame.image.load("imagens/fundorecordes.png").convert_alpha()
bg_recordes = pygame.transform.scale(bg_recordes, (largura_tela, altura_tela))


som_on_img = pygame.image.load("imagens/som_ligado.png").convert_alpha()
som_on_img = pygame.transform.scale(som_on_img, (50, 50))
som_off_img = pygame.image.load("imagens/som_desligado.png").convert_alpha()
som_off_img = pygame.transform.scale(som_off_img, (50, 50))
som_rect_menu = som_on_img.get_rect(topleft=(12, 270))
som_rect_jogo = som_on_img.get_rect(topright=(380, 7))

tela_menu = 0
tela_jogo = 1
tela_final = 2
tela_recordes = 3
estado_tela = tela_menu

nivel = 1
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

def desenhar_botao_voltar(cor):
    botao_voltar = pygame.Rect(6, 8, 130, 40)
    pygame.draw.rect(tela, (cor), botao_voltar, border_radius=8)

    texto_voltar = fonte_botao.render("Voltar", True, (255, 255, 255))
    tela.blit(texto_voltar, texto_voltar.get_rect(center=botao_voltar.center))

    return botao_voltar

def botao_novamente():
    botao_reiniciar = pygame.Rect(100, 580, 200, 60)
    pygame.draw.rect(tela, (131, 40, 101), botao_reiniciar, border_radius = 8)

    texto = fonte_novamente.render("Jogar novamente", True, (255, 255, 255))
    tela.blit(texto, texto.get_rect(center = botao_reiniciar.center))

    return botao_reiniciar

def desenhar_menu():
    tela.blit(bg_menu, (0, 0))

    pygame.draw.rect(tela, (218, 232, 244), botao_facil, border_radius = 8)
    pygame.draw.rect(tela, (159, 210, 255), botao_medio, border_radius= 8)
    pygame.draw.rect(tela, (91, 155, 213),  botao_dificil, border_radius= 8)

    texto_facil = fonte_botao.render("Fácil", True, (120, 40, 90))
    texto_medio = fonte_botao.render("Médio", True, (120, 40, 90))
    texto_dificil = fonte_botao.render("Difícil", True, (120, 40, 90))

    tela.blit(logo_img, logo_rect)

    tela.blit(texto_facil, texto_facil.get_rect(center = botao_facil.center))
    tela.blit(texto_medio, texto_medio.get_rect(center = botao_medio.center))
    tela.blit(texto_dificil, texto_dificil.get_rect(center = botao_dificil.center))

    tela.blit(medalha_img, medalha_rect)

def desenhar_botao_som(rect):
    if som_ligado:
        tela.blit(som_on_img, rect)
    else:
        tela.blit(som_off_img, rect)

def desenhar_final():
    tela.blit(bg_final, (0, 0))

    texto_bom = fonte_bom.render("Muito bom!", True, (131, 40, 101))
    tela.blit(texto_bom, texto_bom.get_rect(center=(largura_tela // 2, 110)))

    patinha = pygame.image.load("imagens/patinha.png").convert_alpha()
    patinha = pygame.transform.scale(patinha, (400, 400))
    rect_patinha = patinha.get_rect(center=(largura_tela // 2, 350))
    tela.blit(patinha, rect_patinha)

def desenhar_recordes():
    tela.blit(bg_recordes, (0, 0))

    texto_pontuacoes = fonte_pontuacoes.render("Pontuações máximas", True, (159, 210, 255))
    tela.blit(texto_pontuacoes, texto_pontuacoes.get_rect(center=(largura_tela // 2, 150)))

    tela.blit(recordes_img, recordes_rect)

    facil = fonte_recordes.render(
        f"{formatar_tempo(recordes[0])}", True, (0, 0, 0))

    medio = fonte_recordes.render(
        f"{formatar_tempo(recordes[1])}", True, (0, 0, 0))

    dificil = fonte_recordes.render(
        f"{formatar_tempo(recordes[2])}", True, (0, 0, 0))

    x_tempo = recordes_rect.centerx - 13
    y_facil = recordes_rect.top + 40
    y_medio = recordes_rect.top + 135
    y_dificil = recordes_rect.top + 225

    tela.blit(facil, facil.get_rect(center=(x_tempo, y_facil)))
    tela.blit(medio, medio.get_rect(center=(x_tempo, y_medio)))
    tela.blit(dificil, dificil.get_rect(center=(x_tempo, y_dificil)))

def formatar_tempo(tempo_total_em_mili):
    if tempo_total_em_mili is None:
        return "--:--:---"
    
    tempo_em_segundos = tempo_total_em_mili // 1000
    resto_em_mili = tempo_total_em_mili % 1000

    minutos = tempo_em_segundos // 60
    resto_em_seg = tempo_em_segundos % 60

    return f"{minutos:02d}:{resto_em_seg:02d}:{resto_em_mili:03d}"

def salvar_recordes():
    global recordes
    with open("recordes.csv", "w") as arquivo:
        arquivo.write(",".join(map(str, recordes)))
    
def converter_texto_para_recorde(texto):
    try:
        return int(texto)
    except ValueError:
        return None

def carregar_recordes():
    global recordes
    try:
        with open("recordes.csv", "r") as arquivo:
            linha = arquivo.readline()
            recordes = list(map(converter_texto_para_recorde, linha.split(",")))
            if len(recordes) < 3:
                recordes = [None, None, None]
    except FileNotFoundError:
        pass

carregar_recordes()

while True:
    tempo = pygame.time.get_ticks()
    pos_mouse = pygame.mouse.get_pos()
    
    for event in pygame.event.get():

        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == MOUSEBUTTONDOWN:
            if estado_tela == tela_menu and som_rect_menu.collidepoint(event.pos):
                som_ligado = not som_ligado

            elif estado_tela == tela_jogo and som_rect_jogo.collidepoint(event.pos):
                som_ligado = not som_ligado

            if som_ligado:
                pygame.mixer.music.unpause()
            else:
                pygame.mixer.music.pause()

        if estado_tela == tela_menu and event.type == MOUSEBUTTONDOWN:
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
                estado_tela = tela_jogo

            elif medalha_rect.collidepoint(event.pos):
                estado_tela = tela_recordes

        elif estado_tela == tela_jogo and event.type == MOUSEBUTTONDOWN:

            desenhar_botao_voltar((218, 232, 244))

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
        
        elif estado_tela == tela_final and event.type == MOUSEBUTTONDOWN:
            if botao_reiniciar.collidepoint(event.pos):
                estado_tela = tela_menu

        elif estado_tela == tela_recordes and event.type == MOUSEBUTTONDOWN:
            if botao_voltar.collidepoint(event.pos):
                estado_tela = tela_menu
    
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
                    salvar_recordes()

                estado_tela = tela_final

        else:
            cartas_viradas[cartas_escolhidas[0]] = False
            cartas_viradas[cartas_escolhidas[1]] = False
        
        cartas_escolhidas = []

    if estado_tela == tela_menu:
        desenhar_menu()
        desenhar_botao_som(som_rect_menu)

    elif estado_tela == tela_jogo:

        tela.fill((218, 232, 244))
        texto_superficie = fonte_nivel.render(texto_nivel, True, (226, 139, 197))
        tela.blit(texto_superficie, texto_superficie.get_rect(center=(largura_tela // 2, 100)))

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

        desenhar_botao_som(som_rect_jogo)

    elif estado_tela == tela_final:
        desenhar_final()
        botao_reiniciar = botao_novamente()

    elif estado_tela == tela_recordes:
        desenhar_recordes()
        botao_voltar = desenhar_botao_voltar((159, 210, 255))

    pygame.display.update()
    clock.tick(60)