# -*- coding: utf-8 -*-

__author__ = 'fyabc'

# Standard libraries.
import sys

# Dependent libraries.
import pygame
import pygame.locals

# Local modules.
from config.gameConfig import *
from shift.utils.loadLevels import loadLevels
from shift.utils.basicUtils import *
from shift.screen import *
import GVar

# Some global variables.
mainWindow = None
globalTimer = None
globalFont = None
keyMap = None
unlockedLevelNum = None


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
    }

    def __init__(self):
        initGame()
        self.screens = {}
        self.prevState = None
        self.state = Game.allStates['startGameScreen']

    def registerScreen(self, stateName, screen):
        self.screens[Game.allStates[stateName]] = screen

    def run(self):
        while True:
            if self.state == Game.allStates['esc']:
                break
            elif self.state == Game.allStates['default']:
                break

            self.prevState, self.state = self.state, self.screens[self.state].run(self.prevState)

        quitGame()


def main():
    game = Game()

    game.registerScreen('startGameScreen', StartGameScreen(game))
    game.registerScreen('helpScreen', HelpScreen(game))
    game.registerScreen('mainMenuScreen', MainMenuScreen(game))
    game.registerScreen('mainGame', MainGameScreen(game))

    game.run()


def initGame():
    pygame.init()
    GVar.mainWindow = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption(GAME_NAME)

    GVar.globalTimer = pygame.time.Clock()

    GVar.globalFont = getFont()

    GVar.keyMap = loadKeyMap()

    GVar.totalLevelNum, GVar.levelsData = loadLevels()

    GVar.unlockedLevelNum = loadRecord()

    # This may be speed up the game or not?
    pygame.event.set_blocked(pygame.locals.MOUSEMOTION)


def quitGame():
    saveRecord(GVar.unlockedLevelNum)
    pygame.quit()
    print('The game is quited!')
    sys.exit()


if __name__ == '__main__':
    main()
