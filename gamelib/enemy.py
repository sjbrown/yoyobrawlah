#! /usr/bin/python

import pyglet
import events
from walker import Walker
from util import clamp, outOfBounds, Facing, Rect

class State:
    normal = 'normal'

class Enemy(Walker):
    def __init__(self):
        Walker.__init__(self)
        self.health = 1
        self.energy = 1
        self.state = State.normal
        self.knownAvatars = []

    def Hurt(self, amount):
        self.health -= amount
        if self.health > 0:
            events.fire('EnemyHurt', self)
        else:
            events.fire('EnemyDeath', self)

    def Attack(self, attack):
        center = self.rect.center
        for victim, attackAmt in attack.GetVictimsAndAmount(self.center):
            power = attackAmt*self.energy
            victim.Hurt(power)

    def getDesiredLocation(self):
        if not self.knownAvatars:
            return self.feetPos
        print 'going after the avatar'
        return self.knownAvatars[0].feetPos

    def showAvatar(self, avatar):
        print 'now i know about', avatar
        self.knownAvatars.append(avatar)

    def update(self, timeChange=None):
        oldRect = self.rect.move(0,0)

        desiredLoc = self.getDesiredLocation()
        xdelta = desiredLoc[0] - self.feetPos[0]
        ydelta = desiredLoc[1] - self.feetPos[1]
        isXWalking = xdelta != 0
        isYWalking = ydelta != 0
        
        hPower = 0
        vPower = 0

        if isXWalking:
            if xdelta > 0:
                self.facing = Facing.right
            else:
                self.facing = Facing.left
            hPower = self.xAccel * self.facing
        else:
            hPower = -self.velocity[0]

        if isYWalking:
            if ydelta > 0:
                self.yFacing = Facing.up
            else:
                self.yFacing = Facing.down
            vPower = self.yAccel * self.yFacing
        else:
            vPower = -self.velocity[1]

        newRect = self.walkTo(oldRect, hPower, vPower)

        self.rect = newRect

        #self.fireTriggers()
