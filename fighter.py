import pygame

# criando a classe do player
class Fighter():

    # player constructor
    def __init__(self, x, y):
        self.flip = False
        self.rect = pygame.Rect((x, y, 80, 180))
        self.vel_y = 0
        self.jump = False
        self.attacking = False
        self.attack_type = 0
        self.health = 0

    #func de movimentacao
    def move(self, screen_width, screen_height, surface, target):
        SPEED = 10
        GRAVITY = 2
        dx = 0
        dy = 0

        # pegando as teclas apertadas
        key = pygame.key.get_pressed()
        # So pode fazer alguma coisa caso nao esteja atacando 
        if self.attacking == False:
            # movendo para esquerda
            if key [pygame.K_a]:
                dx = -SPEED

            # movendo para direita
            if key [pygame.K_d]:
                dx = SPEED

            # criando o pulo
            if key[pygame.K_w] and self.jump == False:
                self.vel_y = -30
                self.jump = True

            # criando os ataques 
            if key[pygame.K_r] or key[pygame.K_t]:
                self.attack(surface, target)
                # determinando qual ataque eh
                if key[pygame.K_r]:
                    self.attack_type = 1
                if key[pygame.K_t]:
                    self.attack_type = 2

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
            self.jump = False
            dy = screen_height - 132 - self.rect.bottom

        # tendo certeza que os jogadores estao se olhando
        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True

        # atualizando a posição do player
        self.rect.x += dx
        self.rect.y += dy

    # criando o metodo de ataque
    def attack(self, surface, target):
        self.attacking = True
        attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width, self.rect.height)
        if attacking_rect.colliderect(target.rect):
            target.health += 10

        pygame.draw.rect(surface, (0, 255, 0), attacking_rect)

    # definindo o desenho do player
    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.rect)
