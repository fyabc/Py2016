# -*- coding: utf-8 -*-

__author__ = 'fyabc'

import pygame
import time


class ShiftTimer:
    """The Timer of this game. Copied from pgu.timer.
    This is a singleton class. Do NOT have two ShiftTimer object at the same time.
    """
    # The game time when one of the clock parameters was last changed
    lastGameTime = None
    # The real time corresponding to the last game time
    lastRealTime = None
    # The game time when 'tick' was last called
    lastTickTime = None

    # Whether the timer is paused or not
    paused = False
    # When this clock was created
    startTime = None
    # The speed which this clock moves at relative to the real clock
    speed = 1

    def __init__(self):
        self.lastGameTime = 0
        self.lastTickTime = 0
        self.lastRealTime = time.time()
        self.startTime = time.time()

    # Set the rate at which this clock ticks relative to the real clock
    def set_speed(self, n):
        assert (n >= 0)
        self.lastGameTime = self.getTime()
        self.lastRealTime = time.time()
        self.speed = n

    # Pause the clock
    def pause(self):
        if not self.paused:
            self.lastGameTime = self.getTime()
            self.lastRealTime = time.time()
            self.paused = True

    # Resume the clock
    def resume(self):
        if self.paused:
            self.paused = False
            self.lastRealTime = time.time()

    def tick(self, fps=0):
        tm = self.getTime()
        dt = tm - self.lastTickTime
        if fps > 0:
            minTime = 1.0 / fps
            if dt < minTime:
                pygame.time.wait(int((minTime - dt) * 1000))
                dt = minTime
        self.lastTickTime = tm
        return dt

    # Returns the amount of 'game time' that has passed since creating
    # the clock (paused time does not count).
    def getTime(self):
        if self.paused:
            return self.lastGameTime
        return self.speed * (time.time() - self.lastRealTime) + self.lastGameTime

    def getRealTime(self):
        return time.time() - self.startTime
