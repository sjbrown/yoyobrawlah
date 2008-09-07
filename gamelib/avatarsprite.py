#! /usr/bin/python

import pyglet
import window
import data

class AvatarSprite(pyglet.sprite.Sprite):
    def __init__(self, avatar):
        self.avatar = avatar
        img = data.pngs['avatar.png']
        pyglet.sprite.Sprite.__init__(self, img, 0, 0)

        self.on_key_press = window.window.event(self.on_key_press)
        self.on_key_release = window.window.event(self.on_key_release)

    def update(self, timeChange=None):
        self.avatar.update(timeChange)
        self.x = self.avatar.x
        self.y = self.avatar.y
        self.x += window.bgOffset[0]
        self.y += window.bgOffset[1]

    def on_key_press(self, symbol, modifiers):
        from pyglet.window import key
        dispatchDict = {
            key.UP: self.avatar.On_UpKeyPress,
            key.RIGHT: self.avatar.On_RightKeyPress,
            key.DOWN: self.avatar.On_DownKeyPress,
            key.LEFT: self.avatar.On_LeftKeyPress,
            }
        fn = dispatchDict.get(symbol)
        if fn:
            fn()

    def on_key_release(self, symbol, modifiers):
        from pyglet.window import key
        dispatchDict = {
            key.UP: self.avatar.On_UpKeyRelease,
            key.RIGHT: self.avatar.On_RightKeyRelease,
            key.DOWN: self.avatar.On_DownKeyRelease,
            key.LEFT: self.avatar.On_LeftKeyRelease,
            }
        fn = dispatchDict.get(symbol)
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

