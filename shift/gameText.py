# -*- coding: utf-8 -*-
__author__ = 'fyabc'

# Dependent libraries
import pygame

# Local modules
from config.gameConfig import *
from shift.utils import invertColor

class GameText:
    """A help class for text string of game.
    """
    def __init__(self, text = '', location = (0.5, 0.5), fontSize = 40,
                 fgColor = allColors['black'], bgColor = None,
                 fontName = 'freesansbold.ttf'):
        """
        :param text:
        :param location: The location of the center of the text. Note that it's relative position.
        :param fontSize:
        :param fgColor:
        :param bgColor:
        :param fontName:
        :return:
        """
        self.text = text
        self.location = (round(GAME_SCREEN_WIDTH * location[0]),
                         round(GAME_SCREEN_HEIGHT * location[1]))
        self.fontSize = fontSize
        self.fgColor = fgColor
        if bgColor is None:
            self.bgColor = invertColor(self.fgColor)
        else:
            self.bgColor = bgColor
        self.fontName = fontName

    def writeToSurface(self, surface):
        font = pygame.font.Font(self.fontName, self.fontSize)
        text = font.render(self.text, True, self.fgColor, self.bgColor)
        rect = text.get_rect()
        rect.center = self.location

        surface.blit(text, rect)