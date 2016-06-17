#! /usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'fyabc'

# Standard libraries.
import sys

# Dependent libraries.
import pygame.locals

# Local modules.
from config.gameConfig import *
from shift.utils.loadLevels import loadLevels
from shift.utils.basicUtils import *
from shift.screen import *
from shift.editor.editorScreen import EditorScreen
import GVar


class Game:
    """the class of the main game.
    It is a state machine, the states are screens, and the actions are events.
    """
    # All game states.
    allStates = {
        'esc': -1,
        'default': 0,  # for debug
        'startGameScreen': 1,
        'mainMenuScreen': 2,
        'helpScreen': 3,
        'mainGame': 4,
        'aboutScreen': 5,
        'pauseMenuScreen': 6,
        'editorScreen': 7,
        'selectLevelsScreen': 8,
    }

    def __init__(self):
        initGame()
        self.screens = {}
        self.prevState = None
        self.state = Game.allStates['startGameScreen']
        self.args = []

    def registerScreen(self, stateName, screen):
        self.screens[Game.allStates[stateName]] = screen

    def run(self):
        while True:
            if self.state == Game.allStates['esc']:
                break
            elif self.state == Game.allStates['default']:
                break

            self.prevState, self.state, *self.args =\
                self.state, self.screens[self.state].run(self.prevState, *self.args)

        quitGame()


def main():
    game = Game()

    game.registerScreen('startGameScreen', StartGameScreen(game))
    game.registerScreen('helpScreen', HelpScreen(game))
    game.registerScreen('mainMenuScreen', MainMenuScreen(game))
    game.registerScreen('mainGame', MainGameScreen(game))
    game.registerScreen('editorScreen', EditorScreen(game))
    game.registerScreen('selectLevelsScreen', SelectLevelsScreen(game))

    game.run()


def initGame():
    pygame.init()
    GVar.MainWindow = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption(GAME_NAME)
    GVar.GlobalTimer = pygame.time.Clock()
    GVar.GlobalFont = getFont()

    GVar.KeyMap = loadKeyMap()
    GVar.LevelsName = DEFAULT_LEVELS_NAME
    GVar.LevelsData[DEFAULT_LEVELS_NAME] = loadLevels()
    GVar.unlockedLevelNum = loadRecord()

    # This may be speed up the game or not?
    pygame.event.set_allowed([
        pygame.locals.KEYDOWN,
        pygame.locals.MOUSEBUTTONDOWN,
        pygame.locals.MOUSEBUTTONUP,
    ])


def quitGame():
    # Save all levels records.
    for levelsName in LEVELS_FILE_NAMES:
        levels = GVar.LevelsData.get(levelsName)
        if levels is not None:
            saveRecord(levels.unlockedLevelNum, levelsName)

    pygame.quit()
    print('The game is quited!')
    sys.exit()


if __name__ == '__main__':
    main()
