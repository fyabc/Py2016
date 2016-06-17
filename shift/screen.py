# -*- coding: utf-8 -*-
__author__ = 'fyabc'

# Standard libraries.

# Dependent libraries.
import pygame
import pygame.locals

# Local modules.
from config.gameConfig import FPS_MAIN, BACKGROUND_COLOR, AllColors, DEFAULT_LEVELS_NAME, LEVELS_FILE_NAMES
import GVar

from shift.gameObjects.gameMap import GameMap
from shift.gameObjects.shiftButton import ShiftTextButton, ShiftButtonPool
from shift.gameObjects.menuText import MenuText
from shift.utils.basicUtils import getKeyName, getFont
from shift.utils.loadLevels import loadLevels


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
            GVar.GlobalTimer.tick(FPS_MAIN)
            for event in pygame.event.get():
                if event.type == pygame.locals.QUIT:
                    return self.actions['esc'](*args)

                elif event.type == pygame.locals.KEYDOWN:
                    keyName = getKeyName(event.key, GVar.KeyMap)
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
        super(StartGameScreen, self).__init__(game, GVar.MainWindow)

        self.addInactiveThings(
            MenuText('Sh', (0.43, 0.14), 57),
            MenuText('ift', (0.57, 0.14), 57, AllColors['white']),
        )

        # some special actions
        def __newGameAction(*args):
            # start a new game will clear your record!
            GVar.LevelsData[GVar.LevelsName].unlockedLevelNum = (
                1 if GVar.LevelsData[GVar.LevelsName].totalLevelNum >= 1 else 0)
            return self.game.allStates['mainMenuScreen']

        def __openGitHub(*args):
            import webbrowser
            webbrowser.open('http://github.com/fyabc/Py2016')
            return self.game.allStates['startGameScreen']

        # register actions
        # using callable to do some other actions
        self.actions['newGame'] = __newGameAction
        self.actions['continue'] = lambda *args: self.game.allStates['mainMenuScreen']
        self.actions['help'] = lambda *args: self.game.allStates['helpScreen']
        self.actions['quit'] = lambda *args: self.game.allStates['esc']
        self.actions['editor'] = lambda *args: self.game.allStates['editorScreen']

        newGameButton = ShiftTextButton('New Game(N)', (0.25, 0.31))
        continueButton = ShiftTextButton('Continue(C)', (0.75, 0.31))
        editorButton = ShiftTextButton('Edit(E)', (0.25, 0.51))
        helpButton = ShiftTextButton('Help(H)', (0.75, 0.51))
        selectLevelsButton = ShiftTextButton('Select Levels', (0.25, 0.71), font=getFont(35))
        quitButton = ShiftTextButton('Quit(Q)', (0.75, 0.71))
        githubButton = ShiftTextButton('Author: fyabc<www.github.com/fyabc>', (0.5, 0.9), font=getFont(18))

        # add buttons to group
        self.addButtonAndAction(newGameButton, self.actions['newGame'])
        self.addButtonAndAction(continueButton, self.actions['continue'])
        self.addButtonAndAction(helpButton, self.actions['help'])
        self.addButtonAndAction(quitButton, self.actions['quit'])
        self.addButtonAndAction(editorButton, self.actions['editor'])
        self.addButtonAndAction(githubButton, __openGitHub)
        self.addButtonAndAction(selectLevelsButton, lambda *args: self.game.allStates['selectLevelsScreen'])


class HelpScreen(MenuScreen):
    def __init__(self, game):
        super(HelpScreen, self).__init__(game, GVar.MainWindow)

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
        super(MainMenuScreen, self).__init__(game, GVar.MainWindow)

        self.actions['quit'] = lambda *args: self.game.allStates['startGameScreen']
        self.actions['help'] = lambda *args: self.game.allStates['helpScreen']

        self.addInactiveThings(
            MenuText('Choose a level', (0.5, 0.13), 60, AllColors['white'])
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
            for i in range(1, GVar.LevelsData[GVar.LevelsName].totalLevelNum + 1)
        ]

        self.returnButton = ShiftTextButton('Return to main menu(Q)', (0.5, 0.91), font=getFont(25))

    def run(self, *args):
        # clean all buttons before and then add buttons. The GVar.unlockedLevelNum may changed.
        self.buttons.empty()

        levels = GVar.LevelsData[GVar.LevelsName]

        def __levelButtonsAction(levelNum):
            def __action(*args):
                levels.currentLevelNum = levelNum
                return self.game.allStates['mainGame']

            return __action

        for i in range(levels.unlockedLevelNum):
            self.addButtonAndAction(self.levelButtons[i], __levelButtonsAction(i + 1))

        self.addButtonAndAction(self.returnButton, self.actions['quit'])

        return super(MainMenuScreen, self).run(*args)


class SelectLevelsScreen(MenuScreen):
    def __init__(self, game):
        super(SelectLevelsScreen, self).__init__(game, GVar.MainWindow)

        returnButton = ShiftTextButton('Return to main menu(Q)', (0.5, 0.85), font=getFont(25))

        self.actions['quit'] = lambda *args: self.game.allStates['startGameScreen']

        def __changeLevels(newLevelsName):
            def __action(*args):
                GVar.LevelsName = newLevelsName
                if levelsName not in GVar.LevelsData:
                    GVar.LevelsData[levelsName] = loadLevels(levelsName)
                return self.game.allStates['startGameScreen']
            return __action

        self.addButtonAndAction(returnButton, self.actions['quit'])

        for i, levelsName in enumerate(LEVELS_FILE_NAMES):
            row, col = i // 2, i % 2
            self.addButtonAndAction(
                ShiftTextButton(levelsName, position=(0.25 + col * 0.5, 0.2 + row * 0.1), font=getFont(25)),
                __changeLevels(levelsName)
            )


class MainGameScreen(MenuScreen):
    def __init__(self, game):
        super(MainGameScreen, self).__init__(game, GVar.MainWindow)

        self.actions['quit'] = lambda *args: self.game.allStates['mainMenuScreen']
        self.actions['nextGame'] = lambda *args: self.game.allStates['mainGame']
        self.actions['restart'] = self.actions['nextGame']
        self.actions['help'] = lambda *args: self.game.allStates['helpScreen']

    def run(self, *args):
        self.surface.fill(AllColors['white'])

        levels = GVar.LevelsData.get(GVar.LevelsName)
        if levels is None:
            levels = loadLevels(GVar.LevelsName)
            GVar.LevelsData[GVar.LevelsName] = levels
        gameMap = GameMap(levels.maps[levels.currentLevelNum - 1], self.surface)

        gameMap.draw(gameMap.surface)
        pygame.display.update()

        while True:
            GVar.GlobalTimer.tick(FPS_MAIN)
            command = GameMap.allCommands['noOp']

            for event in pygame.event.get():
                if event.type == pygame.locals.QUIT:
                    return self.actions['esc'](*args)

                elif event.type == pygame.locals.KEYDOWN:
                    keyName = getKeyName(event.key, GVar.KeyMap)
                    if keyName in self.actions:
                        # parse common key actions.
                        return self.actions[keyName](*args)
                    else:
                        # parse game key actions.
                        if keyName in ('left', 'right', 'jump', 'shift'):
                            command = GameMap.allCommands[keyName]

                elif event.type == pygame.locals.KEYUP:
                    keyName = getKeyName(event.key, GVar.KeyMap)
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
                if levels.currentLevelNum < levels.unlockedLevelNum:
                    levels.currentLevelNum += 1
                    return self.actions['nextGame'](*args)
                else:
                    if levels.unlockedLevelNum < levels.totalLevelNum:
                        levels.unlockedLevelNum += 1
                        levels.currentLevelNum += 1
                        return self.actions['nextGame'](*args)
                    else:
                        print('I have completed all levels!!!')
                        return self.actions['quit'](*args)
            elif result == -1:  # Lose
                print('I lose!!!')
                return self.actions['nextGame'](*args)

        return self.game.allStates['default']
