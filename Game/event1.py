import pygame
import button
import button2
from pygame.locals import *
from pygame import mixer

pygame.init()

def event_sequence(text, hp_bonus):
    SCREEN_SIZE = (800, 400)
    screen_event = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Event")
    clock = pygame.time.Clock()

    eventbg_image = pygame.image.load("images/background.png")

    def draw_background():
        screen_event.blit(eventbg_image, (0, 0))

    def draw_text(text, font, color, x, y):
        title = font.render(text, True, color)
        screen_event.blit(title, (x, y))
 
    font_1 = pygame.font.SysFont("cambria", 24)
    font_2 = pygame.font.SysFont("cambria", 18)

    white = (255, 255, 255)

    options1_image = pygame.image.load("images/options1.png").convert_alpha()
    options2_image = pygame.image.load("images/options2.png").convert_alpha()
    options1_button = button.Button(options1_image, 500, 175)
    options2_button = button.Button(options2_image, 500, 275)


    event_state = "event1"


    run = True
    while run:
        campfire_img =  pygame.image.load('battle/img/icons/campfire.png').convert_alpha()
        campfire_button = button2.Button(screen_event, 700, 300, campfire_img, 64, 64)
        draw_background()

        if event_state == "event1":
            draw_text(text[0], font_1, white, 80, 70)
            draw_text(text[1], font_1, white, 80, 125)
            draw_text(text[2] , font_2, white, 80, 175)
            draw_text(text[3], font_2, white, 80, 275)
            if options1_button.draw(screen_event) :
                event_state = "options1"
            if options2_button.draw(screen_event) :
                draw_text(text[5], font_1, white, 80, 150)
                event_state = "options2"
        if event_state == "options1":
            draw_text(text[4], font_1, white, 80, 150)
            hp = hp_bonus[0]
        if event_state == "options2":
            draw_text(text[5], font_1, white, 80, 150)
            hp = hp_bonus[1]
        #event handler
        if campfire_button.draw():
            return hp
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        #update display
        pygame.display.update()


