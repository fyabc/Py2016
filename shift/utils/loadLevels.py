# -*- coding: utf-8 -*-
__author__ = 'fyabc'

# Local libraries.
from config.gameConfig import LEVELS_DIR


class LevelData:
    """the class to store level data from file and then be copied to GameMap.
        I use this class because the pygame.surface.Surface cannot be copied.
    """

    def __init__(self, rowNum):
        self.rowNum = rowNum
        self.matrix = [[None for _ in range(rowNum)] for _ in range(rowNum)]
        self.records = {
            'S': [],  # Start
            'D': [],  # Door
            'A': [],  # Arrow
            'T': [],  # Trap
            'K': [],  # Key
            'L': [],  # Lamp
        }

    def getLine(self, line, lineNum):
        for i in range(len(line)):
            self.matrix[lineNum][i] = bool(int(line[i]))

    def addRecord(self, record):
        self.records[record[0]].append([int(record[i]) for i in range(1, len(record))])


def lineStripComment(line, commentStr='#'):
    loc = line.find(commentStr)
    return line[:None if loc == -1 else loc].strip()


def loadLevels(levelsFileName='basic.txt', levelsFolderName=LEVELS_DIR):
    levelsFile = open(levelsFolderName + '/' + levelsFileName, 'r')

    allLines = levelsFile.read().split('\n')

    levelsFile.close()

    allLines = [
        lineStripComment(line)
        for line in allLines if len(lineStripComment(line)) > 0
    ]

    levelNum = int(allLines[0])
    levelMap = [None] * levelNum

    index = 1

    for currentLevel in range(levelNum):
        index += 1  # parse 'begin'
        rowNum = int(allLines[index])
        index += 1

        levelMap[currentLevel] = LevelData(rowNum)

        for i in range(rowNum):
            line = allLines[index].split()
            levelMap[currentLevel].getLine(line, i)
            index += 1

        while allLines[index] != 'end':
            record = allLines[index].split()
            index += 1
            levelMap[currentLevel].addRecord(record)

        index += 1  # parse 'end'

    return levelNum, levelMap
