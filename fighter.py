import pygame
# criando a classe do player
class Fighter():
    # player constructor
    def __init__(self, x, y):
        self.rect = pygame.Rect((x, y, 80, 180))
        self.vel_y = 0

    #func de movimentacao
    def move(self, screen_width, screen_height):
        SPEED = 10
        GRAVITY = 2
        dx = 0
        dy = 0

        # pegando as teclas apertadas
        key = pygame.key.get_pressed()

        # movendo para esquerda
        if key [pygame.K_a]:
            dx = -SPEED
        # movendo para direita
        if key [pygame.K_d]:
            dx = SPEED
        # criando o pulo
        if key[pygame.K_w]:
            self.vel_y = -30
        # aplicando a gravidade
        self.vel_y += GRAVITY
        dy += self.vel_y
        
        # deixando o jogador preso na tela
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right
        if self.rect.bottom + dy > screen_height - 132:
            self.vel_y = 0
            dy = screen_height - 132 - self.rect.bottom
        # atualizando a posição do player
        self.rect.x += dx
        self.rect.y += dy

    # definindo o desenho do player
    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.rect)
