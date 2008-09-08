#! /usr/bin/python

import pyglet
import events
from walker import Walker
from util import clamp, outOfBounds, Facing, Rect

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
        

class Avatar(Walker):
    '''This is the duder that a player controls'''

    def __init__(self):
        Walker.__init__(self)
        self.health = 10
        self.energy = 10
        self.state = State.normal
        self.upPressed = False
        self.rightPressed = False
        self.downPressed = False
        self.leftPressed = False
        self.xFriction = 1
        self.yFriction = 2
        self.xAccel = 1
        self.yAccel = 1 
        self.xMax = 8
        self.xMin = -8
        self.yMax = 4
        self.yMin = -4

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

        newRect = self.walkTo(oldRect, hPower, vPower)

        self.rect = newRect

        self.fireTriggers()

    def fireTriggers(self):
        if not self.triggerZones:
            print 'no trig zones!'
            return
        for zone in self.triggerZones:
            if zone.rect.collidepoint(self.feetPos):
                zone.fire(self)
