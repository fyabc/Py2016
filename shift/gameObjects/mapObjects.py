# -*- coding: utf-8 -*-
__author__ = 'fyabc'

# Dependent libraries.
import pygame

# Local modules.
from config.gameConfig import CELL_SIZE, GAME_SCREEN_WIDTH, GAME_SCREEN_HEIGHT, IMAGES_DIR, FPS_MAIN
from shift.utils.basicUtils import sign, getRealLocation, getLogicLocation, getRotateRealCoor

class Character(pygame.sprite.Sprite):
    """the class of the character of the game.

        The Character object should be contained in a GameMap object.
    """

    ImageWhite = None
    ImageBlack = None

    HorizontalSpeed = 0.1

    InitJumpSpeed = -0.25
    MaxDownSpeed = +0.2
    G = +0.02  # gravity

    def __init__(self, gameMap, location = (0, 0), visible = True):
        """
            gameMap : the gameMap the character belongs to
            bgColor : the background color of the character (the logical background)
            location : the initial location of the character (the logical location)

        """
        super(Character, self).__init__()

        self.gameMap = gameMap
        self.bgColor = self.gameMap.getCellColor(location)

        self.image = self.getImage(self.bgColor)
        self.rect = self.image.get_rect()
        self.rect.center = getRealLocation(location)

        self.visible = visible

        # self.state : the state of the character that determines the image of character
        # and the speed of character.
        # self.state[0] is horizontal, and self.state[1] is vertical.
        # self.state[0] in {
        #     -2 : left running,
        #     -1 : left stopping,
        #     +1 : right stopping,
        #     +2 : right running
        # }
        #
        self.state = [0]
        self.verticalSpeed = 0

    @staticmethod
    def getImage(bgColor):
        if Character.ImageWhite is None:
            Character.ImageWhite =\
                pygame.image.load(IMAGES_DIR + '/whiteBG/character.png').convert_alpha()
        if Character.ImageBlack is None:
            Character.ImageBlack =\
                pygame.image.load(IMAGES_DIR + '/blackBG/character.png').convert_alpha()

        if bgColor is True:
            return Character.ImageWhite
        else:
            return Character.ImageBlack

    def hitLeft(self, rect):
        logicLocationTL = getLogicLocation(rect.topleft)
        logicLocationBL = getLogicLocation((rect.bottomleft[0], rect.bottomleft[1] - 1))
        return rect.left <= 0 or\
               (self.gameMap.getCellColor(logicLocationTL) != self.bgColor) or \
               (self.gameMap.getCellColor(logicLocationBL) != self.bgColor)

    def hitRight(self, rect):
        logicLocationTR = getLogicLocation(rect.topright)
        logicLocationBR = getLogicLocation((rect.bottomright[0], rect.bottomright[1] - 1))
        return rect.right >= GAME_SCREEN_HEIGHT or\
               (self.gameMap.getCellColor(logicLocationTR) != self.bgColor) or \
               (self.gameMap.getCellColor(logicLocationBR) != self.bgColor)

    def hitFloor(self, rect):
        logicLocationBL = getLogicLocation(rect.bottomleft)
        logicLocationBR = getLogicLocation((rect.right - 1, rect.bottom))
        return rect.bottom >= GAME_SCREEN_HEIGHT or\
               (self.gameMap.getCellColor(logicLocationBL) != self.bgColor) or\
               (self.gameMap.getCellColor(logicLocationBR) != self.bgColor)

    def hitCeil(self, rect):
        logicLocationTL = getLogicLocation(rect.topleft)
        logicLocationTR = getLogicLocation((rect.right - 1, rect.top))
        return rect.top <= 0 or\
               (self.gameMap.getCellColor(logicLocationTL) != self.bgColor) or\
               (self.gameMap.getCellColor(logicLocationTR) != self.bgColor)

    def canShift(self):
        logicLocationBL = getLogicLocation(self.rect.bottomleft)
        logicLocationBR = getLogicLocation((self.rect.right - 1, self.rect.bottom))
        return logicLocationBL[1] < GAME_SCREEN_HEIGHT // CELL_SIZE and\
                self.gameMap.getCellColor(logicLocationBL) != self.bgColor and\
                self.gameMap.getCellColor(logicLocationBR) != self.bgColor

    def isQuiet(self):
        return self.verticalSpeed == 0

    def draw(self, surface):
        # fixme: The pygame.surface.Surface object cannot be copied.
        if self.visible:
            surface.blit(self.image, self.rect)

    def update(self, FPS = FPS_MAIN):
        if FPS != 0:
            self.updateCartoon()

        # calculate new horizontal location
        if abs(self.state[0]) == 2:
            self.rect.left += sign(self.state[0]) * self.HorizontalSpeed * FPS

        if self.state[0] != +2:
            if self.hitLeft(self.rect):
                self.rect.left = self.rect.right // CELL_SIZE * CELL_SIZE # [NOTE]

        if self.state[0] != -2:
            if self.hitRight(self.rect):
                self.rect.right = self.rect.right // CELL_SIZE * CELL_SIZE

        # calculate new vertical location
        self.rect.top += int(self.verticalSpeed * FPS)

        if self.verticalSpeed >= 0:
            if self.hitFloor(self.rect):
                self.verticalSpeed = 0
                self.rect.bottom = self.rect.bottom // CELL_SIZE * CELL_SIZE
            else:
                if self.verticalSpeed < self.MaxDownSpeed:
                    self.verticalSpeed += self.G
        else:
            if self.hitCeil(self.rect):
                self.verticalSpeed = 0
                self.rect.top = self.rect.bottom // CELL_SIZE * CELL_SIZE # [NOTE]
            else:
                self.verticalSpeed += self.G

    def updateCartoon(self):
        """this method update the cartoon of the character.
        """
        if abs(self.state[0]) == 1:
            pass
        else:
            pass

        if self.state[0] < 0:
            self.image = pygame.transform.flip(self.getImage(self.bgColor), True, False)
        else:
            self.image = self.getImage(self.bgColor)
        pass

    # There are some help methods below.
    def toLeft(self):
        self.state[0] = -2

    def toLeftStop(self):
        if self.state[0] < 0:
            self.state[0] = -1

    def toRight(self):
        self.state[0] = +2

    def toRightStop(self):
        if self.state[0] > 0:
            self.state[0] = +1

    def toJump(self):
        if self.verticalSpeed == 0:
            self.verticalSpeed = self.InitJumpSpeed

    def rotate(self, angle):
        self.rect.center = getRotateRealCoor(self.rect.center, angle)

class StaticObject(pygame.sprite.Sprite):
    ImageWhite = {}
    ImageBlack = {}

    def __init__(self, gameMap, location=(0, 0), angle = 0, visible=True):
        super(StaticObject, self).__init__()

        self.gameMap = gameMap
        self.bgColor = self.gameMap.getCellColor(location)

        self.visible = visible
        self.angle = angle

        self.image = None
        self.rect = None

    @staticmethod
    def getImage(bgColor, imageName, angle = 0):
        if bgColor is True:
            Image = StaticObject.ImageWhite
            if imageName not in Image:
                Image[imageName] = pygame.image.load(IMAGES_DIR + '/whiteBG/' + imageName).convert_alpha()
        else:
            Image = StaticObject.ImageBlack
            if imageName not in Image:
                Image[imageName] = pygame.image.load(IMAGES_DIR + '/blackBG/' + imageName).convert_alpha()
        return pygame.transform.rotate(Image[imageName], angle)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def rotate(self, angle):
        self.angle = (self.angle + angle) % 360
        newCenter = getRotateRealCoor(self.rect.center, angle)
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect()
        self.rect.center = newCenter

class Door(StaticObject):
    def __init__(self, gameMap, location=(0, 0), angle = 0, visible=True):
        super(Door, self).__init__(gameMap, location, angle, visible)
        self.image = StaticObject.getImage(self.bgColor, 'door.png', self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = getRealLocation(location)

class Trap(StaticObject):
    def __init__(self, gameMap, location=(0, 0), angle = 0, visible=True):
        super(Trap, self).__init__(gameMap, location, angle, visible)
        self.image = StaticObject.getImage(self.bgColor, 'trap.png', self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = getRealLocation(location)

class Arrow(StaticObject):
    def __init__(self, gameMap, location=(0, 0), angle = 0, visible=True):
        super(Arrow, self).__init__(gameMap, location, angle, visible)
        self.image = StaticObject.getImage(self.bgColor, 'arrow.png', self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = getRealLocation(location)

class Key(StaticObject):
    def __init__(self, gameMap, location=(0, 0), angle = 0, visible=True):
        super(Key, self).__init__(gameMap, location, angle, visible)
        self.image = StaticObject.getImage(self.bgColor, 'arrow.png', self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = getRealLocation(location)

class Block(StaticObject):
    def __init__(self, gameMap, location=(0, 0), angle = 0, visible=True):
        super(Block, self).__init__(gameMap, location, angle, visible)
        self.image = StaticObject.getImage(self.bgColor, 'arrow.png', self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = getRealLocation(location)
