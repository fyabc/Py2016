# -*- coding: utf-8 -*-
__author__ = 'fyabc'

# Dependent libraries.
from pygame.color import THECOLORS as allColors

GAME_NAME = 'Shift'

SCREEN_WIDTH = 650
SCREEN_HEIGHT = 600
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

GAME_SCREEN_WIDTH = 600
GAME_SCREEN_HEIGHT = 600
GAME_SCREEN_SIZE = (GAME_SCREEN_WIDTH, GAME_SCREEN_HEIGHT)

FPS_START = 50  # The fps of start screen.
FPS_MAIN = 10   # The fps of main game.

CELL_SIZE = 50  # The size of a cell.

assert GAME_SCREEN_SIZE[0] % CELL_SIZE == 0 and GAME_SCREEN_SIZE[1] % CELL_SIZE == 0

BACKGROUND_COLOR = allColors['white']

RECORD_FILE_NAME = 'data/record.txt'
