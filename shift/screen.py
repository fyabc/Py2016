# -*- coding: utf-8 -*-
__author__ = 'fyabc'

# Standard libraries.

# Dependent libraries.
import pygame
import pygame.locals

# Local modules.
from config.gameConfig import FPS_MAIN, BACKGROUND_COLOR, allColors
import GVar

from shift.gameObjects.gameMap import GameMap
from shift.gameObjects.shiftButton import ShiftTextButton, ShiftButtonPool
from shift.gameObjects.menuText import MenuText
from shift.utils.basicUtils import getKeyName, getFont


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

    def draw(self):
        self.buttons.clear(self.surface, lambda surf, rect: surf.fill(BACKGROUND_COLOR, rect))
        self.buttons.draw(self.surface)

    def run(self, *args):
        self.initDraw()
        pygame.display.update()

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
                            pygame.display.update()

                elif event.type == pygame.locals.MOUSEBUTTONUP:
                    if event.button == 1:
                        for button in self.buttons.sprites():
                            button.update(0)
                        self.draw()
                        pygame.display.update()

                        button = self.buttons.getButtonClicked(event.pos)
                        if button is not None:
                            return self.actions[button](*args)

        return self.game.allStates['default']


class StartGameScreen(MenuScreen):
    def __init__(self, game):
        super(StartGameScreen, self).__init__(game, GVar.mainWindow)

        self.addInactiveThings(
            MenuText('Sh', (0.43, 0.14), 57),
            MenuText('ift', (0.57, 0.14), 57, allColors['white']),
        )

        # some special actions
        def __newGameAction(*args):
            # start a new game will clear your record!
            GVar.unlockedLevelNum = 1
            return self.game.allStates['mainMenuScreen']

        def __openGitHub(*args):
            import webbrowser
            webbrowser.open('github.com/fyabc/Py2016')
            return self.game.allStates['startGameScreen']

        # register actions
        # using callable to do some other actions
        self.actions['newGame'] = __newGameAction
        self.actions['continue'] = lambda *args: self.game.allStates['mainMenuScreen']
        self.actions['help'] = lambda *args: self.game.allStates['helpScreen']
        self.actions['quit'] = lambda *args: self.game.allStates['esc']
        self.actions['editor'] = lambda *args: self.game.allStates['editorScreen']
        self.actions['github'] = __openGitHub

        newGameButton = ShiftTextButton('New Game(N)', (0.25, 0.31))
        continueButton = ShiftTextButton('Continue(C)', (0.75, 0.31))
        editorButton = ShiftTextButton('Edit(E)', (0.25, 0.51))
        helpButton = ShiftTextButton('Help(H)', (0.75, 0.51))
        quitButton = ShiftTextButton('Quit(Q)', (0.25, 0.71))
        githubButton = ShiftTextButton('Author: fyabc<www.github.com/fyabc>', (0.5, 0.9), font=getFont(18))

        # add buttons to group
        self.addButtonAndAction(newGameButton, self.actions['newGame'])
        self.addButtonAndAction(continueButton, self.actions['continue'])
        self.addButtonAndAction(helpButton, self.actions['help'])
        self.addButtonAndAction(quitButton, self.actions['quit'])
        self.addButtonAndAction(editorButton, self.actions['editor'])
        self.addButtonAndAction(githubButton, self.actions['github'])


class HelpScreen(MenuScreen):
    def __init__(self, game):
        super(HelpScreen, self).__init__(game, GVar.mainWindow)

        returnButton = ShiftTextButton('Return to main menu(Q)', (0.5, 0.85), font=getFont(25))

        self.addInactiveThings(
            MenuText('Help', (0.5, 0.2), 50),
            MenuText('Left : run left', (0.5, 0.35), 20),
            MenuText('Right : run right', (0.5, 0.45), 20),
            MenuText('Space : jump', (0.5, 0.55), 20),
            MenuText('Shift : shift to another world', (0.5, 0.65), 20),
        )

        self.actions['quit'] = lambda *args: args[0]

        self.addButtonAndAction(returnButton, self.actions['quit'])


class MainMenuScreen(MenuScreen):
    def __init__(self, game):
        super(MainMenuScreen, self).__init__(game, GVar.mainWindow)

        self.actions['quit'] = lambda *args: self.game.allStates['startGameScreen']
        self.actions['help'] = lambda *args: self.game.allStates['helpScreen']

        self.addInactiveThings(
            MenuText('Choose a level', (0.5, 0.13), 60, allColors['white'])
        )

        columnNum = 5
        getWidth = lambda num: 0.2 + 0.15 * ((num - 1) % columnNum)
        getHeight = lambda num: 0.32 + 0.15 * ((num - 1) // columnNum)

        # store buttons of all levels.
        # the screen must choose which button to show decided by GVar.unlockedLevelNum,
        # not in __init__ .
        self.levelButtons = [
            ShiftTextButton(
                str(i),
                (getWidth(i), getHeight(i)),
                font=getFont(48),
            )
            for i in range(1, GVar.totalLevelNum + 1)
        ]

        self.returnButton = ShiftTextButton('Return to main menu(Q)', (0.5, 0.91), font=getFont(25))

    def run(self, *args):
        # clean all buttons before and then add buttons. The GVar.unlockedLevelNum may changed.
        self.buttons.empty()

        def __levelButtonsAction(levelNum):
            def __action(*args):
                GVar.currentLevelNum = levelNum
                return self.game.allStates['mainGame']

            return __action

        for i in range(GVar.unlockedLevelNum):
            self.addButtonAndAction(self.levelButtons[i], __levelButtonsAction(i + 1))

        self.addButtonAndAction(self.returnButton, self.actions['quit'])

        return super(MainMenuScreen, self).run(*args)


class MainGameScreen(MenuScreen):
    def __init__(self, game):
        super(MainGameScreen, self).__init__(game, GVar.mainWindow)

        self.actions['quit'] = lambda *args: self.game.allStates['mainMenuScreen']
        self.actions['nextGame'] = lambda *args: self.game.allStates['mainGame']
        self.actions['restart'] = self.actions['nextGame']
        self.actions['help'] = lambda *args: self.game.allStates['helpScreen']

    def run(self, *args):
        self.surface.fill(allColors['white'])

        gameMap = GameMap(GVar.levelsData[GVar.currentLevelNum - 1], self.surface)

        gameMap.draw(gameMap.surface)
        pygame.display.update()

        while True:
            GVar.globalTimer.tick(FPS_MAIN)
            command = GameMap.allCommands['noOp']

            for event in pygame.event.get():
                if event.type == pygame.locals.QUIT:
                    return self.actions['esc'](*args)

                elif event.type == pygame.locals.KEYDOWN:
                    keyName = getKeyName(event.key, GVar.keyMap)
                    if keyName in self.actions:
                        # parse common key actions.
                        return self.actions[keyName](*args)
                    else:
                        # parse game key actions.
                        if keyName == 'left':
                            command = GameMap.allCommands['left']
                        elif keyName == 'right':
                            command = GameMap.allCommands['right']
                        elif keyName == 'jump':
                            command = GameMap.allCommands['jump']
                        elif keyName == 'shift':
                            command = GameMap.allCommands['shift']

                elif event.type == pygame.locals.KEYUP:
                    keyName = getKeyName(event.key, GVar.keyMap)
                    if keyName == 'left':
                        command = GameMap.allCommands['leftStop']
                    elif keyName == 'right':
                        command = GameMap.allCommands['rightStop']

            result = gameMap.update(command)
            gameMap.draw(gameMap.surface)
            pygame.display.update()

            # Test results.
            if result == 1:     # Win
                print('I win!!!')
                pygame.time.delay(500)
                if GVar.currentLevelNum < GVar.unlockedLevelNum:
                    GVar.currentLevelNum += 1
                    return self.actions['nextGame'](*args)
                else:
                    if GVar.unlockedLevelNum < GVar.totalLevelNum:
                        GVar.unlockedLevelNum += 1
                        GVar.currentLevelNum += 1
                        return self.actions['nextGame'](*args)
                    else:
                        print('I have completed all levels!!!')
                        return self.actions['quit'](*args)
            elif result == -1:  # Lose
                print('I lose!!!')
                return self.actions['nextGame'](*args)

        return self.game.allStates['default']
