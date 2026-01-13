import pygame
from pygame.locals import *

pygame.init()

altura = 650
largura = 390

x_inicial = 25
y_inicial = 210
tamanho_carta = 100
espaco = 20

pygame.display.set_caption("Memória dos Gatinhos")

tela = pygame.display.set_mode((largura, altura))
fonte = pygame.font.SysFont(None, 50)
nivel = 1

def escolher_nivel(nivel):
    if nivel == 1:
        return 2, 3, "Nível 1"
    elif nivel == 2:
        return 4, 3, "Nível 2"
    elif nivel == 3:
        return 4, 4, "Nível 3"

while True:
    tela.fill((218, 232, 244))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

    linhas, colunas, texto_nivel = escolher_nivel(nivel)

    texto_superficie = fonte.render(texto_nivel, True, (226, 139, 197))
    tela.blit(texto_superficie, (260, 120))

    for linha in range(linhas):
        for coluna in range(colunas):
            x = x_inicial + coluna * (tamanho_carta + espaco)
            y = y_inicial + linha * (tamanho_carta + espaco)

            pygame.draw.rect(tela,(226, 139, 197),(x, y, tamanho_carta, tamanho_carta), border_radius=8)

    pygame.display.update()