# -*- coding: utf-8 -*-
__author__ = 'fyabc'

# Dependent libraries.
import pygame
import pygame.locals

# Local modules.
from config.gameConfig import FPS_MAIN, BACKGROUND_COLOR, allColors
import GVar
from shift.gameObjects.shiftButton import ShiftTextButton, ShiftButtonPool
from shift.gameObjects.gameText import GameText
from shift.utils import getKeyName, getFont

class Screen:
    """base class for shift game screens.
    """
    def __init__(self, game, surface):
        # [NOTE]: I cannot use 'surface = GVar.mainWindow' here,
        # because the argument must be given after the mainWindow initialized.
        self.game = game
        self.surface = surface

    def initDraw(self):
        self.surface.fill(BACKGROUND_COLOR)
        pygame.display.update()

    def draw(self, *args):
        pass

    def run(self, *args):
        pass

class MenuScreen(Screen):
    """the menu screen that contains some buttons.
    """
    def __init__(self, game, surface):
        super(MenuScreen, self).__init__(game, surface)

        # a list contains inactive things.
        self.inactiveThings = []

        # a group contains all buttons.
        self.buttons = ShiftButtonPool()

        # a dictionary contains all events with those actions
        # and add some common useful actions.
        self.actions = {
            'esc': lambda : self.game.allStates['esc']
        }

        # add some useful common actions.

    def addInactiveThings(self, *things):
        self.inactiveThings += things

    def addButtons(self, *buttons):
        self.buttons.add(*buttons)

    def initDraw(self):
        self.surface.fill(BACKGROUND_COLOR)

        for element in self.inactiveThings:
            element.draw(self.surface)

        for button in self.buttons.sprites():
            button.update(0)
        self.buttons.draw(self.surface)
        pygame.display.update()

    def draw(self):
        self.buttons.clear(self.surface, lambda surf, rect: surf.fill(BACKGROUND_COLOR, rect))
        self.buttons.draw(self.surface)
        pygame.display.update()

    def run(self, *args):
        self.initDraw()

        while True:
            GVar.globalTimer.tick(FPS_MAIN)
            for event in pygame.event.get():
                if event.type == pygame.locals.QUIT:
                    return self.actions['esc']()

                elif event.type == pygame.locals.KEYDOWN:
                    keyName = getKeyName(event.key, GVar.keyMap)
                    if keyName in self.actions:
                        return self.actions[keyName]()

                elif event.type == pygame.locals.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        button = self.buttons.getButtonClicked(event.pos)
                        if button is not None:
                            button.update(1)
                            self.draw()

                elif event.type == pygame.locals.MOUSEBUTTONUP:
                    if event.button == 1:
                        for button in self.buttons.sprites():
                            button.update(0)
                        self.draw()

                        button = self.buttons.getButtonClicked(event.pos)
                        if button is not None:
                            return self.actions[button]()

        return self.game.allStates['default']


class StartGameScreen(MenuScreen):
    def __init__(self, game):
        super(StartGameScreen, self).__init__(game, GVar.mainWindow)

        self.addInactiveThings(
            GameText('Sh', (0.43, 0.2), 60),
            GameText('ift', (0.57, 0.2), 60, allColors['white']),
            GameText('Author: fyabc<www.github.com/fyabc>', (0.5, 0.85), 18), # should it be a button?
        )

        newGameButton = ShiftTextButton('New Game(N)', (0.3, 0.4))
        continueButton = ShiftTextButton('Continue(C)', (0.8, 0.4))
        helpButton = ShiftTextButton('Help(H)', (0.3, 0.65))
        quitButton = ShiftTextButton('Quit(Q)', (0.8, 0.65))

        # add button to group
        self.addButtons(
            newGameButton,
            continueButton,
            helpButton,
            quitButton,
        )

        # some special actions
        def __newGameAction():
            # start a new game will clear your record!
            GVar.unlockedLevelNum = 1
            return self.game.allStates['mainMenuScreen']

        # register actions
        # using callable to do some other actions
        self.actions['newGame'] = __newGameAction
        self.actions['continue'] = lambda : self.game.allStates['mainMenuScreen']
        self.actions['help'] = lambda : self.game.allStates['helpScreen']
        self.actions['quit'] = lambda : self.game.allStates['esc']

        self.actions[newGameButton] = self.actions['newGame']
        self.actions[continueButton] = self.actions['continue']
        self.actions[helpButton] = self.actions['help']
        self.actions[quitButton] = self.actions['quit']

class HelpScreen(MenuScreen):
    def __init__(self, game):
        super(HelpScreen, self).__init__(game, GVar.mainWindow)

        returnButton = ShiftTextButton('Return to main menu(Q)', (0.5, 0.85), font = getFont(25))

        self.addInactiveThings(
            GameText('Help', (0.5, 0.2), 50),
            GameText('Left : run left', (0.5, 0.35), 20),
            GameText('Right : run right', (0.5, 0.45), 20),
            GameText('Space : jump', (0.5, 0.55), 20),
            GameText('Shift : shift to another world', (0.5, 0.65), 20),
        )

        self.addButtons(
            returnButton,
        )

        self.actions['quit'] = lambda : self.game.allStates['startGameScreen']

        self.actions[returnButton] = self.actions['quit']

class MainMenuScreen(MenuScreen):
    def __init__(self, game):
        super(MainMenuScreen, self).__init__(game, GVar.mainWindow)

        self.actions['quit'] = lambda : self.game.allStates['startGameScreen']
