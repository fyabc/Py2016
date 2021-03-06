# -*- coding: utf-8 -*-
__author__ = 'fyabc'

# Standard libraries.
from copy import deepcopy
from functools import partial

# Dependent libraries.
import pygame

# Local modules.
from config.gameConfig import CELL_SIZE, AllColors, FPS_MAIN, GAME_SCREEN_SIZE
from shift.utils.basicUtils import hitTestByDistance
from shift.utils.timer import ShiftTimer

from shift.gameObjects.mapObjects import Character, Door, Trap, Arrow, Key, Block, Mosaic, Lamp, GameText
from shift.gameObjects.mapGroups import ShiftGroup
import GVar


def getRealColor(logicColor):
    if logicColor is True:
        return AllColors['white']
    else:
        return AllColors['black']


class GameMap:
    """the class of the game map.

        It contains a matrix of map and some Sprites.

        self.matrix : the matrix of True(white) or False(black)
        self.character : a Sprite of game character
        self.door : a Sprite of game destination(a door)
        self.rotateArrows : a list of Sprites of rotate Arrows
        self.traps : a list of Sprites of traps
        self.keys : a list of Sprites of keys and blocks
        self.blocks :
        self.lamps : a list of Sprites of lamps and mosaics
        self.mosaics :
        self.texts : a list of Sprites of texts
    """

    allCommands = {
        'noOp': 0,
        'jump': 1,
        'left': 2,
        'leftStop': 3,
        'right': 4,
        'rightStop': 5,
        'shift': 6,
    }

    def __init__(self, levelData, surface):
        self.surface = surface
        self.rowNum = levelData.rowNum

        self.matrix = deepcopy(levelData.matrix)

        self.character = Character(self, location=levelData.records['S'][0])

        self.door = Door(
            self, location=levelData.records['D'][0][:2],
            angle=levelData.records['D'][0][2]
        )

        self.arrows = ShiftGroup(
            Arrow(self, location=r[:2], angle=r[2])
            for r in levelData.records['A']
        )

        self.traps = ShiftGroup(*[
            Trap(self, location=r[:2], angle=r[2])
            for r in levelData.records['T']
        ])

        self.blocks = ShiftGroup(*[
            Block(self, Id=r[4], start=r[:2], length=r[2], angle=r[3])
            for r in levelData.records['B']
        ])

        # keys must be initialized after blocks
        self.keys = ShiftGroup(
            Key(self, location=r[:2], blockIds=r[2:], angle=0)
            for r in levelData.records['K']
        )

        self.mosaics = ShiftGroup(
            Mosaic(self, Id=r[2], location=r[:2])
            for r in levelData.records['M']
        )

        # lamps must be initialized after mosaics
        self.lamps = ShiftGroup(
            Lamp(self, mosaicIds=r[2:], location=r[:2])
            for r in levelData.records['L']
        )

        self.texts = ShiftGroup(
            GameText(self, text=r[3], location=r[:2], angle=r[2])
            for r in levelData.records['Text']
        )

        self.staticObjects = ShiftGroup(
            self.texts, self.door, self.arrows, self.keys, self.mosaics, self.lamps, self.traps, self.blocks,
        )

        # Start the timer of this game.
        self.timer = ShiftTimer()

    def getRotateCoordinate(self, coordinate, angle):
        if angle == 0:
            return coordinate
        elif angle == 90:
            return coordinate[1], self.rowNum - 1 - coordinate[0]
        elif angle == 180:
            return self.rowNum - 1 - coordinate[0], self.rowNum - 1 - coordinate[1]
        elif angle == 270:
            return self.rowNum - 1 - coordinate[1], coordinate[0]
        return coordinate

    def getCellColor(self, location):
        return self.matrix[location[1]][location[0]]

    def drawBackground(self, surface):
        for h in range(len(self.matrix)):
            for w in range(len(self.matrix[h])):
                surface.fill(getRealColor(self.matrix[h][w]),
                             pygame.Rect(w * CELL_SIZE, h * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                             )
        self.staticObjects.draw(surface)

    def draw(self, surface):
        self.drawBackground(surface)
        self.character.draw(surface)

    def win(self):
        return self.character.isQuiet() and self.door.angle == 0 and \
               pygame.sprite.collide_rect_ratio(0.4)(self.character, self.door)

    def lose(self):
        return pygame.sprite.spritecollideany(self.character, self.traps,
                                              collided=partial(hitTestByDistance, ratio=0.5)) is not None

    def update(self, command):
        """Update the GameMap,
        such as change the location of character, handle hit objects, etc.
        Note: This method does NOT call pygame.display.update.
        """
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
                self.shiftMap()

        # Then special events below.

        # update the character here.
        self.character.update()

        # hitArrow here.
        hitArrow = pygame.sprite.spritecollideany(self.character, self.arrows,
                                                  collided=partial(hitTestByDistance, ratio=0.4))
        if hitArrow is not None:
            angle = -hitArrow.angle % 360
            if angle != 0:
                self.rotateCartoon(angle)
                self.rotateMap(angle)
                self.character.verticalSpeed = 0  # after rotating, do not jump.
                # self.character.toStop()

        # hitKey here.
        hitKey = pygame.sprite.spritecollideany(self.character, self.keys,
                                                collided=partial(hitTestByDistance, ratio=0.55))
        if hitKey is not None:
            hitKey.visible = False
            for block in hitKey.controlBlocks:
                block.rotateFromKey()
            hitKey.kill()

        # hitLamp here.
        hitLamp = pygame.sprite.spritecollideany(self.character, self.lamps,
                                                 collided=partial(hitTestByDistance, ratio=0.55))
        if hitLamp is not None:
            hitLamp.visible = False
            for mosaic in hitLamp.controlMosaics:
                mosaic.disappearCartoon()
                mosaic.kill()
            hitLamp.kill()

        if self.win():
            return 1
        elif self.lose():
            self.character.deathCartoon()
            return -1

        return 0

    def rotateCartoon(self, angle, origSurface=None):
        from config.gameConfig import MAP_ROTATE_SPEED
        if angle > 180:
            angle -= 360
            AnglePerStep = -MAP_ROTATE_SPEED
        else:
            AnglePerStep = MAP_ROTATE_SPEED

        if origSurface is None:
            origSurface = pygame.Surface(GAME_SCREEN_SIZE)
            self.draw(origSurface)

        for currAngle in range(0, angle, AnglePerStep):
            GVar.GlobalTimer.tick(FPS_MAIN)
            self.surface.fill(AllColors['white'])

            rotateSurface = pygame.transform.rotate(origSurface, currAngle).convert_alpha()
            rotateRect = rotateSurface.get_rect()
            rotateRect.center = self.surface.get_rect().center

            self.surface.blit(rotateSurface, rotateRect)

            pygame.display.update()

    def covered(self, location):
        """test if the input logic location is covered by any block or mosaic.
        """
        for block in self.blocks:
            if block.cover(location):
                return True
        for mosaic in self.mosaics:
            if mosaic.cover(location):
                return True
        return False

    def shiftMap(self):
        # Update character image and location.
        self.character.bgColor = not self.character.bgColor
        self.character.image = self.character.getImage(self.character.bgColor)

        # flip the image when rotating
        self.character.image = pygame.transform.flip(self.character.image, False, True)
        self.character.rect.top += CELL_SIZE

        # the cartoon of the flipping of character should be here.
        # todo

        self.rotateCartoon(180)
        self.rotateMap(180)
        self.character.toStop()  # after shifting, do not move.

        # reset the image after rotating
        self.character.image = pygame.transform.flip(self.character.image, False, True)

    def rotateMap(self, angle):
        """rotate the logic structure of the map.
        """
        newMatrix = [[None for _ in range(self.rowNum)] for _ in range(self.rowNum)]
        for y in range(self.rowNum):
            for x in range(self.rowNum):
                newCoor = self.getRotateCoordinate((x, y), angle)
                newMatrix[newCoor[1]][newCoor[0]] = self.matrix[y][x]

        self.matrix = newMatrix

        self.character.rotate(angle)
        for obj in self.staticObjects:
            obj.rotate(angle)
