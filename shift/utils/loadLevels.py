# -*- coding: utf-8 -*-
__author__ = 'fyabc'

# Standard libraries.
from collections import defaultdict

# Local libraries.
from config.gameConfig import LEVELS_DIR, DEFAULT_LEVELS_NAME
from shift.utils.basicUtils import loadRecord
import GVar


class MapData:
    """the class to store map data of one level from file and then be copied to GameMap.
        I use this class because the pygame.surface.Surface cannot be copied.

        record types:
        [matrix] the 0-1 matrix.
        'S':    Start
        'D':    Door
        'A':    Arrow
        'T':    Trap
        'K':    Key
        'L':    Lamp
        'B':    Block
        'M':    Mosaic
        'Text': Text
    """

    def __init__(self, rowNum):
        self.rowNum = rowNum
        self.matrix = [[None for _ in range(rowNum)] for _ in range(rowNum)]
        self.records = defaultdict(list)

    def getLine(self, line, lineNum):
        for i in range(len(line)):
            self.matrix[lineNum][i] = bool(int(line[i]))

    def addRecord(self, record):
        if record[0] == 'Text':
            self.records[record[0]].append([int(record[i]) for i in range(1, 4)] + [' '.join(record[4:])])
        else:
            self.records[record[0]].append([int(record[i]) for i in range(1, len(record))])


class Levels:
    def __init__(self, name):
        self.name = name
        self.maps = []
        self.totalLevelNum = None
        self.currentLevelNum = None
        self.unlockedLevelNum = loadRecord(name)


def lineStripComment(line, commentStr='#'):
    loc = line.find(commentStr)
    return line[:None if loc == -1 else loc].strip()


def loadLevels(levelsFileName=DEFAULT_LEVELS_NAME, levelsFolderName=LEVELS_DIR):
    levelsFile = open(levelsFolderName + '/' + levelsFileName, 'r')

    allLines = levelsFile.read().split('\n')

    levelsFile.close()

    allLines = [lineStripComment(line) for line in allLines if len(lineStripComment(line)) > 0]

    levels = Levels(GVar.LevelsName)

    index = 0

    # read map size.
    mapSize = int(allLines[index])
    index += 1

    while index < len(allLines):
        index += 1  # parse 'begin'

        levels.maps.append(MapData(mapSize))

        for i in range(mapSize):
            line = allLines[index].split()
            levels.maps[-1].getLine(line, i)
            index += 1

        while allLines[index] != 'end':
            record = allLines[index].split()
            index += 1
            levels.maps[-1].addRecord(record)

        index += 1  # parse 'end'

    levels.totalLevelNum = len(levels.maps)

    return levels
