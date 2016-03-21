# -*- coding: utf-8 -*-
__author__ = 'fyabc'

import pygame
import pygame.locals

def initGame():
    pygame.init()

def quitGame():
    pygame.quit()

def main():
    initGame()

    mainWindow = pygame.display.set_mode((640, 480))

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                running = False

    quitGame()

if __name__ == '__main__':
    main()