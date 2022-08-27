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
# carregando o background
bg_image = pygame.image.load("assets/images/background/background.jpg").convert_alpha()


# func para colocar o bg na tela
def draw_bg():
    # modificando o tamanho da imagem
    scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDHT, SCREEN_HEIGHT))
    # colocando a imagem na tela e a posicao que ela vai aparecer
    screen.blit(scaled_bg, (0, 0))


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
    # implementando a movimentação
    figter_1.move(SCREEN_WIDHT, SCREEN_HEIGHT)
    
    
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
