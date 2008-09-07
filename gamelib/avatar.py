#! /usr/bin/python

import pygame
import pyglet
import events

#make a Rect that obeys pyglet's cartesian origin
class Rect(pygame.Rect):
    def move_ip(self, x, y):
        return pygame.Rect.move_ip(x,-y)
    def move(self, x, y):
        return pygame.Rect.move(x,-y)

class Facing:
    left = -1
    right = 1

class State:
    normal = 'normal'

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
        self.leftPressed = False
        self.rightPressed = False
        self.facing = Facing.right

    def Hurt(self, amount):
        self.health -= amount
        if self.health > 0:
            events.fire('AvatarHurt', self)
        else:
            events.fire('AvatarDeath', self)

    def Attack(self, attack):
        center = self.logicalRect.center
        for victim, attackAmt in attack.GetVictimsAndAmount(self.center):
            power = attackAmt*self.energy
            victim.Hurt(power)

    def On_UpKeyPress(self):
        self.upPressed = True
    def On_UpKeyRelease(self):
        self.upPressed = False
    def On_RightKeyPress(self):
        self.rightPressed = True
    def On_RightKeyRelease(self):
        self.rightPressed = False
    def On_DownKeyPress(self):
        self.downPressed = True
    def On_DownKeyRelease(self):
        self.downPressed = False
    def On_LeftKeyPress(self):
        self.leftPressed = True
    def On_LeftKeyRelease(self):
        self.leftPressed = False
            
    def update(self, timeChange):
        isWalking = any(self.leftPressed, self.rightPressed,
                        self.upPressed, self.downPressed)
        self.logicalRect.move_ip(*self.moveState)

    def setCenter(self, xy):
        self.logicalRect.center = xy
    def getCenter(self):
        return self.logicalRect.center
    center = property(getCenter, setCenter)

    def setX(self, x):
        self.logicalRect.x = x
    def getX(self):
        return self.logicalRect.x
    center = property(getX, setX)

    def setY(self, y):
        self.logicalRect.y = y
    def getY(self):
        return self.logicalRect.y
    center = property(getY, setY)

