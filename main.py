from cmath import rect
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

# definindo as variaveis dos players
WARRIOR_SIZE = 162
WARRIOR_SCALE = 4
WARRIOR_OFFSET = [72, 56]
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
WIZZARD_SIZE = 250
WIZZARD_SCALE = 3
WIZZARD_OFFSET = [112, 107]
WIZZARD_DATA = [WIZZARD_SIZE, WIZZARD_SCALE, WIZZARD_OFFSET]


# carregando o background
bg_image = pygame.image.load("assets/images/background/background.jpg").convert_alpha()

# carregando as sprites sheets
warrior_sheet = pygame.image.load("assets/images/warrior/warrior.png").convert_alpha()
wizard_sheet = pygame.image.load("assets/images/wizard/wizard.png").convert_alpha()

# definindo o numero de sprites em cada animacao
WARRIOR_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
WIZARD_ANIMATION_STEPS = [8, 8, 1, 8, 8, 3, 7]

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
figter_1 = Fighter(250, 408, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS)
figter_2 = Fighter(900, 408, True, WIZZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS)


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
