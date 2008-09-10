import pyglet
from pyglet import clock
from util import clamp, Rect
import window
import data
import events

from avatar import Avatar, LogicalYoyo
from avatarsprite import AvatarSprite
from enemy import Enemy, TalkingEnemy
from enemysprite import EnemySprite

import visualeffects

from scene import Scene, Cutscene

_activeLevel = None
def getActiveLevel():
    return _activeLevel

def getLevel(levelNum):
    # some levels have special menthods and thus have named classes in here.
    className = 'Level'+str(levelNum)
    if className in globals():
        # ie, Level2(2)
        return globals()[className](levelNum)
    else:
        # just a generic level.  no special methods
        return Level(levelNum)

class TriggerZone(object):
    def __init__(self, rectTuple, level):
        self.rect = Rect(rectTuple)
        self.level = level
        self.fired = False
    def fire(self, firer):
        print 'firing triggerzone'

class GoalZone(TriggerZone):
    def fire(self, firer):
        if self.fired:
            return

        self.fired = True
        events.Fire('LevelCompletedEvent', getActiveLevel())

class EnemySpawn(TriggerZone):
    def fire(self, firer):
        if self.fired:
            return

        self.fired = True
        enemy = TalkingEnemy()
        enemy.feetPos = self.level.startLoc
        enemy.walkMask = self.level.walkMask
        enemy.showAvatar(firer)
        events.Fire('EnemyBirth', enemy)

class EnemySpawn2(EnemySpawn):
    def fire(self, firer):
        if self.fired:
            return

        self.fired = True
        enemy = TalkingEnemy()
        enemy.feetPos = (1040, 440)
        enemy.walkMask = self.level.walkMask
        enemy.showAvatar(firer)
        events.Fire('EnemyBirth', enemy)

class YoyoPickupSprite(pyglet.sprite.Sprite):
    def __init__(self, zone, x, y):
        self.zone = zone
        img = data.pngs['yoyo_pickup.png']
        self.origX = x - img.width/2
        self.origY = y - img.height/2
        pyglet.sprite.Sprite.__init__(self, img, self.origX, self.origY)
        events.AddListener(self)
        self.state = 'normal'

    def On_TriggerZoneRemove(self, zone):
        if self.zone != zone:
            return
        events.RemoveListener(self)
        self.state = 'die'

    def update(self, timeChange=None):
        self.x = self.origX + window.bgOffset[0]
        self.y = self.origY + window.bgOffset[1]
        if self.state == 'die':
            self.opacity -= 5
            self.scale += 0.1
            if self.opacity < 50:
                events.Fire('SpriteRemove', self)

class YoyoPickup(TriggerZone):
    def __init__(self, rectTuple, level):
        TriggerZone.__init__(self, rectTuple, level)
        self.sprite = YoyoPickupSprite(self, *self.rect.center)
    def fire(self, firer):
        if self.fired:
            return
        if not isinstance(firer, Avatar):
            return

        print 'yoyo pickup!'

        self.fired = True
        yoyo = LogicalYoyo()
        firer.pickupYoyo(yoyo)
        events.Fire('TriggerZoneRemove', self)

class Level(Scene):
    def __init__(self, levelNum):
        events.AddListener(self)
        self.done = False
        self.levelNum = levelNum
        strLevelNum = '%02d' % levelNum
        self.bg = data.pngs['levelbg'+strLevelNum+'.png']
        self.walkMask = data.levelMasks[strLevelNum]
        self.visualEffects = visualeffects.EffectManager()
        triggers = data.levelTriggers['leveltriggers'+strLevelNum]

        if self.levelNum == 1:
            self.avatar = Avatar()

        self.miscSprites = []
        self.triggerZones = []
        for rect, clsName in triggers.items():
            cls = globals().get(clsName)
            if not cls:
                if len(rect) == 4:
                    print "ERROR: couldn't find", clsName
                continue
            zone = cls(rect, self)
            self.triggerZones.append(zone)
            if hasattr(zone, 'sprite'):
                self.miscSprites.append(zone.sprite)

        self.enemySprites = {}

        self.startLoc = [key for key,val in triggers.items()
                        if val == 'start location'][0]

    def getNextScene(self):
        print 'getting next scene for ', self.levelNum
        nextScene = getLevel(self.levelNum+1)
        nextScene.avatar = self.avatar
        return nextScene

    def end(self):
        events.RemoveListener(self)
        self.done = True
        self.avatar.triggerZones = []

    def getAttackables(self):
        # TODO: might wanna be more sophisticated, including barrels and such.
        return self.enemySprites.keys()

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
        global _activeLevel
        _activeLevel = self
        self.done = False
        clock.set_fps_limit(60)
        win = window.window

        avSprite = AvatarSprite(self.avatar)
        self.avatar.feetPos = self.startLoc
        self.avatar.walkMask = self.walkMask
        self.avatar.triggerZones = self.triggerZones

        events.Fire('AvatarBirth', self.avatar)
        events.Fire('LevelStartedEvent', self)
        
        while not self.done:
            timeChange = clock.tick()

            events.ConsumeEventQueue()
            win.dispatch_events()
            avSprite.update( timeChange )
            for miscSprite in self.miscSprites:
                miscSprite.update(timeChange)
            for enemySprite in self.enemySprites.values():
                enemySprite.update(timeChange)
            for sprite in self.visualEffects.sprites:
                sprite.update(timeChange)

            win.clear()
            if self.done or win.has_exit:
                break

            offset = self.calcBGOffset(self.avatar.x, self.avatar.y,
                                       win.width, win.height,
                                       self.bg.width, self.bg.height)
            window.bgOffset[0] = offset[0]
            window.bgOffset[1] = offset[1]

            self.bg.blit(*window.bgOffset)
            for miscSprite in self.miscSprites:
                miscSprite.draw()
            avSprite.draw()
            avSprite.yoyo.draw()
            for enemySprite in self.enemySprites.values():
                enemySprite.draw()
            for sprite in self.visualEffects.sprites:
                sprite.draw()
            win.flip()

        return self.getNextScene()

    def On_LevelCompletedEvent(self, level):
        # just assume it's me.
        self.end()

    def On_EnemyBirth(self, enemy):
        print 'handling enemy birth'
        enemySprite = EnemySprite(enemy)
        self.enemySprites[enemy] = enemySprite

    def On_EnemyDeath(self, enemy):
        del self.enemySprites[enemy]

    def On_TriggerZoneRemove(self, zone):
        if zone in self.triggerZones:
            self.triggerZones.remove(zone)

    def On_SpriteRemove(self, sprite):
        if sprite in self.miscSprites:
            self.miscSprites.remove(sprite)

class Level2(Level):
    def getNextScene(self):
        scene = Cutscene(1)
        scene.avatar = self.avatar
        scene.nextLevelNum = 3
        return scene
