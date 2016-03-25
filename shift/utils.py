# -*- coding: utf-8 -*-
__author__ = 'fyabc'

# Dependent libraries.
import pygame.locals

# Local libraries.
from config.gameConfig import RECORD_FILE_NAME

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

def loadLevels(levelsFolderName = 'data/levels/basic'):
    pass

def loadRecord():
    try:
        record = open(RECORD_FILE_NAME, 'r')
        result = int(record.read())
        record.close()
        return result
    except FileNotFoundError:
        return 1
    except ValueError:
        return 1

def saveRecord(unlockedLevelNum):
    record = open(RECORD_FILE_NAME, 'w')
    record.write('%d\n' % unlockedLevelNum)
    record.close()

def invertColor(color):
    if len(color) == 4:
        return 255 - color[0], 255 - color[1], 255 - color[2], color[3]
    else:
        return 255 - color[0], 255 - color[1], 255 - color[2]
