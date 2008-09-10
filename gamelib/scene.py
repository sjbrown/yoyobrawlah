#! /usr/bin/python

import pyglet
from pyglet import clock
from util import Rect
import window
import data
import events

class Scene(object):
    def __init__(self):
        self.done = False

    def run(self):
        self.done = False
        clock.set_fps_limit(40)
        win = window.window

        while not self.done:
            timeChange = clock.tick()
            events.ConsumeEventQueue()
            win.dispatch_events()
            for miscSprite in self.miscSprites:
                miscSprite.update(timeChange)

            win.clear()
            if self.done or win.has_exit:
                break

            self.bg.blit(0,0)
            for miscSprite in self.miscSprites:
                miscSprite.draw()
            win.flip()

        return self.getNextScene()

    def end(self):
        events.RemoveListener(self)
        self.done = True


class Menu(Scene):
    def __init__(self):
        events.AddListener(self)
        self.done = False
        self.bg = data.pngs['menu.png']
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
        # avoid circular imports
        import level
        return level.getLevel(1)

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
