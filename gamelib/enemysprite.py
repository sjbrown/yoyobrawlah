#! /usr/bin/python

import pyglet
import window
import data
import events
from enemy import State
from util import ShadowSprite, Facing
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
    imgPrefix = 'ted'
    def __init__(self, enemy):
        self.enemy = enemy
        events.AddListener(self)
        self.currentAnim = Anim(self.imgPrefix+'Walk', 5)
        #img = data.pngs['enemy.png']
        pyglet.sprite.Sprite.__init__(self, self.currentAnim.animation, 0, 0)
        self.blinkingCounter = 0.0

        self.shadow = ShadowSprite()
        self.shadow.scale = float(self.width)/self.shadow.width
        self.shadow.opacity = 100

        self.hugImgs = {Facing.left: data.pngs[self.imgPrefix+'Hug_left'],
                        Facing.right: data.pngs[self.imgPrefix+'Hug']}
        self.stunImgs = {Facing.left: data.pngs[self.imgPrefix+'Stun_left'],
                        Facing.right: data.pngs[self.imgPrefix+'Stun']}
        self.idleImg = data.pngs[self.imgPrefix+'Stand']
        self.walkImg = self.currentAnim.animation

    def draw(self):
        self.shadow.draw()
        if hasattr(self.enemy, 'mad') and self.enemy.mad:
            self.color = (200, 10, 10)
        EnemySprite.draw(self)

    def update(self, timeChange=None):
        EnemySprite.update(self, timeChange)
        if self.enemy.state in State.walkingStates:
            if self.enemy.facing != self.currentAnim.facing:
                self.currentAnim.flip()
                self.image = self.currentAnim.animation
            elif self.image != self.currentAnim.animation:
                self.image = self.currentAnim.animation
        elif self.enemy.state in State.attackingStates:
            self.image = self.hugImgs[self.enemy.facing]
        elif self.enemy.state == State.stunned:
            self.image = self.stunImgs[self.enemy.facing]
        elif self.enemy.state == State.idle:
            self.image = self.idleImg
        self.shadow.x = self.x
        self.shadow.y = self.y - (self.shadow.height/2) #shadow center = feetpos


class KittySprite(TeddySprite):
    imgPrefix = 'kit'

class ThrowingKittySprite(KittySprite):
    def draw(self):
        if self.enemy.attack.knifeSprite:
            self.enemy.attack.knifeSprite.draw()
        KittySprite.draw(self)
