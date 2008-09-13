#! /usr/bin/python

import pyglet
import events
import window
import data
import yoyo

import euclid
import effects
from random import randint

from util import Facing
from avatar import State
from animation import Anim
from util import ShadowSprite

keysPressed = {}

class AvatarSprite(pyglet.sprite.Sprite):
    def __init__(self, avatar):
        self.avatar = avatar
        self.currentAnim = Anim('subWalkSquash', 5)
        #img = data.pngs['avatar.png']
        pyglet.sprite.Sprite.__init__(self, self.currentAnim.animation, 0, 0)
        events.AddListener(self)
        self.blinkingCounter = 0.0

        self.yoyo = yoyo.YoYo()

        self.shadow = ShadowSprite()
        self.shadow.scale = float(self.width)/self.shadow.width
        self.shadow.opacity = 128

        self.on_key_press = window.window.event(self.on_key_press)
        self.on_key_release = window.window.event(self.on_key_release)

        self.attackImgs = {Facing.left: data.pngs[self.avatar.attackImg +'_left'],
                           Facing.right: data.pngs[self.avatar.attackImg]}
        self.deadImgs = {Facing.left: data.pngs[self.avatar.deadImg +'_left'],
                         Facing.right: data.pngs[self.avatar.deadImg]}

    def draw(self):
        self.shadow.draw()
        pyglet.sprite.Sprite.draw(self)
        if self.avatar.yoyo and not self.avatar.health == 0:
            if self.avatar.selectedAttack:
                self.avatar.selectedAttack.draw(self.avatar, self.yoyo)
            else:
                self.yoyo.draw()

    def update(self, timeChange=None):
        self.avatar.update(timeChange)

        if self.avatar.state == State.attacking:
            self.image = self.attackImgs[self.avatar.facing]
        elif self.avatar.health == 0:
            self.image = self.deadImgs[self.avatar.facing]
        else:
            if self.avatar.facing != self.currentAnim.facing:
                self.currentAnim.flip()
                self.image = self.currentAnim.animation
            elif self.image != self.currentAnim.animation:
                self.image = self.currentAnim.animation
            

        if self.blinkingCounter > 0:
            self.opacity = (10 + self.opacity) % 255
            self.blinkingCounter -= timeChange
        elif not self.opacity == 255:
            self.opacity = 255

        self.x = self.avatar.x
        self.y = self.avatar.y

        self.x += window.bgOffset[0]
        self.y += window.bgOffset[1]

        if self.avatar.yoyo:
            self.avatar.yoyo.gfxYoyo = self.yoyo
            self.yoyo.moveToFeetPos(self.avatar.feetPos,
                                    self.avatar.facing)
            self.yoyo.stringMaxLength = self.avatar.getStringLength()*30

            if not self.avatar.selectedAttack:
                self.yoyo.update(timeChange)

        self.shadow.x = self.x
        self.shadow.y = self.y - (self.shadow.height/2) #shadow center = feetpos
        if self.avatar.health == 0:
            self.shadow.y += 10

    def On_AttackHit(self, attack, attacker, victim):
        if victim == self.avatar:
            self.blinkingCounter = 1.0

        
    def on_key_press(self, symbol, modifiers):
        if self.avatar.health == 0:
            return

        from pyglet.window import key
        keysPressed[symbol] = True

        if keysPressed.get(key.LCTRL):
        #if symbol == key.LCTRL:
            if keysPressed.get(key.DOWN):
                self.yoyo.throw('walkthedog')
                self.avatar.setAttack('walkthedog')
            elif keysPressed.get(key.UP):
                self.yoyo.throw('shootthemoon')
                self.avatar.setAttack('shootthemoon')
            else:
                self.yoyo.throw('looping')
                self.avatar.setAttack('looping')
            self.avatar.doAttack()
        else:
            moveDict = {
                key.UP: self.avatar.On_UpKeyPress,
                key.RIGHT: self.avatar.On_RightKeyPress,
                key.DOWN: self.avatar.On_DownKeyPress,
                key.LEFT: self.avatar.On_LeftKeyPress,
                }
            fn = moveDict.get(symbol)
            if fn:
                #oldFacing = self.avatar.facing
                fn()
                #print 'old', oldFacing, 'new', self.avatar.facing
                #if self.avatar.facing != oldFacing:
                    #self.currentAnim.flip()


    def on_key_release(self, symbol, modifiers):
        from pyglet.window import key
        keysPressed[symbol] = False

        if symbol == key.LCTRL and self.yoyo.moveType:
            self.yoyo.yoyoReturn = True
            self.avatar.fireSpecial()

        moveDict = {
            key.UP: self.avatar.On_UpKeyRelease,
            key.RIGHT: self.avatar.On_RightKeyRelease,
            key.DOWN: self.avatar.On_DownKeyRelease,
            key.LEFT: self.avatar.On_LeftKeyRelease,
            }
        fn = moveDict.get(symbol)
        if fn:
            fn()




class TestAvatar(object):
    '''This avatar class is for testing purposes only.  An instance of
    TestAvatar can be used as an argument to AvatarSprite's constructor
    '''
    def __init__(self):
        self.keysDown = [0,0,0,0]
        self.x = 0
        self.y = 0

    def On_UpKeyPress(self):
        self.y += 4
    def On_RightKeyPress(self):
        self.x += 4
    def On_DownKeyPress(self):
        self.y -= 4
    def On_LeftKeyPress(self):
        self.x -= 4

    def On_UpKeyRelease(self):
        pass
    def On_RightKeyRelease(self):
        pass
    def On_DownKeyRelease(self):
        pass
    def On_LeftKeyRelease(self):
        pass

    def update(self, *args):
        pass

