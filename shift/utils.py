# -*- coding: utf-8 -*-
__author__ = 'fyabc'

# Dependent libraries.
import pygame.locals

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
