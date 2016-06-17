# -*- coding: utf-8 -*-
__author__ = 'fyabc'

# Standard libraries.
import os

# Dependent libraries.
from pygame.color import THECOLORS as AllColors

GAME_NAME = 'Shift'

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

GAME_SCREEN_WIDTH = 600
GAME_SCREEN_HEIGHT = 600
GAME_SCREEN_SIZE = (GAME_SCREEN_WIDTH, GAME_SCREEN_HEIGHT)
CELL_SIZE = 50  # The size of a cell.

FPS_START = 50  # The fps of start screen.
FPS_MAIN = 60   # The fps of main game.

assert GAME_SCREEN_SIZE[0] % CELL_SIZE == 0 and GAME_SCREEN_SIZE[1] % CELL_SIZE == 0

BACKGROUND_COLOR = AllColors['white']

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))

LEVELS_DIR = ROOT_DIR + '/data/levels'
IMAGES_DIR = ROOT_DIR + '/data/images'
KEYMAP_DIR = ROOT_DIR + '/config/keymap.txt'

RECORDS_DIR = ROOT_DIR + '/data/records'

DEFAULT_LEVELS_NAME = 'basic.txt'
LEVELS_FILE_NAMES = os.listdir(LEVELS_DIR)

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
    FONT_NAME = ROOT_DIR + '/data/consolas-yahei.ttf'

# Game Show Configs.
MAP_ROTATE_SPEED = 3

DEFAULT_FONT_SIZE = 40
