import pygame
import button2
from data import encounters


class Node(pygame.sprite.Sprite):
    def __init__(self, pos, path):
        super().__init__()
        self.pos = pos
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(center = pos)

class Background(pygame.sprite.Sprite):
    def __init__(self, pos, path):
        super().__init__()
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = pos 


class Map:
    def __init__(self, start_encounter, final_encounter, surface):

        self.display_surface = surface
        self.final_encounter = final_encounter
        self.current_encounter = start_encounter

        #sprites
        self.setup_nodes()
        self.setup_background()
        #self.setup_player()

    def setup_nodes(self):
        self.nodes = pygame.sprite.Group()

        for element in encounters.values():
            sprite = Node(element['pos'], element['encounter_graphic'])
            self.nodes.add(sprite)

    def setup_background(self):
        self.background = pygame.sprite.GroupSingle()
        background = Background([0,0],'graphics\Demo.png')
        self.background.add(background)

    def path(self):
        points = [element['pos'] for element in encounters.values()]
        pygame.draw.lines(self.display_surface, 'black', False, points, 5)

    def run(self):
        self.background.draw(self.display_surface)
        self.path()
        self.nodes.draw(self.display_surface)

        #self.player.draw(self.display_surface)

""" class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((20,20))
        self.image.fill('blue')
        self.rect = self.image.get_rect(center = pos) """

"""  def setup_player(self):
        self.player = pygame.sprite.GroupSingle()
        player_sprite = Player(self.nodes.sprites()[self.current_encounter].rect.center)
        self.player.add(player_sprite) """
        