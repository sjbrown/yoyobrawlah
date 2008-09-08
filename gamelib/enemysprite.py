#! /usr/bin/python

import pyglet
import window
import data

class EnemySprite(pyglet.sprite.Sprite):
    def __init__(self, enemy):
        self.enemy = enemy
        img = data.pngs['enemy.png']
        pyglet.sprite.Sprite.__init__(self, img, 0, 0)

    def update(self, timeChange=None):
        self.enemy.update(timeChange)
        self.x = self.enemy.x
        self.y = self.enemy.y
        self.x += window.bgOffset[0]
        self.y += window.bgOffset[1]

