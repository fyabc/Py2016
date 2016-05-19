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
            'S': [],        # Start
            'D': [],        # Door
            'A': [],        # Arrow
            'T': [],        # Trap
            'K': [],        # Key
            'L': [],        # Lamp
            'B': [],        # Block
            'M': [],        # Mosaic
            'Text': [],     # Text
        }

    def getLine(self, line, lineNum):
        for i in range(len(line)):
            self.matrix[lineNum][i] = bool(int(line[i]))

    def addRecord(self, record):
        if record[0] == 'Text':
            self.records[record[0]].append([int(record[i]) for i in range(1, 4)] + [' '.join(record[4:])])
        else:
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

    levelNum = 0
    levelMap = []

    index = 0

    # read map size.
    mapSize = int(allLines[index])
    index += 1

    while index < len(allLines):
        index += 1  # parse 'begin'

        levelMap.append(LevelData(mapSize))

        for i in range(mapSize):
            line = allLines[index].split()
            levelMap[levelNum].getLine(line, i)
            index += 1

        while allLines[index] != 'end':
            record = allLines[index].split()
            index += 1
            levelMap[levelNum].addRecord(record)

        index += 1  # parse 'end'

        levelNum += 1

    return levelNum, levelMap
