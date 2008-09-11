#! /usr/bin/python

import pyglet
import events
import window
import data
import yoyo

import euclid
import effects
from random import randint

keysPressed = {}

class AvatarSprite(pyglet.sprite.Sprite):
    def __init__(self, avatar):
        self.avatar = avatar
        img = data.pngs['avatar.png']
        pyglet.sprite.Sprite.__init__(self, img, 0, 0)
        events.AddListener(self)
        self.blinkingCounter = 0.0

        self.blood = []

        direction = effects.Blood.right
        for drop in range(0, randint(15, 20)):
            self.blood.append(effects.Blood(euclid.Vector2(200, 200), direction +
                               euclid.Vector2(randint(-2, 2), randint(-2, 2))))

        self.yoyo = yoyo.YoYo()

        self.on_key_press = window.window.event(self.on_key_press)
        self.on_key_release = window.window.event(self.on_key_release)


    def update(self, timeChange=None):
        self.avatar.update(timeChange)

        if self.blinkingCounter > 0:
            self.opacity = (10 + self.opacity) % 255
            self.blinkingCounter -= timeChange
        elif not self.opacity == 255:
            self.opacity = 255

        self.x = self.avatar.x
        self.y = self.avatar.y

        deltaX = self.x - self.yoyo.x + 35
        deltaY = self.y - self.yoyo.y + 40

        self.yoyo.x = self.x + 35
        self.yoyo.y = self.y + 40
        self.yoyo.yoyoX += deltaX
        self.yoyo.yoyoY += deltaY

        self.x += window.bgOffset[0]
        self.y += window.bgOffset[1]

        self.yoyo.offsetX = window.bgOffset[0]
        self.yoyo.offsetY = window.bgOffset[1]

        self.yoyo.facing = self.avatar.facing

        self.yoyo.update(timeChange)

    def On_AttackHit(self, attack, attacker, victim):
        if victim == self.avatar:
            self.blinkingCounter = 1.0

    def on_key_press(self, symbol, modifiers):
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
                fn()

    def on_key_release(self, symbol, modifiers):
        from pyglet.window import key
        keysPressed[symbol] = False

        if symbol == key.LCTRL:
            self.yoyo.yoyoReturn = True

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

