# -*- coding: utf-8 -*-
import pygame

__author__ = 'fyabc'


class ShiftGroup(pygame.sprite.Group):
    """The Group for this game.
    Override method draw to call sprites' draw.
    """
    def __init__(self, *sprites):
        # Change the sprite dict to OrderedDict,
        # so that the sprites will be drawn in the order when they were added.
        from collections import OrderedDict
        self.spritedict = OrderedDict()
        self.lostsprites = []
        self.add(*sprites)

    def add(self, *sprites):
        super(ShiftGroup, self).add(*sprites)

    def __iter__(self):
        return super(ShiftGroup, self).__iter__()

    def draw(self, surface):
        sprites = self.sprites()
        for spr in sprites:
            self.spritedict[spr] = spr.draw(surface)
        self.lostsprites = []
