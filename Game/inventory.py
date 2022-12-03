import pygame
from sys import exit
import button2

pygame.init()
def inventory_sequence(equipped):
    screen = pygame.display.set_mode((800,400))
    pygame.display.set_caption('Lone Adventurer')
    clock = pygame.time.Clock()
    font = pygame.font.Font('font/AncientModernTales.ttf',50)

    background_surf = pygame.image.load('graphics/background.jpg')
    background_rect = background_surf.get_rect(center = (400,500))

    inven_text_surf = font.render('Inventory', False, 'Red')
    inven_text_rect = inven_text_surf.get_rect(topleft = (550,20))

    stats_text_surf = font.render('Str: ',False, 'Red')
    stats_text_rect = inven_text_surf.get_rect(topleft = (550,200))

    knight_img_surf = pygame.image.load('graphics/knight.png')
    knight_img_surf = pygame.transform.scale(knight_img_surf,(70,70))
    knight_img_rect = knight_img_surf.get_rect(topleft = (600,300))

    wep_strength = 0

    screen_width = 800 
    screen_height = 400 



    #scrolling inventory
    scroll_surf = pygame.Surface((450,1000))
    scroll_surf.fill((94,38,18))
    scroll_rect = scroll_surf.get_rect(topleft = (0,-20))


    #loading in weapon surfaces
    weapon_count = 4
    sword_surf = pygame.image.load('graphics/weapons/icon_sword_short1.png')
    spear_surf = pygame.image.load('graphics/weapons/icon_spear2.png')
    dagger_surf = pygame.image.load('graphics/weapons/icon_dagger3.png')
    axe_surf = pygame.image.load('graphics/weapons/icon_axe3.png')


    item_x_pos,item_y_pos,border = 50, 130,10

    #equip button
    equip_button_surf = font.render('Equip',False,'Red')
    equipped_button_surf = font.render('Equipped',False,'Green')

    class Ebutton():
        def __init__(self,x,y,equip_img,equipped_img,scale):
            width = equip_img.get_width()
            height = equip_img.get_height()
            self.image = pygame.transform.scale(equip_img,(int(width*scale),int(height*scale)))
            self.eimage = pygame.transform.scale(equipped_img,(int(width*scale),int(height*scale)))
            self.rect = self.image.get_rect()
            self.rect.topleft = (x,y)
            self.clicked = False

        def draw(self):
            pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(pos):
                if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                    self.clicked = True
                    print('clicked')
                    

            if self.clicked:
                screen.blit(self.eimage,(self.rect.x,self.rect.y))
            else: 
                screen.blit(self.image,(self.rect.x,self.rect.y))
            


    class Weapon():
        def __init__(self,weapon_num,weapon_img,str_val,scale):
            width = weapon_img.get_width()
            height = weapon_img.get_height()
            self.weapon_num = weapon_num
            self.weapon_img = pygame.transform.scale(weapon_img,(int(width*scale),int(height*scale)))
            self.rect = self.weapon_img.get_rect()
            self.rect.topleft = (30,-110 + (130 * weapon_num) + 10)
            self.desc = font.render('Str: ' + str(str_val), False, 'Red')
            self.str_val = str_val
            self.button = Ebutton(300, -110 + (130 * weapon_num) + 10,equip_button_surf,equipped_button_surf,.7)
            self.equipped = False

        def draw(self):
            Rect = (self.rect.x - 20,self.rect.y-20,430,120)
            pygame.draw.rect(screen,'Black',Rect)
            screen.blit(self.desc,(self.rect.x + 50,self.rect.y))
            screen.blit(self.weapon_img,(self.rect.x,self.rect.y))



    def show_str():
        strength_display = font.render(str(wep_strength), False, 'Red')
        screen.blit(strength_display,(650,200))

    sword = Weapon(1,sword_surf,10,1.5)
    spear = Weapon(2,spear_surf,7,1.5)
    axe = Weapon(3,axe_surf,15,1.5)
    dagger = Weapon(4,dagger_surf,5,1.5)

    weapon_list = []
    weapon_list.extend([sword,spear,axe,dagger])
            

    run = True
    while run:
        campfire_img =  pygame.image.load('battle/img/icons/campfire.png').convert_alpha()
        campfire_button = button2.Button(screen, 700, 300, campfire_img, 64, 64)
        #visuals for inventory
        screen.blit(background_surf,background_rect)
        screen.blit(inven_text_surf,inven_text_rect)
        screen.blit(scroll_surf,scroll_rect)
        screen.blit(stats_text_surf,stats_text_rect)
        screen.blit(knight_img_surf,knight_img_rect)

        show_str()
        
        #load in weapon and buttons for inventory
        for wep in weapon_list:
            wep.draw()
            wep.button.draw()

            #if a weapon is equipped, all other weapons are unequipped
            if wep.button.clicked:
                for wep_compare in weapon_list:
                    if wep != wep_compare:
                        wep_compare.button.clicked = False
                wep_strength = wep.str_val
                equipped = wep.weapon_num   

        for wep in weapon_list:
                if wep.weapon_num == equipped:
                    wep.button.clicked = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()



            #for scrolling the inventory screen
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #if scroll down move screen up
                if event.button == 4:
                    scroll_rect.y += 13
                    for wep in weapon_list:
                        wep.rect.y+= 13
                        wep.button.rect.y+=13
                #if scroll up move screen down
                if event.button == 5:
                    scroll_rect.y -= 13
                    for wep in weapon_list:
                        wep.rect.y -= 13
                        wep.button.rect.y -=13  

        if campfire_button.draw():
            return equipped, wep_strength
            run = False
            
        pygame.display.update()
        clock.tick(60)