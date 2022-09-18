from ast import Num
from sre_parse import WHITESPACE
import pygame
from fighter import Fighter
import os

# n = Network()
# p = n.getP()
pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
clicked_play = False
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Avatar Fight Game")
clock = pygame.time.Clock()
FPS = 60

RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

pygame.mixer.music.load("assets/audio/soundtrack.mp3")
pygame.mixer.music.play(-1, 0.0, 5000)

bg_image =  pygame.image.load("assets/images/background/background.png").convert_alpha()

def introduction():
    title_img = pygame.image.load("assets/images/introduction/Intro1.png").convert_alpha()
    screen.blit(title_img, (0,0))

def draw_start_button():
    button_rect = pygame.draw.rect(screen, WHITE, (419,500,162,60))
    button = pygame.image.load("assets/images/introduction/normal.png").convert_alpha()
    button_scaled = pygame.transform.scale(button, (162, 60))
    screen.blit(button_scaled, (419,500))
    return button_rect
def update_button():
    pygame.draw.rect(screen, WHITE, (419,500,162,60))
    button = pygame.image.load("assets/images/introduction/hover.png").convert_alpha()
    button_scaled = pygame.transform.scale(button, (162, 60))
    screen.blit(button_scaled, (419,500))


def draw_bg(screen):
    scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0,0))

def draw_health_bar(health, x, y):
    pygame.draw.rect(screen, WHITE, (x-2,y-2,404,34))
    pygame.draw.rect(screen, RED, (x,y,400,30))
    ratio = health/100
    pygame.draw.rect(screen, YELLOW, (x,y,400*ratio,30))

player = "aang"
fighter_1 = Fighter(1, 200, 270, False, player)
fighter_2 = Fighter(2, 700, 270, True, player)
fighter_1.load_images()

run = True
intro = True
title_sc = True

def choose_characters(screen):
    run = True
    aang = pygame.image.load("assets/images/introduction/aang_intro.png").convert_alpha()
    katara = pygame.image.load("assets/images/introduction/katara_intro.png").convert_alpha()
    zuko = pygame.image.load("assets/images/introduction/zuko_intro.png").convert_alpha()


    characters = []
    chars_selected = 0
    for player in range(0,2):
        while run:

            title_img = pygame.image.load("assets/images/introduction/background-2.png").convert_alpha()
            scaled_img = pygame.transform.scale(title_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
            screen.blit(scaled_img, (0,0))

            font = pygame.font.Font('assets/fonts/LcdSolid-VPzB.ttf', 32)

            text = font.render(f"PLAYER {player+1}, choose your player...", True, (0,0,0), (173, 182,213))
            textRect = text.get_rect()

            
                        
                # copying the text surface object
                # to the display surface object
                # at the center coordinate.
            screen.blit(text, textRect)
            aang_rect = pygame.draw.rect(screen, WHITE, (330, 147.5, 290, 65))
            katara_rect = pygame.draw.rect(screen, WHITE, (330, 266.5, 290, 65))
            zuko_rect = pygame.draw.rect(screen, WHITE, (330, 381.5, 290, 62))

            screen.blit(pygame.transform.scale(aang, (317, 112)), (317,112))
            screen.blit(pygame.transform.scale(katara, (317, 112)), (317,224))
            screen.blit(pygame.transform.scale(zuko, (317, 112)), (317,336))

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    if aang_rect.collidepoint(pos):
                        chars_selected +=1
                        
                        if chars_selected == 2:
                            run = False
                        characters.append("aang")
                        print(player)

                    elif katara_rect.collidepoint(pos):
                        chars_selected +=1
                        print(player)
                        if chars_selected ==2:
                            run = False
                        characters.append("katara")

                    elif zuko_rect.collidepoint(pos):
                        chars_selected +=1
                        characters.append("zuko")
                        if chars_selected == 2:
                            run = False
                    

                if event.type == pygame.QUIT:
                    run = False

            pygame.display.update()        
        return characters

def intro_screen(screen):
    intro = True
    while intro:
        if title_sc:
            introduction()
            button_rect = draw_start_button()
        ev = pygame.event.get()

        for event in ev:
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if button_rect.collidepoint(pos):
                    update_button()
                    intro = False
                    break

            if event.type == pygame.QUIT:
                intro = False

        pygame.display.update() 
intro_screen(screen)

characters = choose_characters(screen)
fighter_1 = Fighter(1, 200, 270, False, characters[0])
fighter_2 = Fighter(2, 700, 270, True, characters[1])
fighter_1.load_images()
fighter_2.load_images()

while run:
    clock.tick(FPS)
    draw_bg(screen)    
    draw_health_bar(fighter_1.health, 20, 20)
    draw_health_bar(fighter_2.health, 580, 20)

    fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2)
    fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1)

    fighter_1.update()
    fighter_2.update()

    fighter_1.draw(screen)
    fighter_2.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update() 

pygame.quit() 