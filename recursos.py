import pygame
import os
import config

def carregar_imagens():
    imagens = {}
    
    lista_gatinhos = []
    for i in range(1, 9):
        caminho = os.path.join('imagens', f'gatinho{i}.png')
        img = pygame.image.load(caminho).convert_alpha()
        lista_gatinhos.append(img)
    imagens['gatinhos'] = lista_gatinhos

    logo = pygame.image.load("imagens/logo.png").convert_alpha()
    imagens['logo'] = pygame.transform.smoothscale(logo, (230, 230))

    medalha = pygame.image.load("imagens/medalha.png").convert_alpha()
    imagens['medalha'] = pygame.transform.scale(medalha, (52, 52))

    bg_menu = pygame.image.load("imagens/fundomenu.png").convert_alpha()
    imagens['bg_menu'] = pygame.transform.scale(bg_menu, (config.LARGURA_TELA, config.ALTURA_TELA))
    bg_final = pygame.image.load("imagens/fundofinal.png").convert_alpha()
    imagens['bg_final'] = pygame.transform.scale(bg_final, (config.LARGURA_TELA, config.ALTURA_TELA))
    bg_recordes = pygame.image.load("imagens/fundorecordes.png").convert_alpha()
    imagens['bg_recordes'] = pygame.transform.scale(bg_recordes, (config.LARGURA_TELA, config.ALTURA_TELA))

    som_on = pygame.image.load("imagens/som_ligado.png").convert_alpha()
    imagens['som_on'] = pygame.transform.scale(som_on, (50, 50))
    som_off = pygame.image.load("imagens/som_desligado.png").convert_alpha()
    imagens['som_off'] = pygame.transform.scale(som_off, (50, 50))

    patinha = pygame.image.load("imagens/patinha.png").convert_alpha()
    imagens['patinha'] = pygame.transform.scale(patinha, (400, 400))
    
    img_rec = pygame.image.load("imagens/recordes.png").convert_alpha()
    imagens['recordes'] = pygame.transform.smoothscale(img_rec, (250, 250))

    return imagens

def carregar_fontes():
    pygame.font.init()
    return {
        'nivel': pygame.font.SysFont(None, 60),
        'botao': pygame.font.SysFont(None, 40),
        'titulo': pygame.font.SysFont(None, 56),
        'cronometro': pygame.font.SysFont(None, 30),
        'bom': pygame.font.SysFont(None, 60),
        'novamente': pygame.font.SysFont(None, 30),
        'recordes': pygame.font.SysFont(None, 30),
        'pontuacoes': pygame.font.SysFont(None, 40),
    }

def carregar_sons():
    pygame.mixer.init()
    pygame.mixer.music.load("sons/bright_stars.ogg")
    pygame.mixer.music.set_volume(0.5)