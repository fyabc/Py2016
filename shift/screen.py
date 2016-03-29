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
        # action must accept *args.
        self.actions = {
            'esc': lambda *args: self.game.allStates['esc']
        }

        # add some useful common actions.

    def addInactiveThings(self, *things):
        self.inactiveThings += things

    def addButtons(self, *buttons):
        self.buttons.add(*buttons)

    def addButtonAndAction(self, button, action):
        self.buttons.add(button)
        self.actions[button] = action

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
                    return self.actions['esc'](*args)

                elif event.type == pygame.locals.KEYDOWN:
                    keyName = getKeyName(event.key, GVar.keyMap)
                    if keyName in self.actions:
                        return self.actions[keyName](*args)

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
                            return self.actions[button](*args)

        return self.game.allStates['default']


class StartGameScreen(MenuScreen):
    def __init__(self, game):
        super(StartGameScreen, self).__init__(game, GVar.mainWindow)

        self.addInactiveThings(
            GameText('Sh', (0.43, 0.2), 60),
            GameText('ift', (0.57, 0.2), 60, allColors['white']),
            GameText('Author: fyabc<www.github.com/fyabc>', (0.5, 0.85), 18), # should it be a button?
        )

        # some special actions
        def __newGameAction(*args):
            # start a new game will clear your record!
            GVar.unlockedLevelNum = 1
            return self.game.allStates['mainMenuScreen']

        # register actions
        # using callable to do some other actions
        self.actions['newGame'] = __newGameAction
        self.actions['continue'] = lambda *args : self.game.allStates['mainMenuScreen']
        self.actions['help'] = lambda *args : self.game.allStates['helpScreen']
        self.actions['quit'] = lambda *args : self.game.allStates['esc']

        newGameButton = ShiftTextButton('New Game(N)', (0.3, 0.4))
        continueButton = ShiftTextButton('Continue(C)', (0.8, 0.4))
        helpButton = ShiftTextButton('Help(H)', (0.3, 0.65))
        quitButton = ShiftTextButton('Quit(Q)', (0.8, 0.65))

        # add buttons to group
        self.addButtonAndAction(newGameButton, self.actions['newGame'])
        self.addButtonAndAction(continueButton, self.actions['continue'])
        self.addButtonAndAction(helpButton, self.actions['help'])
        self.addButtonAndAction(quitButton, self.actions['quit'])


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

        self.actions['quit'] = lambda *args : args[0]

        self.addButtonAndAction(returnButton, self.actions['quit'])

class MainMenuScreen(MenuScreen):
    def __init__(self, game):
        super(MainMenuScreen, self).__init__(game, GVar.mainWindow)

        self.actions['quit'] = lambda *args : self.game.allStates['startGameScreen']
        self.actions['help'] = lambda *args : self.game.allStates['helpScreen']

        self.addInactiveThings(
            GameText('Choose a level', (0.5, 0.13), 60, allColors['white'])
        )

        columnNum = 5
        getWidth = lambda num : 0.2 + 0.15 * ((num - 1) % columnNum)
        getHeight = lambda num : 0.32 + 0.15 * ((num - 1) // columnNum)

        # store buttons of all levels.
        # the screen must choose which button to show decided by GVar.unlockedLevelNum,
        # not in __init__ .
        self.levelButtons = [
            ShiftTextButton(
                str(i),
                (getWidth(i), getHeight(i)),
                font = getFont(48),
            )
            for i in range(1, GVar.totalLevelNum + 1)
        ]

        self.returnButton = ShiftTextButton('Return to main menu(Q)', (0.5, 0.91), font = getFont(25))
        
    def run(self, *args):
        # clean all buttons before and then add buttons. The GVar.unlockedLevelNum may changed.
        self.buttons.empty()

        def __levelButtonsAction(levelNum):
            def __action(*args):
                GVar.currentLevelNum = levelNum
                return self.game.allStates['mainMenuScreen']
            return __action

        for i in range(GVar.unlockedLevelNum):
            self.addButtonAndAction(self.levelButtons[i], __levelButtonsAction(i + 1))

        self.addButtonAndAction(self.returnButton, self.actions['quit'])

        return super(MainMenuScreen, self).run(*args)
