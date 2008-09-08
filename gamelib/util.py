#! /usr/bin/python

import pygame

def clamp(src, _min, _max):
    return min( max( src, _min ), _max )

def outOfBounds(mask, pos1, pos2):
        return mask[pos1] != mask[pos2]

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
