import asyncio
import pygame
from fighter import Fighter
from pygame import mixer


# iniciando o mixer
mixer.init()
# iniciando o loop do pygame
pygame.init()

# criando a janela do jogo
SCREEN_WIDHT = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDHT, SCREEN_HEIGHT))
pygame.display.set_caption("Hills Fight")
async def main():
    # carregando o background
    bg_image = pygame.image.load("assets/images/background/bg.jpg").convert_alpha()

    # setando o frame do jogo
    clock = pygame.time.Clock()
    FPS = 60

    # definindo cores
    RED = (255, 0, 0)
    GREY = (140, 139, 132)
    WHITE = (255, 255, 255)
    GREEN = (52, 184, 0)

    # definindo as variaveis do jogo
    intro_count = 3
    last_count_update = pygame.time.get_ticks()
    score = [0, 0] # player scores [p1, p2]
    round_over = False
    ROUND_OVER_COOLDOWN = 2000
    timer_count = 60



    # definindo as variaveis dos players
    WARRIOR_SIZE = 162
    WARRIOR_SCALE = 4
    WARRIOR_OFFSET = [72, 56]
    WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
    WIZZARD_SIZE = 250
    WIZZARD_SCALE = 3
    WIZZARD_OFFSET = [112, 107]
    WIZZARD_DATA = [WIZZARD_SIZE, WIZZARD_SCALE, WIZZARD_OFFSET]

    # carregando a musica e os sons 
    pygame.mixer.music.load("assets/audio/assets_audio_music.mp3")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1, 0.0, 5000)
    sword_fx = pygame.mixer.Sound("assets/audio/assets_audio_sword.wav")
    sword_fx.set_volume(0.1)
    magic_fx = pygame.mixer.Sound("assets/audio/assets_audio_magic.wav")
    magic_fx.set_volume(0.2)

    # carregando as sprites sheets
    warrior_sheet = pygame.image.load("assets/images/warrior/warrior.png").convert_alpha()
    wizard_sheet = pygame.image.load("assets/images/wizard/wizard.png").convert_alpha()

    # carregando a img da vitoria
    victory_img = pygame.image.load("assets/images/icons/victory.png").convert_alpha()


    # definindo o numero de sprites em cada animacao
    WARRIOR_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
    WIZARD_ANIMATION_STEPS = [8, 8, 1, 8, 8, 3, 7]

    # definindo as fontes
    count_font = pygame.font.Font("assets/fonts/turok.ttf", 120)
    score_font = pygame.font.Font("assets/fonts/turok.ttf", 30)
    timer_font = pygame.font.Font("assets/fonts/turok.ttf", 60)
    draw_font = pygame.font.Font("assets/fonts/turok.ttf", 120)
    vic_font = pygame.font.Font("assets/fonts/turok.ttf", 120)




    # fonte para o  texto
    def draw_text(text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        screen.blit(img, (x, y))

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
    figter_1 = Fighter(1, 250, 408, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
    figter_2 = Fighter(2, 900, 408, True, WIZZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)


    # loop do jogo

    run = True
    while run:
        # defininido o fps do jogo
        clock.tick(FPS)

        # colocando o bg na tela
        # scroll bg
        draw_bg()
        # resentado o scroll

        # mostrando a barra de vida na tela
        draw_health_bar(figter_1.health, 20, 20)
        draw_health_bar(figter_2.health, 860, 20)
        # mostrando o score
        draw_text("P1: " + str(score[0]), score_font, RED, 16, 40)
        draw_text("P2: " + str(score[1]), score_font, RED, 856, 40)
        
        # colocando o timer no jogo
        if intro_count <= 0:
            # implementando a movimentação
            figter_1.move(SCREEN_WIDHT, SCREEN_HEIGHT, screen, figter_2, round_over)
            figter_2.move(SCREEN_WIDHT, SCREEN_HEIGHT, screen, figter_1, round_over)
            draw_text(str(timer_count),timer_font, WHITE, SCREEN_WIDHT/2 - 30, 5)
            if (pygame.time.get_ticks() - last_count_update) >= 1000:
                timer_count -= 1
                last_count_update = pygame.time.get_ticks()
                if timer_count <= 0:
                    timer_count = 0
                
        else:
            # coloando o timer na tela
            draw_text(str(intro_count), count_font, RED, SCREEN_WIDHT / 2 - 20, SCREEN_HEIGHT / 4 - 60)
            # atualizando o contador do timer
            if (pygame.time.get_ticks() - last_count_update) >= 1000:
                intro_count -= 1
                last_count_update = pygame.time.get_ticks()
                

        # atualizando as imagens
        figter_1.update()
        figter_2.update()
        
        
        # desenhando os players na tela 
        figter_1.draw(screen)
        figter_2.draw(screen)

        # checando quem perdeu
        if round_over == False:
            if figter_1.alive == False:
                score[1] += 1
                round_over = True
                round_over_time = pygame.time.get_ticks()
                final_txt = ("P2 WON")
            elif figter_2.alive == False:
                score[0] += 1
                round_over = True
                round_over_time = pygame.time.get_ticks()
                final_txt = ("P1 WON")
            elif figter_1.alive == True and figter_2.alive == True and timer_count <= 0:
                # colocando a img de empate na tela
                round_over = True
                timer_count = timer_count
                round_over_time = pygame.time.get_ticks()
                final_txt = ("DRAW")
        else:
            draw_text(final_txt, vic_font, RED, SCREEN_WIDHT / 2 - 140, SCREEN_HEIGHT / 4 - 60)
            if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
                round_over = False
                intro_count = 2
                timer_count = 60
                figter_1 = Fighter(1, 250, 408, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
                figter_2 = Fighter(2, 900, 408, True, WIZZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)

        # comando de evento
        await asyncio.sleep(0)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # atualizando a tela
        pygame.display.update()

    # fechando o pygame
    pygame.quit()
asyncio.run( main() )