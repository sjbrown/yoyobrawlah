#! /usr/bin/python

import events
from util import clamp, outOfBounds, Facing, Rect

class Walker(object):
    '''A game object like an avatar or enemy that walks on the ground'''
    def __init__(self):
        self.rect = Rect(0,0,70,80) #this is the *logical* rect
        self.facing = Facing.right
        self.yFacing = Facing.up
        self.velocity = [0,0]
        self.xFriction = 1
        self.yFriction = 2
        self.xAccel = 1
        self.yAccel = 1
        self.xMax = 8
        self.xMin = -8
        self.yMax = 4
        self.yMin = -4
        self.walkMask = None #level will set this
        self.triggerZones = None #level will set this

    def walkTo(self, oldRect, hPower, vPower):
        self.velocity[0] = clamp(self.velocity[0]+hPower, self.xMin, self.xMax)
        self.velocity[1] = clamp(self.velocity[1]+vPower, self.yMin, self.yMax)

        newRect = oldRect.move(*self.velocity)

        oob = outOfBounds(self.walkMask, self.feetPos, newRect.midtop)

        if oob:
            #TODO: more precise
            return oldRect
        else:
            return newRect

    def setCenter(self, xy):
        self.rect.center = xy
    def getCenter(self):
        return self.rect.center
    center = property(getCenter, setCenter)

    def setX(self, x):
        self.rect.x = x
    def getX(self):
        return self.rect.x
    x = property(getX, setX)

    def setY(self, y):
        self.rect.y = y
    def getY(self):
        return self.rect.y
    y = property(getY, setY)

    def setFeetPos(self, val):
        self.rect.midtop = val # note Pygame rects are non-cartesian
    def getFeetPos(self):
        return self.rect.midtop
    feetPos = property(getFeetPos, setFeetPos)
