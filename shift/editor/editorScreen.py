# -*- coding: utf-8 -*-

__author__ = 'fyabc'

# Dependent libraries.
import pygame
import pygame.locals

# Local modules.
from shift.screen import Screen, MenuScreen
import GVar


class EditorScreen(MenuScreen):
    def __init__(self, game):
        super().__init__(game, GVar.mainWindow)

        self.actions['quit'] = lambda *args: self.game.allStates['startGameScreen']

    def run(self, *args):
        return super(EditorScreen, self).run(*args)
