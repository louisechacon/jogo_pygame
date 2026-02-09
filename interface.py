import pygame
import config
import dados

def desenhar_botao_voltar(tela, fontes, cor):
    botao_voltar = pygame.Rect(6, 8, 130, 40)
    pygame.draw.rect(tela, cor, botao_voltar, border_radius=8)

    texto_voltar = fontes['botao'].render("Voltar", True, (255, 255, 255))
    tela.blit(texto_voltar, texto_voltar.get_rect(center=botao_voltar.center))

    return botao_voltar

def desenhar_botao_som(tela, imagens, rect, som_ligado):
    if som_ligado:
        tela.blit(imagens['som_on'], rect)
    else:
        tela.blit(imagens['som_off'], rect)

def desenhar_menu(tela, imagens, fontes, rects_botoes):
    tela.blit(imagens['bg_menu'], (0, 0))
    
    botao_facil, botao_medio, botao_dificil = rects_botoes

    pygame.draw.rect(tela, (218, 232, 244), botao_facil, border_radius=8)
    pygame.draw.rect(tela, (159, 210, 255), botao_medio, border_radius=8)
    pygame.draw.rect(tela, (91, 155, 213), botao_dificil, border_radius=8)

    texto_facil = fontes['botao'].render("Fácil", True, (120, 40, 90))
    texto_medio = fontes['botao'].render("Médio", True, (120, 40, 90))
    texto_dificil = fontes['botao'].render("Difícil", True, (120, 40, 90))

    rect_logo = imagens['logo'].get_rect(center=(config.LARGURA_TELA // 2, 170))
    tela.blit(imagens['logo'], rect_logo)

    tela.blit(texto_facil, texto_facil.get_rect(center=botao_facil.center))
    tela.blit(texto_medio, texto_medio.get_rect(center=botao_medio.center))
    tela.blit(texto_dificil, texto_dificil.get_rect(center=botao_dificil.center))

    tela.blit(imagens['medalha'], (8, 213))

def desenhar_final(tela, imagens, fontes):
    tela.blit(imagens['bg_final'], (0, 0))

    texto_bom = fontes['bom'].render("Muito bom!", True, (131, 40, 101))
    tela.blit(texto_bom, texto_bom.get_rect(center=(config.LARGURA_TELA // 2, 110)))

    rect_patinha = imagens['patinha'].get_rect(center=(config.LARGURA_TELA // 2, 350))
    tela.blit(imagens['patinha'], rect_patinha)

    botao_reiniciar = pygame.Rect(100, 580, 200, 60)
    pygame.draw.rect(tela, (131, 40, 101), botao_reiniciar, border_radius=8)

    texto = fontes['novamente'].render("Jogar novamente", True, (255, 255, 255))
    tela.blit(texto, texto.get_rect(center=botao_reiniciar.center))

    return botao_reiniciar

def desenhar_recordes(tela, imagens, fontes, lista_recordes):
    tela.blit(imagens['bg_recordes'], (0, 0))

    texto_pontuacoes = fontes['pontuacoes'].render("Pontuações máximas", True, (91, 155, 213))
    tela.blit(texto_pontuacoes, texto_pontuacoes.get_rect(center=(config.LARGURA_TELA // 2, 150)))

    rect_img_rec = imagens['recordes'].get_rect(center=(config.LARGURA_TELA // 2, 350))
    tela.blit(imagens['recordes'], rect_img_rec)

    facil = fontes['recordes'].render(f"{dados.formatar_tempo(lista_recordes[0])}", True, (0, 0, 0))
    medio = fontes['recordes'].render(f"{dados.formatar_tempo(lista_recordes[1])}", True, (0, 0, 0))
    dificil = fontes['recordes'].render(f"{dados.formatar_tempo(lista_recordes[2])}", True, (0, 0, 0))

    x_tempo = rect_img_rec.centerx - 13
    y_facil = rect_img_rec.top + 40
    y_medio = rect_img_rec.top + 135
    y_dificil = rect_img_rec.top + 225

    tela.blit(facil, facil.get_rect(center=(x_tempo, y_facil)))
    tela.blit(medio, medio.get_rect(center=(x_tempo, y_medio)))
    tela.blit(dificil, dificil.get_rect(center=(x_tempo, y_dificil)))