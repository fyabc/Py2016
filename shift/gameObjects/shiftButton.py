# -*- coding: utf-8 -*-
__author__ = 'fyabc'

# Dependent libraries.
import pygame

# Local modules.
from config.gameConfig import AllColors, GAME_SCREEN_WIDTH, GAME_SCREEN_HEIGHT
from shift.utils.basicUtils import getFont, invertColor


class ShiftTextButton(pygame.sprite.Sprite):
    """the button in my Shift game with a text

    ShiftTextButton(text): return ShiftTextButton

    """

    def __init__(self, text='', position=(0, 0),
                 color=AllColors['white'], textColor=AllColors['black'], font=None):
        """create a new ShiftTextButton

            the size of button is determined by its text.

            text : the text of the button.
            font : the font of the text.
            position : the position of the center of the button. Note that it's relative position.
            color : the color of the button.
            textColor : the color of the text.

        """
        super(ShiftTextButton, self).__init__()
        self.text = text
        self.font = getFont() if font is None else font
        self.color = color
        self.textColor = textColor

        # self.state : the state of the button.
        # 0 : common.
        # 1 : mouse pressed on it.
        # 2 : mouse move on it.
        self.state = 0

        self.image = self.font.render(self.text, True, self.textColor, self.color)
        self.rect = self.image.get_rect()
        self.rect.center = (round(GAME_SCREEN_WIDTH * position[0]),
                            round(GAME_SCREEN_HEIGHT * position[1]))

    def update(self, newState):
        """override this method to update the button
        """
        if self.state == newState:
            return

        self.state = newState
        if newState == 0:
            self.image = self.font.render(self.text, True, self.textColor, self.color)
        elif newState == 1:
            self.image = self.font.render(self.text, True,
                                          invertColor(self.textColor), invertColor(self.color))

    def inRange(self, position):
        return self.rect.collidepoint(position[0], position[1])


class ShiftButtonPool(pygame.sprite.Group):
    def __init__(self):
        super(ShiftButtonPool, self).__init__()

    def getButtonClicked(self, position):
        for button in self.sprites():
            if button.inRange(position):
                return button
        return None
