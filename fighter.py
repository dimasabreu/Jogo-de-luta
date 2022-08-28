import pygame

# criando a classe do player
class Fighter():

    # player constructor
    def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps):
        self.player = player
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.flip = flip
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.action = 0 #0:idle #1:correndo #2:pulando #3:attack1 #4:attack2 #5:hit #6:death
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.rect = pygame.Rect((x, y, 80, 180))
        self.vel_y = 0
        self.running = False
        self.jump = False
        self.attacking = False
        self.attack_type = 0
        self.attack_cooldown = 0
        self.hit = False
        self.health = 90 # debug de vida e original eh 0
        self.alive = True

    # func para pegar as sprites
    def load_images(self, sprite_sheet, animation_steps):
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
                temp_img_list.append(pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale)))
            animation_list.append(temp_img_list)
        return animation_list

    # func de movimentacao
    def move(self, screen_width, screen_height, surface, target, round_over):
        SPEED = 10
        GRAVITY = 2
        dx = 0
        dy = 0
        self.running = False
        self.attack_type = 0

        # pegando as teclas apertadas
        key = pygame.key.get_pressed()

        # So pode fazer alguma coisa caso nao esteja atacando 
        if self.attacking == False and self.alive == True and round_over == False:
            # checando os controles do player 1
            if self.player == 1:
                # movendo para esquerda
                if key [pygame.K_a]:
                    dx = -SPEED
                    self.running = True

                # movendo para direita
                if key [pygame.K_d]:
                    dx = SPEED
                    self.running = True

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
            
            # checando os controles do player 2
            if self.player == 2:
                # movendo para esquerda
                if key [pygame.K_LEFT]:
                    dx = -SPEED
                    self.running = True

                # movendo para direita
                if key [pygame.K_RIGHT]:
                    dx = SPEED
                    self.running = True

                # criando o pulo
                if key[pygame.K_UP] and self.jump == False:
                    self.vel_y = -30
                    self.jump = True

                # criando os ataques 
                if key[pygame.K_KP1] or key[pygame.K_KP2]:
                    self.attack(surface, target)
                    # determinando qual ataque eh
                    if key[pygame.K_KP1]:
                        self.attack_type = 1
                    if key[pygame.K_KP2]:
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

        # cooldown dos ataques
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        # atualizando a posição do player
        self.rect.x += dx
        self.rect.y += dy
    
    # atualizando as animações
    def update(self):
        # checando qual acao o jogador esta fazendo
        if self.health >= 100:
            self.health = 100
            self.alive = False
            self.update_action(6)
        elif self.hit == True:
            self.update_action(5)
        elif self.attacking == True:
            if self.attack_type == 1:
                self.update_action(3)
            elif self.attack_type == 2:
                self.update_action(4)
        elif self.jump == True:
            self.update_action(2)
        elif self.running == True:
            self.update_action(1)
        else:
            self.update_action(0)

        animation_cooldown = 50
        # atualizando a imagem
        self.image = self.animation_list[self.action][self.frame_index]
        # checando quanto tempo se passou desde a ultima atualizacao
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        # checando se a animacao acabou
        if self.frame_index >= len(self.animation_list[self.action]):
            # checando se o player morreu
            if self.alive == False:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0
                # checando se o ataque foi concluido
                if self.action == 3 or self.action == 4:
                    self.attacking = False
                    self.attack_cooldown = 20
                # checando se o player foi atingido
                if self.action == 5:
                    self.hit = False
                    # se o player estiver no meio do ataque ele para
                    self.attacking = False
                    self.attack_cooldown = 20

    # criando o metodo de ataque
    def attack(self, surface, target):
        if self.attack_cooldown == 0:
            self.attacking = True
            attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width, self.rect.height)
            if attacking_rect.colliderect(target.rect):
                target.health += 10
                target.hit = True
            pygame.draw.rect(surface, (0, 255, 0), attacking_rect)


    def update_action(self, new_action):
        # checando se a nova acao eh diferente da antiga
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    # definindo o desenho do player
    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        pygame.draw.rect(surface, (255, 0, 0), self.rect)
        surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))
