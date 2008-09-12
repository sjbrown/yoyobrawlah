#! /usr/bin/python

import pyglet
import window
import data
import events
from util import ShadowSprite
from animation import Anim

from pyglet.gl import *

class EnemySprite(pyglet.sprite.Sprite):
    def __init__(self, enemy):
        self.enemy = enemy
        events.AddListener(self)
        img = data.pngs['enemy.png']
        pyglet.sprite.Sprite.__init__(self, img, 0, 0)
        self.blinkingCounter = 0.0

    def update(self, timeChange=None):
        self.enemy.update(timeChange)
        self.x = self.enemy.x
        self.y = self.enemy.y
        self.x += window.bgOffset[0]
        self.y += window.bgOffset[1]

        if self.blinkingCounter > 0:
            self.opacity = (20 + self.opacity) % 255
            self.blinkingCounter -= timeChange
        elif not self.opacity == 255:
            self.opacity = 255

    def On_AttackHit(self, attack, attacker, victim):
        if victim == self.enemy:
            self.blinkingCounter = 0.5

class TeddySprite(EnemySprite):
    def __init__(self, enemy):
        self.enemy = enemy
        events.AddListener(self)
        self.currentAnim = Anim('tedWalk', 5)
        #img = data.pngs['enemy.png']
        pyglet.sprite.Sprite.__init__(self, self.currentAnim.animation, 0, 0)
        self.blinkingCounter = 0.0

        self.shadow = ShadowSprite()
        self.shadow.scale = float(self.width)/self.shadow.width
        self.shadow.opacity = 100

    def draw(self):
        self.shadow.draw()
        self.color = (200, 10, 10)
        EnemySprite.draw(self)

    def update(self, timeChange=None):
        EnemySprite.update(self, timeChange)
        self.shadow.x = self.x
        self.shadow.y = self.y - (self.shadow.height/2) #shadow center = feetpos


