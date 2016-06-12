# -*- coding: utf-8 -*-
__author__ = 'fyabc'

# Standard libraries.
from collections import defaultdict

# Dependent libraries.
import pygame.font
import pygame.locals

# Local libraries.
from config.gameConfig import KEYMAP_DIR, RECORD_FILE_NAME, FONT_NAME, CELL_SIZE, GAME_SCREEN_SIZE


def lineStripComment(line, commentStr='#'):
    loc = line.find(commentStr)
    return line[:None if loc == -1 else loc].strip()


def loadKeyMap():
    keyMap = defaultdict(set)

    keyMapFile = open(KEYMAP_DIR, 'r')

    for line in keyMapFile:
        line = line.strip()
        if len(line) > 0 and line[0] == '#':
            continue

        words = line.split()
        if len(words) < 2:
            continue
        keyMap[words[0]].add(pygame.locals.__dict__['K_' + words[1]])

    keyMapFile.close()

    return keyMap


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


def getFont(fontSize=40, fontName=FONT_NAME):
    return pygame.font.Font(fontName, fontSize)


def getKeyName(key, keyMap):
    for keyName in keyMap:
        if key in keyMap[keyName]:
            return keyName
    return None


def sign(x):
    if x > 0:
        return +1
    elif x < 0:
        return -1
    else:
        return 0


def getRealLocation(location):
    # [NOTE]: return the center location of this cell.
    return CELL_SIZE * location[0] + CELL_SIZE / 2, \
           CELL_SIZE * location[1] + CELL_SIZE / 2


def getLogicLocation(location):
    # fixme: the logic location of bottom and right often +1.
    return location[0] // CELL_SIZE, location[1] // CELL_SIZE


def getRotateRealCoor(coor, angle):
    if angle == 0:
        return coor
    elif angle == 90:
        return coor[1], GAME_SCREEN_SIZE[1] - coor[0]
    elif angle == 180:
        return GAME_SCREEN_SIZE[0] - coor[0], GAME_SCREEN_SIZE[1] - coor[1]
    elif angle == 270:
        return GAME_SCREEN_SIZE[0] - coor[1], coor[0]
    return coor


def distance(loc1, loc2):
    from math import sqrt
    return sqrt((loc1[0] - loc2[0]) ** 2 + (loc1[1] - loc2[1]) ** 2)


def hitTestByDistance(s1, s2, ratio=0.4):
    return distance(s1.rect.center, s2.rect.center) <= CELL_SIZE * ratio
