import pygame
import os

class Fighter():
    def __init__(self,player,x,y, flip, character):
        self.character = character
        self.player = player
        self.animate = True
        self.flip = flip
        self.rect = pygame.Rect((x,y, 80, 180))
        self.action_types = ["idle", "attack1", "attack2", "defeat", "jump"]
        self.animation_list, self.animation_steps = self.load_images()
        self.defeated = False
        self.jump = False
        self.attacking = False
        self.attack_type = 0
        self.attack_cooldown = 0
        self.health = 100
        self.action = 0
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()

    def load_images(self):
        animation_list = []
        animation_steps = []
        for action_folder in self.action_types:
            directory = f"assets/images/characters/{self.character}/{action_folder}"

            temp_img_list = []
            for filename in os.listdir(directory):
                f = os.path.join(directory, filename)
                temp_img = pygame.image.load(f).convert_alpha()
                temp_img_list.append(pygame.transform.scale(temp_img, (136*1.75,115*1.75)))
            animation_list.append(temp_img_list)
            animation_steps.append(len(temp_img_list))
        return animation_list, animation_steps
        

    def move(self, screen_width, screen_height, surface, opponent):
        SPEED = 10
        GRAVITY = 4
        dx = 0
        dy = 0
        vel_y = 0
        # self.attack_type = 0
        key = pygame.key.get_pressed()
        if not self.attacking:
            if self.player == 1:
                if key[pygame.K_a]:
                    dx = -SPEED
                if key[pygame.K_d]:
                    dx = SPEED
                
                if key[pygame.K_w] and not self.jump:
                    vel_y = -80
                    self.jump = True
                
                if key[pygame.K_q] or key[pygame.K_e]:
                    if key[pygame.K_q]:
                        self.attack_type = 1
                        self.attack_1(opponent)
                    if key[pygame.K_e]:
                        self.attack_type = 2
                        self.attack_2(opponent)
            if self.player ==2:
                if key[pygame.K_LEFT]:
                    dx = -SPEED
                if key[pygame.K_RIGHT]:
                    dx = SPEED
                
                if key[pygame.K_UP] and not self.jump:
                    vel_y = -80
                    self.jump = True
                
                if key[pygame.K_KP_1] or key[pygame.K_KP0]:
                    if key[pygame.K_KP_1]:
                        self.attack_type = 1
                        self.attack_1(opponent)
                    if key[pygame.K_KP_0]:
                        self.attack_type = 2
                        self.attack_2(opponent)

        dy += vel_y + GRAVITY

        if self.rect.left + dx <0:
            dx = -self.rect.left
        
        if self.rect.right + dx >screen_width:
            dx = screen_width -self.rect.right
        
        if self.rect.bottom + dy > screen_height - 90:
            self.vel_y = 0 
            self.jump = False
            dy = screen_height -90 - self.rect.bottom

        if opponent.rect.centerx > self.rect.centerx:
            self.flip = False
        if opponent.rect.centerx < self.rect.centerx:
            self.flip = True
        
        if self.attack_cooldown>0:
            self.attack_cooldown -= 1 

        self.rect.x += dx
        self.rect.y += dy
 
    def update(self):
        if self.jump :
            self.update_action(4)

        elif self.health <= 0:
            self.update_action(3)

        elif self.attacking and (self.attack_type ==1):
            self.update_action(1)
        
        elif self.attacking and (self.attack_type == 2):
            self.update_action(2)

        else:
            self.update_action(0)

        animation_cooldown = 100
        self.image = self.animation_list[self.action][self.frame_index]
        if self.animate:
            if pygame.time.get_ticks() - self.update_time > animation_cooldown:
                self.frame_index += 1
                self.update_time = pygame.time.get_ticks()


            if self.frame_index >= len(self.animation_list[self.action]):
                self.frame_index = 0
                if self.action == 1 or self.action == 2:
                    self.attacking = False
                    self.attack_cooldown = self.action*40

                if self.action == 3:
                    self.frame_index = 1
                    self.animate = False
                
            
    def attack_1(self, target):
        self.attacking = True
        attacking_rect = pygame.Rect(self.rect.centerx - (2*self.rect.width * self.flip), self.rect.y, 2* self.rect.width, self.rect.height)
        if attacking_rect.colliderect(target.rect):
            target.health -= 10


    def attack_2(self, target):
        self.attacking = True
        attacking_rect = pygame.Rect(self.rect.centerx - (2*self.rect.width * self.flip), self.rect.y, 2* self.rect.width, self.rect.height)
        if attacking_rect.colliderect(target.rect):
            target.health -= 10


    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        surface.blit(img, (self.rect.x-(75), self.rect.y-(5)))