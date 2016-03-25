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
from shift.gameText import GameText

# All game states.
allStates = {
    'esc' :             -1,
    'default' :         0,      # for debug
    'startGameScreen' : 1,
    'mainMenuScreen' :  2,
    'helpScreen' :      3,
    'mainGame' :        4,
    # 'pauseMenu' :       5,
}

def main():
    initGame()

    state = allStates['startGameScreen']

    while True:
        if state == allStates['esc']:
            state = quitGame()
        elif state == allStates['default']:
            state = quitGame()
        elif state == allStates['startGameScreen']:
            state = showStartGameScreen()
        elif state == allStates['mainMenuScreen']:
            state = showMainMenuScreen()
        elif state == allStates['helpScreen']:
            state = showHelpScreen()
        elif state == allStates['mainGameScreen']:
            state = mainGame()

def initGame():
    global mainWindow, globalTimer, globalFont, keyMap
    global unlockedLevelNum

    pygame.init()
    mainWindow = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption(GAME_NAME)

    globalTimer = pygame.time.Clock()
    globalFont = pygame.font.Font('freesansbold.ttf', 40)

    keyMap = loadKeyMap()

    unlockedLevelNum = loadRecord()

def showStartGameScreen():
    mainWindow.fill(BACKGROUND_COLOR)

    allText = [
        GameText('Sh', (0.5, 0.2), 60),
        GameText('ift', (0.62, 0.2), 60, allColors['white']),
        GameText('New Game(N)', (0.3, 0.5), 40),
        GameText('Help(H)', (0.3, 0.7), 40),
        GameText('Quit(Q)', (0.8, 0.5), 40),
        GameText('About(A)', (0.8, 0.7), 40),
        GameText('Author: fyabc<www.github.com/fyabc>', (0.5, 0.9), 18),
    ]

    for text in allText:
        text.writeToSurface(mainWindow)

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                return allStates['esc']
            elif event.type == pygame.locals.KEYDOWN:
                if event.key in keyMap['esc']:
                    return allStates['esc']
                elif event.key in keyMap['help']:
                    return allStates['helpScreen']

def showMainMenuScreen():
    return allStates['default']

def showHelpScreen():
    mainWindow.fill(BACKGROUND_COLOR)

    allText = [
        GameText('Help', (0.5, 0.3), fontSize=60),
        GameText('Left : run left        Right : run right', (0.5, 0.45), 30),
        GameText('Space : jump        Shift : shift to another world', (0.5, 0.6), 30),
        GameText('Tap Q to return', (0.5, 0.76), 22),
    ]

    for text in allText:
        text.writeToSurface(mainWindow)

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                return allStates['esc']
            elif event.type == pygame.locals.KEYDOWN:
                if event.key in keyMap['esc']:
                    return allStates['startGameScreen']

def mainGame():
    while True:
        return allStates['default']

def showGameOverScreen():
    return allStates['esc']

def quitGame():
    saveRecord(unlockedLevelNum)
    pygame.quit()
    sys.exit()
    return allStates['default']

if __name__ == '__main__':
    main()