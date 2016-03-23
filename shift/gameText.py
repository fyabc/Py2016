# -*- coding: utf-8 -*-
__author__ = 'fyabc'

# Dependent libraries
import pygame

# Local modules
from config.gameConfig import *

class GameText:
    """A help class for text string of game.
    """
    def __init__(self, text = '', location = None, fontSize = 40):
        """
        :param text:
        :param location: The location of the canter of the text. Note that it's relative position.
        :param font:
        :return:
        """
        font = pygame.font.Font('freesansbold.ttf', fontSize)

        self.text = font.render(text, True, allColors['black'])

        self.rect = self.text.get_rect()

        if location is not None:
            self.rect.center = (round(GAME_SCREEN_WIDTH * location[0]),
                                round(GAME_SCREEN_HEIGHT * location[1]))

    def writeToSurface(self, surface):
        surface.blit(self.text, self.rect)