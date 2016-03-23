# -*- coding: utf-8 -*-
__author__ = 'fyabc'

# Standard libraries.
import sys

# Dependent libraries.
import pygame
import pygame.locals

# Local modules.
from config.gameConfig import *
from shift.utils import loadKeyMap
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

    pygame.init()
    mainWindow = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption(GAME_NAME)

    globalTimer = pygame.time.Clock()
    globalFont = pygame.font.Font('freesansbold.ttf', 40)

    keyMap = loadKeyMap()

def showStartGameScreen():
    mainWindow.fill(BACKGROUND_COLOR)

    choiceText = [
        GameText('Shift', (0.5, 0.2), 60),
        GameText('New Game(N)', (0.3, 0.5), 40),
        GameText('Help(H)', (0.3, 0.7), 40),
        GameText('Quit(Q)', (0.8, 0.5), 40),
        GameText('About(A)', (0.8, 0.7), 40),
        GameText('Author: fyabc<www.github.com/fyabc>', (0.5, 0.9), 18),
    ]

    for text in choiceText:
        text.writeToSurface(mainWindow)

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                return allStates['esc']
            elif event.type == pygame.locals.KEYDOWN:
                if event.key in keyMap['esc']:
                    return allStates['esc']

    return allStates['default']

def showMainMenuScreen():
    return allStates['default']

def showHelpScreen():
    return allStates['default']

def mainGame():
    running = True

    while running:
        # Step1 : handle events.
        for event in pygame.event.get():
            # print(event) # FIXME
            if event.type == pygame.locals.QUIT:
                running = False
            elif event.type == pygame.locals.KEYDOWN:
                # print(event.key) # FIXME
                if event.key in keyMap['esc']:
                    running = False

        # Step2 : calculate game logic.
        # gameLogic(currentEvent)

        # Step3 : render the game surface.
        # renderSurface()

        pygame.display.update()

    return allStates['menuScreen']

def showGameOverScreen():
    return allStates['esc']

def quitGame():
    pygame.quit()
    sys.exit()
    return allStates['default']

if __name__ == '__main__':
    main()