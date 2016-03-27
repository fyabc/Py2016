# -*- coding: utf-8 -*-

__author__ = 'fyabc'

# Standard libraries.
import sys

# Dependent libraries.
import pygame
import pygame.locals

# Local modules.
from config.gameConfig import *
from shift.utils import *
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
        'aboutScreen' : 5,
        'pauseMenu' : 6,
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

            self.prevState = self.state
            self.state = self.screens[self.state].run(self.prevState)

        quitGame()

def main():
    game = Game()

    game.registerScreen('startGameScreen', StartGameScreen(game))
    game.registerScreen('helpScreen', HelpScreen(game))
    game.registerScreen('mainMenuScreen', MainMenuScreen(game))

    game.run()

def initGame():
    pygame.init()
    GVar.mainWindow = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption(GAME_NAME)

    GVar.globalTimer = pygame.time.Clock()

    GVar.globalFont = getFont()

    GVar.keyMap = loadKeyMap()

    GVar.unlockedLevelNum = loadRecord()

# def showStartGameScreen():
#     mainWindow.fill(BACKGROUND_COLOR)
#
#     allText = [
#         GameText('Sh', (0.43, 0.2), 60),
#         GameText('ift', (0.57, 0.2), 60, allColors['white']),
#         GameText('New Game(N)', (0.3, 0.5), 40),
#         GameText('Help(H)', (0.3, 0.7), 40),
#         GameText('Quit(Q)', (0.8, 0.5), 40),
#         GameText('About(A)', (0.8, 0.7), 40),
#         GameText('Author: fyabc<www.github.com/fyabc>', (0.5, 0.9), 18),
#     ]
#
#     for text in allText:
#         text.writeToSurface(mainWindow)
#
#     pygame.display.update()
#
#     while True:
#         for event in pygame.event.get():
#             if event.type == pygame.locals.QUIT:
#                 return GVars.allStates['esc']
#             elif event.type == pygame.locals.KEYDOWN:
#                 if event.key in keyMap['esc']:
#                     return GVars.allStates['esc']
#                 elif event.key in keyMap['help']:
#                     return GVars.allStates['helpScreen']
#
# def showMainMenuScreen():
#     return GVars.allStates['default']
#
# def showHelpScreen():
#     mainWindow.fill(BACKGROUND_COLOR)
#
#     allText = [
#         GameText('Help', (0.5, 0.3), fontSize=60),
#         GameText('Left : run left    Right : run right', (0.5, 0.45), 18),
#         GameText('Space : jump    Shift : shift to another world', (0.55, 0.6), 18),
#         GameText('Tap Q to return', (0.5, 0.76), 22),
#     ]
#
#     for text in allText:
#         text.writeToSurface(mainWindow)
#
#     pygame.display.update()
#
#     while True:
#         for event in pygame.event.get():
#             if event.type == pygame.locals.QUIT:
#                 return GVars.allStates['esc']
#             elif event.type == pygame.locals.KEYDOWN:
#                 if event.key in keyMap['esc']:
#                     return GVars.allStates['startGameScreen']
#
# def mainGame():
#     while True:
#         return GVars.allStates['default']
#
# def showGameOverScreen():
#     return GVars.allStates['esc']

def quitGame():
    saveRecord(GVar.unlockedLevelNum)
    pygame.quit()
    print('The game is quited!')
    sys.exit()

if __name__ == '__main__':
    main()