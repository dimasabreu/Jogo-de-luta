import pygame

pygame.init()

# criando a janela do jogo
SCREEN_WIDHT = 1280
SCREEN_HEIGHT = 720

screen = pygame.display.set_mode((SCREEN_WIDHT, SCREEN_HEIGHT))
pygame.display.set_caption("Hills Fight")

# carregando o background
bg_image = pygame.image.load("../assets/images/background/background.jpg").convert_alpha()

# func para colocar o bg na tela


def draw_bg():
    # modificando o tamanho da imagem
    scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDHT, SCREEN_HEIGHT))
    # colocando a imagem na tela e a posicao que ela vai aparecer
    screen.blit(scaled_bg, (0, 0))


# loop do jogo
run = True
while run:
    # colocando o bg na tela
    draw_bg()

    # comando de evento
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # atualizando a tela
    pygame.display.update()
# fechando o pygame
pygame.quit()
