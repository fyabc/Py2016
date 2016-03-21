# -*- coding: utf-8 -*-
__author__ = 'fyabc'

import pygame
import pygame.locals

SCREEN_SIZE = (640, 480)

def loadKeyMap():
    keyMap = {}

    keyMapFile = open('config/keymap.txt', 'r')

    for line in keyMapFile:
        line = line.strip()
        if len(line) > 0 and line[0] == '#': continue

        words = line.split()
        if len(words) < 2: continue
        if words[0] not in keyMap:
            keyMap[words[0]] = [pygame.locals.__dict__['K_' + words[1]]]
        else:
            keyMap[words[0]].append(pygame.locals.__dict__['K_' + words[1]])

    keyMapFile.close()

    return keyMap

def initGame():
    pygame.init()
    keyMap = loadKeyMap()
    return keyMap

def quitGame():
    pygame.quit()

def main():
    keyMap = initGame()

    mainWindow = pygame.display.set_mode(SCREEN_SIZE)

    running = True

    while running:
        # Step1 : handle events.
        for event in pygame.event.get():
            # print event # FIXME
            if event.type == pygame.locals.QUIT:
                running = False
            elif event.type == pygame.locals.KEYDOWN:
                if event.key in keyMap['esc']:
                    running = False

        # Step2 : calculate game logic.
        # gameLogic(currentEvent)

        # Step3 : render the game surface.
        # renderSurface()

        pygame.display.update()

    quitGame()

if __name__ == '__main__':
    main()