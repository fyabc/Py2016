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
FPS_MAIN = 30   # The fps of main game.

CELL_SIZE = 50  # The size of a cell.

assert GAME_SCREEN_SIZE[0] % CELL_SIZE == 0 and GAME_SCREEN_SIZE[1] % CELL_SIZE == 0

BACKGROUND_COLOR = allColors['white']

LEVELS_DIR = 'data/levels'

RECORD_FILE_NAME = 'data/record.txt'

USE_SYSTEM_FONT = False

if USE_SYSTEM_FONT:
    from sys import platform

    if platform == 'win32':
        FONT_NAME = 'C:/Windows/Fonts/consolab.ttf'
    else:
        FONT_NAME = '/usr/share/fonts/truetype/Consolas/consolab.ttf'

    # # set this to get system default font.
    # FONT_NAME = None
else:
    FONT_NAME = 'data/consolas-yahei.ttf'
