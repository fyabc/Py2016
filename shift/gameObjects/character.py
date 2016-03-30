# -*- coding: utf-8 -*-
__author__ = 'fyabc'

# Dependent libraries.
import pygame

# Local modules.
from config.gameConfig import CELL_SIZE
from shift.utils.basicUtils import invertColor

class Character(pygame.sprite.Sprite):
    """the class of the character of the game.

        The Character object should be contained in a GameMap object.
    """

    allActions = {
        'default'   : 0,
        'jump'      : 1,
        'run'       : 2,
        'shift'     : 3,
    }

    def __init__(self, bgColor, location):
        """
            bgColor : the background color of the character
            location : the initial location of the character (the logical location)

        """
        super(Character, self).__init__()

        # The background color of character.
        self.bgColor = bgColor
        self.location = location

        # self.image = pygame.surface.Surface((30, 30))
        self.image = pygame.image.load('data/images/character.png').convert()
        # self.image.fill(invertColor(self.bgColor))

        self.rect = self.image.get_rect()
        self.rect.topleft = Character.getRealLocation(self.location)

        self.speed = (0, 0)

    @staticmethod
    def getRealLocation(location):
        return CELL_SIZE * location[0], CELL_SIZE * location[1]

    def draw(self, surface):
        # fixme: The pygame.surface.Surface cannot be copied.
        self.image = pygame.surface.Surface((30, 30))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        surface.blit(self.image, self.rect)

    def update(self, action):
        pass
