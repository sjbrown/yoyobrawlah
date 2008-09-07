#! /usr/bin/python

import pygame
import pyglet
import events
from util import clamp

def outOfBounds(mask, pos1, pos2):
        #oldMaskPixel = maskImg.get_region(pos1[0], pos1[1], 1,1)
        #newMaskPixel = maskImg.get_region(pos2[0], pos2[1], 1,1)
        #format = 'R' #only care about the red
        #pitch = maskImg.width * len(format)
        #newRedValue = newMaskPixel.get_data(format, pitch)[0]
        oldRedValue = mask[pos1]
        newRedValue = mask[pos2]
        return oldRedValue != newRedValue
        #print 'old', oldMaskPixel.get_data(format, pitch)[0] == '\x00'
        #print 'new', newMaskPixel.get_data(format, pitch)[0]
        #print 'new', newMaskPixel.get_data(format, pitch)[0] == '\x00'

#make a Rect that obeys pyglet's cartesian origin
class Rect(pygame.Rect):
    def move_ip(self, x, y):
        return pygame.Rect.move_ip(self, x,-y)
    def move(self, x, y):
        return pygame.Rect.move(self, x,-y)

class Facing:
    left = -1
    right = 1
    up = 1
    down = -1

class State:
    normal = 'normal'

def GetFriction(orig, absFriction):
    '''Return the friction.  Makes sure that the friction opposes the orig'''
    if abs(orig) < 1:
        return 0
    elif orig < 0:
        return +absFriction
    elif orig > 0:
        return -absFriction

class AvatarAttack(object):
    '''Abstract class for the various avatar attacks'''

    def GetVictimsAndAmount(self, origin):
        '''returns a list of pairs (victim, amount of attack power)'''
        raise NotImplementedError('abstract class')

    def GetVictimsInRange(self, origin):
        '''given an origin point, return a list of all victims that this
        attack would hit
        '''
        raise NotImplementedError('abstract class')
        

class Avatar(object):
    '''This is the duder that a player controls'''

    def __init__(self):
        self.rect = Rect(0,0,70,80) #this is the *logical* rect
        self.health = 10
        self.energy = 10
        self.state = State.normal
        self.upPressed = False
        self.rightPressed = False
        self.downPressed = False
        self.leftPressed = False
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

    def Hurt(self, amount):
        self.health -= amount
        if self.health > 0:
            events.fire('AvatarHurt', self)
        else:
            events.fire('AvatarDeath', self)

    def Attack(self, attack):
        center = self.rect.center
        for victim, attackAmt in attack.GetVictimsAndAmount(self.center):
            power = attackAmt*self.energy
            victim.Hurt(power)

    def On_UpKeyPress(self):
        self.yFacing = Facing.up
        self.upPressed = True
    def On_UpKeyRelease(self):
        self.upPressed = False
    def On_RightKeyPress(self):
        self.facing = Facing.right
        print 'right press'
        self.rightPressed = True
    def On_RightKeyRelease(self):
        print 'right release'
        self.rightPressed = False
    def On_DownKeyPress(self):
        self.yFacing = Facing.down
        self.downPressed = True
    def On_DownKeyRelease(self):
        self.downPressed = False
    def On_LeftKeyPress(self):
        self.facing = Facing.left
        self.leftPressed = True
    def On_LeftKeyRelease(self):
        self.leftPressed = False
            
    def update(self, timeChange=None):
        oldRect = self.rect.move(0,0)

        isXWalking = self.leftPressed or self.rightPressed
        isYWalking = self.upPressed or self.downPressed
        
        hPower = 0
        vPower = 0

        if isXWalking:
            hPower = self.xAccel * self.facing
        else:
            hPower = GetFriction(self.velocity[0], self.xFriction)

        if isYWalking:
            vPower = self.yAccel * self.yFacing
        else:
            vPower = GetFriction(self.velocity[1], self.yFriction)

        self.velocity[0] = clamp(self.velocity[0]+hPower, self.xMin, self.xMax)
        self.velocity[1] = clamp(self.velocity[1]+vPower, self.yMin, self.yMax)

        newRect = oldRect.move(*self.velocity)

        #TODO: calculate collisions and the walkable mask here....
        oob = outOfBounds(self.walkMask, self.feetPos, newRect.midtop)

        if oob:
            #TODO: more precise
            self.rect = oldRect
        else:
            self.rect = newRect

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

