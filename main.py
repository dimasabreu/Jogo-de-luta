import pygame
from fighter import Fighter

# iniciando o loop do pygame
pygame.init()

# criando a janela do jogo
SCREEN_WIDHT = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDHT, SCREEN_HEIGHT))
pygame.display.set_caption("Hills Fight")

# setando o frame do jogo
clock = pygame.time.Clock()
FPS = 60

# definindo cores
RED = (255, 0, 0)
GREY = (140, 139, 132)
WHITE = (255, 255, 255)
GREEN = (52, 184, 0)

# carregando o background
bg_image = pygame.image.load("assets/images/background/background.jpg").convert_alpha()


# func para colocar o bg na tela
def draw_bg():
    # modificando o tamanho da imagem
    scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDHT, SCREEN_HEIGHT))
    # colocando a imagem na tela e a posicao que ela vai aparecer
    screen.blit(scaled_bg, (0, 0))

# func para criar as barras de vida
def draw_health_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x - 4, y - 3, 408, 26))
    pygame.draw.rect(screen, GREEN, (x, y, 400, 20))
    pygame.draw.rect(screen, RED, (x, y, 400 * ratio, 20))

# criando os 2 jogadores
figter_1 = Fighter(250, 408)
figter_2 = Fighter(900, 408)


# loop do jogo
run = True
while run:
    # defininido o fps do jogo
    clock.tick(FPS)

    # colocando o bg na tela
    draw_bg()

    # mostrando a barra de vida na tela
    draw_health_bar(figter_1.health, 20, 20)
    draw_health_bar(figter_2.health, 860, 20)

    # implementando a movimentação
    figter_1.move(SCREEN_WIDHT, SCREEN_HEIGHT, screen, figter_2)
    
    
    # desenhando os players na tela 
    figter_1.draw(screen)
    figter_2.draw(screen)

    # comando de evento
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # atualizando a tela
    pygame.display.update()

# fechando o pygame
pygame.quit()
