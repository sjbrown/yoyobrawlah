from pyglet import clock
from util import clamp
import window
import data

from avatar import Avatar
from avatarsprite import AvatarSprite

class Scene(object):
    def __init__(self):
        self.done = False


class Level(Scene):
    def __init__(self, levelNum):
        self.done = False
        self.levelNum = '%02d' % levelNum
        self.bg = data.pngs['levelbg'+self.levelNum+'.png']
        self.walkMask = data.levelMasks[self.levelNum]
        print 'walkmask', self.walkMask
        self.triggers = data.levelTriggers['leveltriggers'+self.levelNum]

        self.startLoc = [key for key,val in self.triggers.items()
                        if val == 'start location'][0]

        self.nextScene = None

    def end(self):
        self.done = True

    def calcBGOffset(self, cameraFocusX, cameraFocusY,
                     windowWidth, windowHeight,
                     backgroundWidth, backgroundHeight):
        '''Return the amount to offset the background.
        (cameraFocusX, cameraFocusY) is the spot where the camera is focused
        to, usually the center of the Avatar.
        '''
        return (-clamp(cameraFocusX-(windowWidth/2),
                       0, (backgroundWidth-windowWidth)),
                -clamp(cameraFocusY-(windowHeight/2),
                       0, (backgroundHeight-windowHeight))
               )

    def run(self):
        self.done = False
        clock.set_fps_limit(60)
        win = window.window

        avatar = Avatar()
        avSprite = AvatarSprite(avatar)
        avatar.feetPos = self.startLoc
        avatar.walkMask = self.walkMask
        print 'ava wak', avatar.walkMask
        
        while True:
            timeChange = clock.tick()

            win.dispatch_events()
            avSprite.update( timeChange )

            win.clear()
            if self.done or win.has_exit:
                break

            offset = self.calcBGOffset(avatar.x, avatar.y,
                                       win.width, win.height,
                                       self.bg.width, self.bg.height)
            window.bgOffset[0] = offset[0]
            window.bgOffset[1] = offset[1]

            self.bg.blit(*window.bgOffset)
            avSprite.draw()
            win.flip()

        return self.nextScene

