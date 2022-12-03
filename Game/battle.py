import pygame
import random
import button2
import sys 
import map

pygame.init()

def battle_sequence(wep_str, hp_bonus):
    clock = pygame.time.Clock()
    fps = 60

    bottom_panel = 150
    screen_width = 800
    screen_height = 400 + bottom_panel
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Lone Adventurer')


    #game variables
    current_fighter = 1
    total_fighters = 2
    action_cooldown = 0
    action_wait_time = 90
    attack = False
    potion = False
    potion_effect = 15
    clicked = False
    game_over = 0 



    #font
    font = pygame.font.Font('battle\img\AncientModernTales.ttf.ttf', 26)

    #define colors
    red = (255, 0, 0)
    green = (0, 255, 0)

    #load images
    #background images
    background_img1 = pygame.image.load('battle/img/caverns/layers/background.png').convert_alpha()
    background_img2 = pygame.image.load('battle/img/caverns/layers/back-walls.png').convert_alpha()
    background_img3 = pygame.image.load('battle/img/caverns/layers/tiles.png').convert_alpha()

    #panel image
    panel_img = pygame.image.load('battle/img/icons/panel.png').convert_alpha()

    #cursor image
    cursor_img = pygame.image.load('battle/img/icons/cursor.png').convert_alpha()

    #potion image
    potion_img = pygame.image.load('battle/img/icons/potion.png').convert_alpha()

    campfire_img =  pygame.image.load('battle/img/icons/campfire.png').convert_alpha()

    #load victory and defeat image
    victory_img = pygame.image.load('battle/img/icons/victory.png').convert_alpha()
    defeat_img = pygame.image.load('battle/img/icons/defeat.png').convert_alpha()






    #drawing text
    def draw_text(text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        screen.blit(img, (x, y))


    #drawing background
    def draw_bg():
        screen.blit(background_img1,(0,0))
        screen.blit(background_img2,(0,0))
        screen.blit(background_img3,(0,0))
    #draws UI action panel
    def draw_panel():
        #draw panel 
        screen.blit(panel_img,(0,screen_height - bottom_panel))
        #show knight stats
        draw_text(f'{knight.name} HP: {knight.hp}', font, red, 100, screen_height - bottom_panel + 10)
        #show name and health
        draw_text(f'{bandit1.name} HP: {bandit1.hp}', font, red, 550, screen_height - bottom_panel + 10)







    #player class
    class Player():
        def __init__(self, x, y, name, max_hp, strength, potions):
            self.name = name
            self.max_hp = max_hp
            self.hp = max_hp
            self.strength = strength
            self.start_potions = potions
            self.potions = potions
            self.alive = True
            self.animation_list =  []
            self.frame_index = 0
            self.action = 0  #0: idle, 1:attack, 2: dead
            self.update_time = pygame.time.get_ticks()
            
            #load idle images
            temp_list = []
            for i in range(4):
                img = pygame.image.load(f'battle/img/{self.name}/idle/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (img.get_width() * 1.6, img.get_height() *1.6))
                temp_list.append(img)
            self.animation_list.append(temp_list)
        
            #load attack images
            temp_list = []
            for i in range(8):
                img = pygame.image.load(f'battle/img/{self.name}/Attack/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (img.get_width() * 1.6, img.get_height() *1.6))
                temp_list.append(img)
            self.animation_list.append(temp_list)
            self.image = self.animation_list[self.action][self.frame_index] 
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)

            #load death images
            temp_list = []
            for i in range(5):
                img = pygame.image.load(f'battle/img/{self.name}/Death/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (img.get_width() * 1.6, img.get_height() *1.6))
                temp_list.append(img)
            self.animation_list.append(temp_list)
            self.image = self.animation_list[self.action][self.frame_index] 
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)


        def update(self):
            animation_cooldown = 100
            #handle animation
            #update animation
            self.image = self.animation_list[self.action][self.frame_index]
            #check if enough time has passed since last update
            if pygame.time.get_ticks() - self.update_time > animation_cooldown:
                self.update_time = pygame.time.get_ticks()
                self.frame_index += 1
            #if the animation has run out, then reset back to first frame
            if self.frame_index >= len(self.animation_list[self.action]):
                if self.action == 2:
                    self.frame_index = len(self.animation_list[self.action]) -1
                else:
                    self.idle()

        def idle(self):
            self.action = 0
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()



        def attack(self, target):
            #deal damage
            rand = random.randint(-5, 5)
            damage = self.strength + rand
            target.hp -= damage
            #check if target has died
            if target.hp < 1:
                target.hp = 0
                target.alive = False
                target.death()
            damage_text = DamageText(target.rect.centerx, target.rect.y, str(damage), red)
            damage_text_group.add(damage_text)
            #set variables to attack animation
            self.action = 1
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

        def death(self):
            self.action = 2 
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

        def draw(self):
            screen.blit(self.image, self.rect)



    class Healthbar():
        def __init__(self, x, y, hp, max_hp):
            self.x = x
            self.y = y
            self.hp = hp
            self.max_hp = max_hp

        def draw(self, hp):
            #update with new health
            self.hp = hp
            #calculate health
            ratio = self.hp / self.max_hp
            pygame.draw.rect(screen, red, (self.x, self.y, 150, 20))
            pygame.draw.rect(screen, green, (self.x, self.y, 150 * ratio, 20))

    class DamageText(pygame.sprite.Sprite):
        def __init__(self, x, y, damage, color):
            pygame.sprite.Sprite.__init__(self)
            self.image = font.render(damage, True, color)
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)
            self.counter = 0

        def update(self):
            #move damage text up 
            self.rect.y -= 1
            #delete text after a few seconds
            self.counter += 1
            if self.counter > 30:
                self.kill()

    damage_text_group = pygame.sprite.Group()      

    knight = Player(225, 175, 'knight', 30 + hp_bonus, 7 + wep_str, 3)
    bandit1 = Player(500, 170, 'Bandit', 20, 5, 0)

    bandit_list = []
    bandit_list.append(bandit1)

    knight_health_bar = Healthbar(100, screen_height - bottom_panel + 40, knight.hp, knight.max_hp)
    bandit1_health_bar = Healthbar(550, screen_height - bottom_panel + 40, bandit1.hp, bandit1.max_hp)

    potion_button = button2.Button(screen, 100, screen_height - bottom_panel + 70, potion_img, 64, 64)
    campfire_button = button2.Button(screen, 200, screen_height - bottom_panel + 70, campfire_img, 64, 64)

    won = True
    run = True

    while run:
        clock.tick(fps)

        #draws background
        draw_bg()

        #draw_panel
        draw_panel()    
        knight_health_bar.draw(knight.hp)
        bandit1_health_bar.draw(bandit1.hp)

        #draw Player
        knight.update()
        knight.draw()
        for bandit in bandit_list:
            bandit.update()
            bandit.draw()

        #draw damage text
        damage_text_group.update()
        damage_text_group.draw(screen)

        #control player input
        #reset action variables
        attack = False
        potion = False
        target = None
        #makes sure mouse is visible
        pygame.mouse.set_visible(True)
        pos = pygame.mouse.get_pos()
        for count, bandit in enumerate(bandit_list):
            if bandit.rect.collidepoint(pos):
                
                pygame.mouse.set_visible(False)
                #show sword in place of mouse cursor
                screen.blit(cursor_img, pos)
                if clicked == True and bandit.alive == True:
                    attack = True
                    target = bandit_list[count]

        if potion_button.draw():
            potion = True
        #show number of potions remaining
        draw_text(str(knight.potions), font, red, 150, screen_height - bottom_panel + 70)
        if game_over == 0:
            #player action
            if knight.alive == True:
                if current_fighter == 1:
                    action_cooldown += 1
                    if action_cooldown >= action_wait_time:
                        #look for player action
                        #attack
                        if attack == True and target != None: 
                            knight.attack(target)
                            current_fighter += 1
                            action_cooldown = 0
                        #potion
                        if potion == True:
                            if knight.potions > 0:
                                #check if potion would heal player beyond max hp
                                if knight.max_hp - knight.hp > potion_effect :
                                    heal_amount = potion_effect 
                                else: 
                                    heal_amount = knight.max_hp - knight.hp
                                knight.hp += heal_amount
                                knight.potions -= 1
                                damage_text = DamageText(knight.rect.centerx, knight.rect.y, str(heal_amount), green)
                                damage_text_group.add(damage_text)
                                current_fighter += 1
                                action_cooldown = 0
            else:
                game_over = -1                    



            #enemy action
            for count, bandit in enumerate(bandit_list):
                if current_fighter == 2 + count:
                    if bandit.alive == True:
                        action_cooldown += 1
                        if action_cooldown >= action_wait_time:
                            #attack
                            bandit.attack(knight)
                            current_fighter += 1
                            action_cooldown = 0
                    else:
                        current_fighter += 1

                #if all fighters had a turn then reset
                if current_fighter > total_fighters:
                    current_fighter = 1

            #check if all enemies are dead
            alive_bandits = 0
            for bandit in bandit_list:
                if bandit.alive == True:
                    alive_bandits += 1
            if alive_bandits == 0:
                game_over = 1

            #check if game is over
        if game_over != 0:
            if game_over == 1:
                screen.blit(victory_img, (250, 50))
            if game_over == -1:
                screen.blit(defeat_img, (290, 50))
                won = False
            if campfire_button.draw():
                #map function will go here to go back to overworld
                run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
            else:
                clicked = False
        
        pygame.display.update()

    return won
