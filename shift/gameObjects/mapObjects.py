# -*- coding: utf-8 -*-
__author__ = 'fyabc'

# Dependent libraries.
import pygame

# Local modules.
from config.gameConfig import CELL_SIZE, GAME_SCREEN_WIDTH, GAME_SCREEN_HEIGHT, IMAGES_DIR, FPS_MAIN, allColors
from shift.utils.basicUtils import sign, getRealLocation, getLogicLocation, getRotateRealCoor, getFont
from shift.gameObjects.menuText import MenuText


class ShiftSprite(pygame.sprite.Sprite):
    """The abstract base class of shift sprites.
    add draw method and visible property.
    """

    def __init__(self, visible=False):
        super(ShiftSprite, self).__init__()
        self.visible = visible

    def draw(self, surface):
        # fixme: The pygame.surface.Surface object cannot be copied.
        if self.visible:
            surface.blit(self.image, self.rect)


class Character(ShiftSprite):
    """the class of the character of the game.

        The Character object should be contained in a GameMap object.
    """

    ImageWhite = None
    ImageBlack = None

    HorizontalSpeed = 0.116

    # [NOTE]:
    # These speeds have been set carefully.
    # Do NOT change it unless you have test it many times.
    InitJumpSpeed = -0.24
    MaxDownSpeed = +0.2
    G = +0.027  # gravity

    def __init__(self, gameMap, location=(0, 0), visible=True):
        """
            gameMap : the gameMap the character belongs to
            bgColor : the background color of the character (the logical background)
            location : the initial location of the character (the logical location)
        """
        super(Character, self).__init__(visible)

        self.gameMap = gameMap
        self.bgColor = self.gameMap.getCellColor(location)

        self.image = self.getImage(self.bgColor)
        self.rect = self.image.get_rect()
        self.rect.center = getRealLocation(location)

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
        self.state = 0
        self.verticalSpeed = 0

    @staticmethod
    def getImage(bgColor):
        if Character.ImageWhite is None:
            Character.ImageWhite = \
                pygame.image.load(IMAGES_DIR + '/whiteBG/character.png').convert_alpha()
        if Character.ImageBlack is None:
            Character.ImageBlack = \
                pygame.image.load(IMAGES_DIR + '/blackBG/character.png').convert_alpha()

        if bgColor is True:
            return Character.ImageWhite
        else:
            return Character.ImageBlack

    def hitLeft(self, rect):
        logicLocationTL = getLogicLocation(rect.topleft)
        logicLocationBL = getLogicLocation((rect.bottomleft[0], rect.bottomleft[1] - 1))
        return rect.left <= 0 or \
               (self.gameMap.covered(logicLocationTL)) or \
               (self.gameMap.covered(logicLocationBL)) or \
               (self.gameMap.getCellColor(logicLocationTL) != self.bgColor) or \
               (self.gameMap.getCellColor(logicLocationBL) != self.bgColor)

    def hitRight(self, rect):
        logicLocationTR = getLogicLocation(rect.topright)
        logicLocationBR = getLogicLocation((rect.bottomright[0], rect.bottomright[1] - 1))
        return rect.right >= GAME_SCREEN_WIDTH or \
               (self.gameMap.covered(logicLocationTR)) or \
               (self.gameMap.covered(logicLocationBR)) or \
               (self.gameMap.getCellColor(logicLocationTR) != self.bgColor) or \
               (self.gameMap.getCellColor(logicLocationBR) != self.bgColor)

    def hitFloor(self, rect):
        logicLocationBL = getLogicLocation(rect.bottomleft)
        logicLocationBR = getLogicLocation((rect.right - 1, rect.bottom))
        return rect.bottom >= GAME_SCREEN_HEIGHT or \
               (self.gameMap.covered(logicLocationBL)) or \
               (self.gameMap.covered(logicLocationBR)) or \
               (self.gameMap.getCellColor(logicLocationBL) != self.bgColor) or \
               (self.gameMap.getCellColor(logicLocationBR) != self.bgColor)

    def hitCeil(self, rect):
        logicLocationTL = getLogicLocation(rect.topleft)
        logicLocationTR = getLogicLocation((rect.right - 1, rect.top))
        return rect.top <= 0 or \
               (self.gameMap.covered(logicLocationTL)) or \
               (self.gameMap.covered(logicLocationTR)) or \
               (self.gameMap.getCellColor(logicLocationTL) != self.bgColor) or \
               (self.gameMap.getCellColor(logicLocationTR) != self.bgColor)

    def canShift(self):
        logicLocationBL = getLogicLocation(self.rect.bottomleft)
        logicLocationBR = getLogicLocation((self.rect.right - 1, self.rect.bottom))
        return logicLocationBL[1] < GAME_SCREEN_HEIGHT // CELL_SIZE and \
               (not self.gameMap.covered(logicLocationBL)) and \
               (not self.gameMap.covered(logicLocationBR)) and \
               self.gameMap.getCellColor(logicLocationBL) != self.bgColor and \
               self.gameMap.getCellColor(logicLocationBR) != self.bgColor

    def isQuiet(self):
        return self.verticalSpeed == 0

    def update(self, FPS=FPS_MAIN):
        if FPS != 0:
            self.updateCartoon()

        # calculate new horizontal location
        if abs(self.state) == 2:
            self.rect.left += sign(self.state) * self.HorizontalSpeed * FPS

        if self.state != +2:
            if self.hitLeft(self.rect):
                self.rect.left = self.rect.right // CELL_SIZE * CELL_SIZE  # [NOTE]

        if self.state != -2:
            if self.hitRight(self.rect):
                self.rect.right = self.rect.right // CELL_SIZE * CELL_SIZE

        # calculate new vertical location
        self.rect.top += self.verticalSpeed * FPS

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
                self.rect.top = self.rect.bottom // CELL_SIZE * CELL_SIZE  # [NOTE]
            else:
                self.verticalSpeed += self.G

    def updateCartoon(self):
        """this method update the cartoon of the character.
        """
        if abs(self.state) == 1:
            pass
        else:
            pass

        if self.state < 0:
            self.image = pygame.transform.flip(self.getImage(self.bgColor), True, False)
        else:
            self.image = self.getImage(self.bgColor)

    def deathCartoon(self):
        self.visible = False
        self.gameMap.draw(self.gameMap.surface)

        deathImage = pygame.image.load(IMAGES_DIR + '/death_character.png').convert_alpha()
        deathMessage = MenuText(' You lose! ', (0.5, 0.3), 30, allColors['red'], allColors['white'])

        self.gameMap.surface.blit(deathImage, self.rect)
        deathMessage.draw(self.gameMap.surface)

        pygame.display.update()

        pygame.time.delay(1000)

        self.visible = True

    # There are some methods that change the state of character.
    def toLeft(self):
        self.state = -2

    def toLeftStop(self):
        if self.state < 0:
            self.state = -1

    def toRight(self):
        self.state = +2

    def toRightStop(self):
        if self.state > 0:
            self.state = +1

    def toJump(self):
        if self.verticalSpeed == 0:
            self.verticalSpeed = self.InitJumpSpeed

    def rotate(self, angle):
        self.rect.center = getRotateRealCoor(self.rect.center, angle)


class StaticObject(ShiftSprite):
    ImageWhite = {}
    ImageBlack = {}

    def __init__(self, gameMap, imageName, location=(0, 0), angle=0, visible=True):
        super(StaticObject, self).__init__(visible)

        self.gameMap = gameMap
        self.bgColor = self.gameMap.getCellColor(location)

        self.angle = angle

        self.image = self.getImage(self.bgColor, imageName, self.angle)

        self.rect = self.image.get_rect()

        if imageName == 'trap.png':
            if self.angle == 0:
                self.rect.midbottom = (CELL_SIZE * location[0] + CELL_SIZE / 2, CELL_SIZE * (location[1] + 1))
            elif self.angle == 90:
                self.rect.midright = (CELL_SIZE * (location[0] + 1), CELL_SIZE * location[1] + CELL_SIZE / 2)
            elif self.angle == 180:
                self.rect.midtop = (CELL_SIZE * location[0] + CELL_SIZE / 2, CELL_SIZE * location[1])
            elif self.angle == 270:
                self.rect.midleft = (CELL_SIZE * location[0], CELL_SIZE * location[1] + CELL_SIZE / 2)
        else:
            self.rect.center = getRealLocation(location)

    @staticmethod
    def getImage(bgColor, imageName, angle=0):
        if bgColor is True:
            Image = StaticObject.ImageWhite
            if imageName not in Image:
                Image[imageName] = pygame.image.load(IMAGES_DIR + '/whiteBG/' + imageName).convert_alpha()
        else:
            Image = StaticObject.ImageBlack
            if imageName not in Image:
                Image[imageName] = pygame.image.load(IMAGES_DIR + '/blackBG/' + imageName).convert_alpha()
        return pygame.transform.rotate(Image[imageName], angle).convert_alpha()

    def rotate(self, angle):
        self.angle = (self.angle + angle) % 360
        newCenter = getRotateRealCoor(self.rect.center, angle)
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect()
        self.rect.center = newCenter


class Door(StaticObject):
    def __init__(self, gameMap, location=(0, 0), angle=0, visible=True):
        super(Door, self).__init__(gameMap, 'door.png', location, angle, visible)


class Trap(StaticObject):
    def __init__(self, gameMap, location=(0, 0), angle=0, visible=True):
        super(Trap, self).__init__(gameMap, 'trap.png', location, angle, visible)


class Arrow(StaticObject):
    def __init__(self, gameMap, location=(0, 0), angle=0, visible=True):
        super(Arrow, self).__init__(gameMap, 'arrow.png', location, angle, visible)


class Key(StaticObject):
    def __init__(self, gameMap, blockIds, location, angle=0, visible=True):
        super(Key, self).__init__(gameMap, 'key.png', location, angle, visible)

        self.controlBlocks = set()

        for blockId in blockIds:
            self.controlBlocks.add(self.findBlock(blockId))

    def findBlock(self, blockId):
        for block in self.gameMap.blocks:
            if block.Id == blockId:
                return block
        return None


class Lamp(StaticObject):
    def __init__(self, gameMap, mosaicIds, location, angle=0, visible=True):
        super(Lamp, self).__init__(gameMap, 'lamp.png', location, angle, visible)

        self.controlMosaics = set()

        for mosaicId in mosaicIds:
            self.controlMosaics.add(self.findMosaic(mosaicId))

    def findMosaic(self, mosaicId):
        for mosaic in self.gameMap.mosaics:
            if mosaic.Id == mosaicId:
                return mosaic
        return None


class Mosaic(StaticObject):
    def __init__(self, gameMap, Id, location=(0, 0), angle=0, visible=True):
        super(Mosaic, self).__init__(gameMap, 'mosaic.png', location, angle, visible)

        self.Id = Id

    def cover(self, location):
        return self.rect.collidepoint(getRealLocation(location))

    def disappearCartoon(self):
        from config.gameConfig import MAP_ROTATE_SPEED
        import GVar

        self.kill()

        for currentSize in range(self.rect.height, 0, -MAP_ROTATE_SPEED - 2):
            GVar.globalTimer.tick(FPS_MAIN)
            self.gameMap.draw(self.gameMap.surface)

            scaledImage = pygame.transform.scale(self.image, (currentSize, currentSize))
            scaledRect = scaledImage.get_rect()
            scaledRect.center = self.rect.center

            self.gameMap.surface.blit(scaledImage, scaledRect)
            pygame.display.update()


class GameText(StaticObject):
    """The text in the game.
    Note: This class is different from MenuText.
    """
    @staticmethod
    def getImage(bgColor, text, angle=0):
        if bgColor is True:
            Image = getFont(20).render(text, True, allColors['black'], allColors['white'])
        else:
            Image = getFont(20).render(text, True, allColors['white'], allColors['black'])
        return pygame.transform.rotate(Image, angle).convert_alpha()

    def __init__(self, gameMap, text, location=(0, 0), angle=0, visible=True):
        super(GameText, self).__init__(gameMap, text, location, angle, visible)


# Block is a little special, so I do not let it be the subclass of StaticObject.
class Block(ShiftSprite):
    UP = 180
    DOWN = 0
    LEFT = 270
    RIGHT = 90

    Image = None

    @staticmethod
    def getImage():
        if Block.Image is None:
            Block.Image = pygame.image.load(IMAGES_DIR + '/block.png').convert_alpha()
        return Block.Image

    def __init__(self, gameMap, Id, start, length, angle, visible=True):
        """A block is like below:
        . . . . . . . .
        . # # * . . . .
        . . . . . . . .

        :param gameMap: the gameMap of this Block.
        :param start: a pair of (x, y), the location of *.
        :param length: the length of the block, 3 in above.
        :param angle: the direction of the block, left in above.

        after rotate:

        . . . . . . . .
        . . . . * # # .
        . . . . . . . .

        """
        super(Block, self).__init__(visible)
        self.gameMap = gameMap
        self.Id = Id

        self.image = pygame.Surface((1 * CELL_SIZE, length * CELL_SIZE))

        # draw block.
        LINE_WIDTH = 2
        pygame.draw.rect(self.image, allColors['black'], (0, 0, 1 * CELL_SIZE, length * CELL_SIZE), LINE_WIDTH)
        pygame.draw.rect(self.image, allColors['white'],
                         (LINE_WIDTH, LINE_WIDTH, 1 * CELL_SIZE - 2 * LINE_WIDTH, length * CELL_SIZE - 2 * LINE_WIDTH),
                         LINE_WIDTH)

        blockImage = pygame.transform.rotate(Block.getImage(), 90)
        self.image.blit(blockImage, (self.image.get_width() // 2 - blockImage.get_width() // 2,
                                     self.image.get_height() // 2 - blockImage.get_height() // 2,
                                     blockImage.get_width(), blockImage.get_height()))

        self.image = pygame.transform.rotate(self.image, angle).convert_alpha()
        self.rect = self.image.get_rect()

        self.rotateCenter = (0, 0)
        self.angle = angle
        self.setCenter(angle, start)
        self.setRect()

    def setCenter(self, direction, start):
        if direction == Block.UP:
            self.rotateCenter = (start[0] * CELL_SIZE + CELL_SIZE // 2, (start[1] + 1) * CELL_SIZE)
        elif direction == Block.DOWN:
            self.rotateCenter = (start[0] * CELL_SIZE + CELL_SIZE // 2, start[1] * CELL_SIZE)
        elif direction == Block.LEFT:
            self.rotateCenter = ((start[0] + 1) * CELL_SIZE, start[1] * CELL_SIZE + CELL_SIZE // 2)
        elif direction == Block.RIGHT:
            self.rotateCenter = (start[0] * CELL_SIZE, start[1] * CELL_SIZE + CELL_SIZE // 2)

    def setRect(self):
        if self.angle == Block.UP:
            self.rect.midbottom = self.rotateCenter
        elif self.angle == Block.DOWN:
            self.rect.midtop = self.rotateCenter
        elif self.angle == Block.LEFT:
            self.rect.midright = self.rotateCenter
        elif self.angle == Block.RIGHT:
            self.rect.midleft = self.rotateCenter

    def rotateFromKey(self):
        from config.gameConfig import MAP_ROTATE_SPEED
        import GVar
        import math

        self.visible = False

        for currAngle in range(0, 180, MAP_ROTATE_SPEED):
            GVar.globalTimer.tick(FPS_MAIN)
            self.gameMap.draw(self.gameMap.surface)

            rotatedImage = pygame.transform.rotate(self.image, currAngle).convert_alpha()
            radius = max(self.rect.width, self.rect.height) // 2
            realAngle = (self.angle + currAngle - 90) * math.pi / 180
            newCenter = (self.rotateCenter[0] + math.cos(realAngle) * radius,
                         self.rotateCenter[1] - math.sin(realAngle) * radius)
            rotateRect = rotatedImage.get_rect()
            rotateRect.center = newCenter

            self.gameMap.surface.blit(rotatedImage, rotateRect)
            pygame.display.update()

        self.angle = (self.angle + 180) % 360
        self.image = pygame.transform.rotate(self.image, 180)
        self.rect = self.image.get_rect()
        self.setRect()

        self.visible = True

    def rotate(self, angle):
        self.angle = (self.angle + angle) % 360
        self.rotateCenter = getRotateRealCoor(self.rotateCenter, angle)
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect()
        self.setRect()

    def cover(self, location):
        return self.rect.collidepoint(getRealLocation(location))


class ShiftGroup(pygame.sprite.Group):
    """The Group for this game.
    Override method draw to call sprites' draw.
    """
    def __init__(self, *sprites):
        super(ShiftGroup, self).__init__(self, *sprites)

    def __iter__(self):
        return super(ShiftGroup, self).__iter__()

    def draw(self, surface):
        sprites = self.sprites()
        for spr in sprites:
            self.spritedict[spr] = spr.draw(surface)
        self.lostsprites = []
