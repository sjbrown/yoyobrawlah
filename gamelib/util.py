#! /usr/bin/python

#import pygame

def clamp(src, _min, _max):
    return min( max( src, _min ), _max )

def outOfBounds(mask, pos1, pos2):
        return mask[pos1] != mask[pos2]

#make a Rect that obeys pyglet's cartesian origin
#class Rect(pygame.Rect):
#    def move_ip(self, x, y):
#        return pygame.Rect.move_ip(self, x,-y)
#    def move(self, x, y):
#        return pygame.Rect.move(self, x,-y)

class Rect(object):
    def __init__(self, *args):
        if len(args) == 1:
            (self.x, self.y, self.width, self.height) = args[0]
        elif len(args) == 4:
            (self.x, self.y, self.width, self.height) = args

    def _getCenter(self):
        return (self.x + int(self.width / 2), self.y + int(self.height / 2))

    def _setCenter(self, *args):
        if len(args) == 1:
            (self.x, self.y) = args[0]
        else:
            (self.x, self.y) = args

    center = property(_getCenter, _setCenter)

    def _getMidtop(self):
        return (self.x + int(self.width / 2), self.y)

    def _setMidtop(self, *args):
        if len(args) == 1:
            (self.x, self.y) = args[0]
        else:
            (self.x, self.y) = args

    midtop = property(_getMidtop, _setMidtop)

    def move(self, x, y):
        return Rect(x+self.x, y+self.y, self.width, self.height)

    def collidepoint(self, *args):
        if len(args) == 1:
            (x, y) = args[0]
        else:
            (x, y) = args

        if x > self.x and x < self.x + self.width and \
           y > self.y and y < self.y + self.height:
            return True
        else:
            return False

class Facing:
    left = -1
    right = 1
    up = 1
    down = -1

import pyglet
import data

class ShadowSprite(pyglet.sprite.Sprite):
    def __init__(self):
        img = data.pngs['shadow.png']
        pyglet.sprite.Sprite.__init__(self, img, 0, 0)
