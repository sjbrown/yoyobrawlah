#! /usr/bin/python

import pyglet
from pyglet import clock
from pyglet import font
from pyglet.gl import *
from util import Rect
import window
import data
import events

class Scene(object):
    def __init__(self):
        self.done = False
        self.moving_bg = None

    def run(self):
        self.done = False
        clock.set_fps_limit(40)
        win = window.window

        xPos = 0

        while not self.done:
            timeChange = clock.tick()
            events.ConsumeEventQueue()
            win.dispatch_events()
            for miscSprite in self.miscSprites:
                miscSprite.update(timeChange)

            win.clear()
            if self.done or win.has_exit:
                break

            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            glColor4f(0.65, 0.65, 0.65, 1)

            if self.moving_bg:
                for count, bbg in enumerate(self.moving_bg):
                    bbg.blit(count * 800 + xPos, 0)

            glColor4f(1, 1, 1, 1)
            self.bg.blit(0,0)
            for miscSprite in self.miscSprites:
                miscSprite.draw()
            win.flip()

            xPos -= 1
            if xPos == -800:
                xPos = 0

        return self.getNextScene()

    def end(self):
        events.RemoveListener(self)
        self.done = True

class SimpleTextButton:
    def __init__(self, text, x, y, selected=False):
        self.bigFont = data.fonts['ohcrud32']
        self.smallFont = data.fonts['ohcrud28']
        self.text = text
        self.x = x
        self.y = y
        self.selected = selected

    def update(self, tick):
        pass

    def draw(self):
        if self.selected:
            text = font.Text(self.bigFont, self.text, x=self.x, y=self.y,
                             color=(1, 1, 1, 1))
        else:
            text = font.Text(self.smallFont, self.text, x=self.x, y=self.y,
                             color=(1, 0.5, 0.5, 1))
    
        text.draw()


class Menu(Scene):
    def __init__(self, sound=True):
        events.AddListener(self)
        self.done = False
        self.bg = data.pngs['menu.png']
        self.moving_bg = [data.pngs['menu-bricks.png'],
                          data.pngs['menu-bricks.png']]
        self.miscSprites = [
            SimpleTextButton('Start!', 400, 200, True),
        ]

        self.keyPress = False
        self.on_key_press = window.window.event(self.on_key_press)
        self.on_key_release = window.window.event(self.on_key_release)

        self.sound = sound

    def on_key_press(self, symbol, modifiers):
        self.keyPress = True
    def on_key_release(self, symbol, modifiers):
        if self.keyPress:
            self.end()

    def getNextScene(self):
        # avoid circular imports
        import level
        return level.getLevel(1, self.sound)

class Cutscene(Scene):
    def __init__(self, cutsceneNum):
        events.AddListener(self)
        self.done = False
        self.cutsceneNum = cutsceneNum
        self.frameNum = 1
        strCutsceneNum = '%02d' % self.cutsceneNum
        strFrameNum = '%02d' % self.frameNum
        self.bg = data.pngs['cutscene'+strCutsceneNum+strFrameNum+'.png']

        # this is a total hack.  just passing these objects on to the next scene
        self.nextLevelNum = None
        self.avatar = None

        self.miscSprites = []

        self.keyPress = False
        self.on_key_press = window.window.event(self.on_key_press)
        self.on_key_release = window.window.event(self.on_key_release)

    def on_key_press(self, symbol, modifiers):
        self.keyPress = True
    def on_key_release(self, symbol, modifiers):
        if self.keyPress:
            self.end()

    def getNextScene(self):
        #print 'geting next scene for cutscene', self.cutsceneNum, self.frameNum
        self.frameNum += 1
        strCutsceneNum = '%02d' % self.cutsceneNum
        strFrameNum = '%02d' % self.frameNum
        try:
            # if there's another frame, just change bg and return self
            self.bg = data.pngs['cutscene'+strCutsceneNum+strFrameNum+'.png']
            return self
        except Exception, ex:
            # passing them on...
            import level
            nextScene = level.getLevel(self.nextLevelNum)
            nextScene.avatar = self.avatar
            return nextScene

