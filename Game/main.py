import pygame, sys
import button
from pygame.locals import *
from pygame import mixer
from data import encounters
from battle import battle_sequence
from map import Map
from event1 import event_sequence
import button2
from inventory import inventory_sequence

bottom_panel = 150
screen_width = 800 
screen_height = 400 + bottom_panel

pygame.init()
FINAL_ENCOUNTER = 11

screen = pygame.display.set_mode((screen_width, screen_height - bottom_panel))
clock = pygame.time.Clock()

quit_image = pygame.image.load("images/quit.png").convert_alpha()

#Map Logic + animation
def map():
    screen = pygame.display.set_mode((screen_width, screen_height))
    campfire_img =  pygame.image.load('battle/img/icons/campfire.png').convert_alpha()
    campfire_button = button2.Button(screen, 420, screen_height - bottom_panel + 70, campfire_img, 64, 64)
    quit_button = button.Button(quit_image, 20, screen_height - bottom_panel + 80)
    map = Map(0, FINAL_ENCOUNTER, screen)
    run = True
    equipped = 0
    wep_str = 0
    hp_bonus = 0
    while run:
        screen = pygame.display.set_mode((screen_width, screen_height))
        screen.fill('black')
        map.run()
        if map.current_encounter != FINAL_ENCOUNTER:       
            panel_img = pygame.image.load('battle/img/icons/panel.png').convert_alpha()
            screen.blit(panel_img,(0,screen_height - bottom_panel))
            mx, my = pygame.mouse.get_pos()
            current_button = map.nodes.sprites()[map.current_encounter].rect
            if current_button.collidepoint ((mx, my)):
                if click:
                    if map.current_encounter in {0, 1, 3, 4, 6, 7, 9, 10}:
                        if battle_sequence(wep_str, hp_bonus) == False:
                            run = False
                            screen = pygame.display.set_mode((screen_width, screen_height - bottom_panel))
                            map.current_encounter = 0
                    if map.current_encounter in {2, 5, 8}:
                        hp_bonus = event_sequence(encounters[map.current_encounter]["string_list"], encounters[map.current_encounter]["hp_bonus"]) + hp_bonus
                    map.current_encounter += 1 
            click = False
            if campfire_button.draw():
                equipped, wep_str = inventory_sequence(equipped)
            if quit_button.draw(screen):
                    run = False
                    screen = pygame.display.set_mode((screen_width, screen_height - bottom_panel))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True
        else:
            run = False
            screen = pygame.display.set_mode((screen_width, screen_height - bottom_panel))

        pygame.display.update()
        clock.tick(60)
        
#Main menu logic+animation
pygame.display.set_caption("Main Menu")

#Background image
background_image = pygame.image.load("images/background.png").convert_alpha()

#Draw background
def draw_background():
    screen.blit(background_image, (0, 0))

#Draw text
def draw_text(text, font, color, x, y):
    title = font.render(text, True, color)
    screen.blit(title, (x, y))

#Font
font_1 = pygame.font.SysFont("cambria", 65)
font_2 = pygame.font.SysFont("cambria", 25)

#Color
white = (255, 255, 255)

#Button images
start_image = pygame.image.load("images/start.png").convert_alpha()
settings_image = pygame.image.load("images/settings.png").convert_alpha()
audio_image = pygame.image.load('images/audio.png').convert_alpha()
back1_image = pygame.image.load('images/back1.png').convert_alpha()
back2_image = pygame.image.load('images/back2.png').convert_alpha()
m1_image = pygame.image.load('images/m1.png').convert_alpha()
m2_image = pygame.image.load('images/m2.png').convert_alpha()
m3_image = pygame.image.load('images/m3.png').convert_alpha()
m4_image = pygame.image.load('images/m4.png').convert_alpha()
m5_image = pygame.image.load('images/m5.png').convert_alpha()

#Button instances
start_button = button.Button(start_image, 340, 70)
settings_button = button.Button(settings_image, 340, 165)
quit_button = button.Button(quit_image, 340, 260)
audio_button = button.Button(audio_image, 210, 150)
back1_button = button.Button(back1_image, 345, 260)
back2_button = button.Button(back2_image, 345, 260)
m1_button = button.Button(m1_image, 280, 150)
m2_button = button.Button(m2_image, 350, 150)
m3_button = button.Button(m3_image, 420, 150)
m4_button = button.Button(m4_image, 490, 150)
m5_button = button.Button(m5_image, 560, 150)


mixer.init()
mixer.music.load('music/bg_music.mp3')
pygame.mixer.music.play(-1)

#Variables
next_step = False
menu_state = "main"

#Game loop
run = True
while run:

    #draw background
    draw_background()

    if next_step == True:
        #check main
        if menu_state == "main":
            if start_button.draw(screen):
                map()    #connect to map
            if settings_button.draw(screen):
                menu_state = "settings"
            if quit_button.draw(screen):
                run = False

        #check settings
        if menu_state == "settings":
            audio_button.draw(screen)
            if m1_button.draw(screen):
                mixer.music.set_volume(0.2)
            if m2_button.draw(screen):
                mixer.music.set_volume(0.4)
            if m3_button.draw(screen):
                mixer.music.set_volume(0.6)
            if m4_button.draw(screen):
                mixer.music.set_volume(0.8)
            if m5_button.draw(screen):
                mixer.music.set_volume(1.0)
            if back1_button.draw(screen):
                menu_state = "main"

        if menu_state == "audio":
            if back1_button.draw(screen):
                menu_state = "settings"
     
    else:
        #draw text
        draw_text("LONE ADVENTURER", font_1, white, 85, 100)
        draw_text("Press SPACE To MAIN MENU", font_2, white, 230, 250)


    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        if event.type == pygame.KEYDOWN:
            #press RETURN to go to the next step
            if event.key == pygame.K_SPACE:
                next_step = True

    #update display
    pygame.display.update()


























