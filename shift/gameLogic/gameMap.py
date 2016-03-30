# -*- coding: utf-8 -*-
__author__ = 'fyabc'

# Dependent libraries.
import pygame

# Local modules.
from config.gameConfig import CELL_SIZE, allColors

from shift.gameObjects.character import Character

class GameMapCell:
    """the cell of a map.

        It contains color and other attributes.
    """

    def __init__(self, color):
        # True : white, False : black
        self.color = color

    def getRealColor(self):
        if self.color is True:
            return allColors['white']
        else:
            return allColors['black']

class GameMap:
    """the class of the game map.

        It contains the logical structure of the map, not pixel structure.
        It contains a N * N matrix of GameMapCell.
    """

    def __init__(self, levelData):
        pass

    def draw(self, surface, angle = 0):
        pass
