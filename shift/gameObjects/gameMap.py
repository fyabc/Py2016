# -*- coding: utf-8 -*-
__author__ = 'fyabc'

# Standard libraries.
from copy import deepcopy

# Dependent libraries.
import pygame

# Local modules.
from config.gameConfig import CELL_SIZE, allColors, FPS_MAIN, GAME_SCREEN_SIZE
from shift.utils.basicUtils import hitSprite

from shift.gameObjects.mapObjects import Character, Door, Trap, Arrow
import GVar

def getRealColor(logicColor):
    if logicColor is True:
        return allColors['white']
    else:
        return allColors['black']

class GameMap:
    """the class of the game map.

        It contains a matrix of map and some Sprites.

        self.matrix : the matrix of True(white) or False(black)
        self.character : a Sprite of game character
        self.door : a Sprite of game destination(a door)
        self.rotateArrows : a list of Sprites of rotate Arrows
        self.keys : a list of Sprites of keys and blocks
        self.lamps : a list of Sprites of lamps and mosaics
        self.traps : a list of Sprites of traps
    """

    allCommands = {
        'noOp'      : 0,
        'jump'      : 1,
        'left'      : 2,
        'leftStop'  : 3,
        'right'     : 4,
        'rightStop' : 5,
        'shift'     : 6,
    }

    def __init__(self, levelData, surface):
        self.surface = surface
        self.direction = 0
        self.rawNum = levelData.rawNum
        self.matrix = deepcopy(levelData.matrix)
        self.character = Character(self, location = levelData.records['S'][0])
        self.door = Door(self, location = levelData.records['D'][0][:2], angle = levelData.records['D'][0][2])
        self.arrows = pygame.sprite.Group(
            Arrow(self, location = r[:2], angle = r[2])
            for r in levelData.records['A']
        )
        self.keys = pygame.sprite.Group()
        self.lamps = pygame.sprite.Group()
        self.traps = pygame.sprite.Group(*[
            Trap(self, location = r[:2], angle = r[2])
            for r in levelData.records['T']
        ])

    def getRotateCoordinate(self, coor, angle):
        if angle == 0:
            return coor
        elif angle == 90:
            return coor[1], self.rawNum - 1 - coor[0]
        elif angle == 180:
            return self.rawNum - 1 - coor[0], self.rawNum - 1 - coor[1]
        elif angle == 270:
            return self.rawNum - 1 - coor[1], coor[0]
        return coor

    def getCellColor(self, location):
        return self.matrix[location[1]][location[0]]

    def drawBackground(self, surface):
        for h in range(len(self.matrix)):
            for w in range(len(self.matrix[h])):
                surface.fill(getRealColor(self.matrix[h][w]),
                             pygame.Rect(w * CELL_SIZE, h * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                             )
        self.door.draw(surface)
        for arrow in self.arrows: arrow.draw(surface)
        for trap in self.traps: trap.draw(surface)

    def draw(self, surface):
        self.drawBackground(surface)
        self.character.draw(surface)

    def win(self):
        return self.character.isQuiet() and self.door.angle == 0 and\
               pygame.sprite.collide_rect(self.character, self.door)

    def lose(self):
        return pygame.sprite.spritecollideany(self.character, self.traps) is not None

    def update(self, command):
        if command == GameMap.allCommands['left']:
            self.character.toLeft()
        elif command == GameMap.allCommands['right']:
            self.character.toRight()
        elif command == GameMap.allCommands['leftStop']:
            self.character.toLeftStop()
        elif command == GameMap.allCommands['rightStop']:
            self.character.toRightStop()
        elif command == GameMap.allCommands['jump']:
            self.character.toJump()
        elif command == GameMap.allCommands['shift']:
            if self.character.canShift():
                # Update character image and location.
                self.character.bgColor = not self.character.bgColor
                self.character.image = self.character.getImage(self.character.bgColor)

                # flip the image when rotating
                self.character.image = pygame.transform.flip(self.character.image, True, True)

                self.character.rect.top += CELL_SIZE

                self.rotateCartoon(180)
                self.rotateMap(180)

                # reset the image after rotating
                self.character.image = pygame.transform.flip(self.character.image, False, True)

        self.character.update()

        hitArrow = pygame.sprite.spritecollideany(self.character, self.arrows,
            collided = hitSprite)
        if hitArrow is not None:
            angle = -hitArrow.angle % 360
            if angle != 0:
                self.rotateCartoon(angle)
                self.rotateMap(angle)

        if self.win():
            return 1
        elif self.lose():
            return -1

        return 0

    def rotateCartoon(self, angle, origSurface = None):
        if angle > 180:
            angle -= 360
            AnglePerStep = -3
        else:
            AnglePerStep = 3

        if origSurface is None:
            origSurface = pygame.Surface(GAME_SCREEN_SIZE)
            self.draw(origSurface)

        for currAngle in range(0, angle, AnglePerStep):
            GVar.globalTimer.tick(FPS_MAIN)
            self.surface.fill(allColors['white'])

            rotateSurface = pygame.transform.rotate(origSurface, currAngle).convert_alpha()
            rotateRect = rotateSurface.get_rect()
            rotateRect.center = self.surface.get_rect().center

            self.surface.blit(rotateSurface, rotateRect)

            pygame.display.update()

    def rotateMap(self, angle):
        newMatrix = [[None for _ in range(self.rawNum)] for _ in range(self.rawNum)]
        for y in range(self.rawNum):
            for x in range(self.rawNum):
                newCoor = self.getRotateCoordinate((x, y), angle)
                newMatrix[newCoor[1]][newCoor[0]] = self.matrix[y][x]

        self.matrix = newMatrix

        self.character.rotate(angle)
        self.door.rotate(angle)
        for arrow in self.arrows:
            arrow.rotate(angle)
        for trap in self.traps:
            trap.rotate(angle)
