# -*- coding: utf-8 -*-
__author__ = 'fyabc'

'''
    Some global variables.
    [NOTE]: This module must be imported as 'import GVar' rather than 'from GVar import *' !
'''

# Some global variables.
mainWindow = None
globalTimer = None
globalFont = None
keyMap = None


class GameRecord:
    def __init__(self, levelsName):
        self.levelsName = levelsName
        self.totalLevelNum = None
        self.unlockedLevelNum = None
        self.currentLevelNum = None

totalLevelNum = None
unlockedLevelNum = None
currentLevelNum = None

levelsName = None
levelsData = None
