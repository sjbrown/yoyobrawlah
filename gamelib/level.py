from pyglet import clock
from util import clamp, Rect
import window
import data
import events

from avatar import Avatar
from avatarsprite import AvatarSprite
from enemy import Enemy
from enemysprite import EnemySprite

class Scene(object):
    def __init__(self):
        self.done = False

class TriggerZone(object):
    def __init__(self, rectTuple, level):
        self.rect = Rect(rectTuple)
        self.level = level
        self.fired = False
    def fire(self, firer):
        print 'firing triggerzone'

class EnemySpawn(TriggerZone):
    def fire(self, firer):
        if self.fired:
            return

        self.fired = True
        enemy = Enemy()
        enemy.feetPos = self.level.startLoc
        enemy.walkMask = self.level.walkMask
        enemy.showAvatar(firer)
        events.Fire('EnemyBirth', enemy)
        print 'fired event!'

class Level(Scene):
    def __init__(self, levelNum):
        events.AddListener(self)
        self.done = False
        self.levelNum = '%02d' % levelNum
        self.bg = data.pngs['levelbg'+self.levelNum+'.png']
        self.walkMask = data.levelMasks[self.levelNum]
        triggers = data.levelTriggers['leveltriggers'+self.levelNum]

        self.triggerZones = []
        for rect,clsName in triggers.items():
            cls = globals().get(clsName)
            if not cls:
                continue
            zone = cls(rect, self)
            self.triggerZones.append(zone)

        self.enemySprites = {}

        self.startLoc = [key for key,val in triggers.items()
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
        print 'setting trig zones', self.triggerZones
        avatar.triggerZones = self.triggerZones

        events.Fire('AvatarBirth', avatar)
        events.Fire('LevelStartedEvent', self)
        
        while True:
            timeChange = clock.tick()

            events.ConsumeEventQueue()
            win.dispatch_events()
            avSprite.update( timeChange )
            for enemySprite in self.enemySprites.values():
                enemySprite.update(timeChange)

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
            for enemySprite in self.enemySprites.values():
                enemySprite.draw()
            win.flip()

        events.Fire('LevelCompletedEvent', self)
        return self.nextScene

    def On_EnemyBirth(self, enemy):
        print 'handling enemy birth'
        enemySprite = EnemySprite(enemy)
        self.enemySprites[enemy] = enemySprite

    def On_EnemyDeath(self, enemy):
        del self.enemySprites[enemy]

