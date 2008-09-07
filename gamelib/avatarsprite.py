#! /usr/bin/python

import pyglet
from window import window
import data

class AvatarSprite(pyglet.sprite.Sprite):
    def __init__(self, avatar, window):
        self.avatar = avatar
        self.window = window
        img = data.pngs['avatar.png']
        pyglet.sprite.Sprite.__init__(self, img, 0, 0)

    @window.event
    def on_draw(self, timeChange=None):
        self.avatar.update(timeChange)
        self.x = self.avatar.x
        self.y = self.avatar.y

    @window.event
    def on_key_press(self, symbol, modifiers):
        from pyglet.window import key
        dispatchDict = {
            key.UP: self.avatar.OnUpKeyPress,
            key.RIGHT: self.avatar.OnRightKeyPress,
            key.DOWN: self.avatar.OnDownKeyPress,
            key.LEFT: self.avatar.OnLeftKeyPress,
            }
        fn = dispatchDict.get(symbol)
        if fn:
            fn()



def TestAvatar(object):
    '''This avatar class is for testing purposes only.  An instance of
    TestAvatar can be used as an argument to AvatarSprite's constructor
    '''
    def __init__(self):
        self.keysDown = [0,0,0,0]
        self.x = 0
        self.y = 0

    def OnUpKeyPress(self):
        self.y += 4
    def OnRightKeyPress(self):
        self.x += 4
    def OnDownKeyPress(self):
        self.y -= 4
    def OnLeftKeyPress(self):
        self.x -= 4

    def update(self, *args):
        pass

