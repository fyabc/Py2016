# -*- coding: utf-8 -*-

__author__ = 'fyabc'

# Dependent libraries.
import pygame
import pygame.locals

# Local modules.
from shift.screen import MenuScreen
from shift.gameObjects.menuText import MenuText
from shift.gameObjects.shiftButton import ShiftTextButton

from shift.utils.basicUtils import getFont
import GVar


class EditorScreen(MenuScreen):
    def __init__(self, game):
        super().__init__(game, GVar.MainWindow)

        self.addInactiveThings(
            MenuText('Coming soon...', (0.5, 0.3), 40)
        )

        returnButton = ShiftTextButton('Return to main menu(Q)', (0.5, 0.85), font=getFont(25))

        self.actions['quit'] = lambda *args: self.game.allStates['startGameScreen']

        self.addButtonAndAction(returnButton, self.actions['quit'])

    def run(self, *args):
        return super(EditorScreen, self).run(*args)
