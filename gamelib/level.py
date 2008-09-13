import pyglet
from pyglet import clock
from pyglet import font
from pyglet import media

from util import clamp, Rect
import window
import data
import events
import glob
import os.path

from avatar import Avatar, LogicalYoyo
from avatarsprite import AvatarSprite
from enemy import Enemy, TalkingTeddy, TalkingKitty, Speeches, ThrowingKitty
import enemysprite

from pyglet.gl import *

import visualeffects
import soundeffects

from scene import Scene, Cutscene, DeathCutscene
import main

DEBUG = True
soundtrack = None

_activeLevel = None
def getActiveLevel():
    return _activeLevel

def getLevel(levelNum, sound):
    # some levels have special menthods and thus have named classes in here.
    className = 'Level'+str(levelNum)
    if className in globals():
        # ie, Level2(2)
        return globals()[className](levelNum, sound)
    else:
        # just a generic level.  no special methods
        return Level(levelNum, sound)

class TriggerZone(object):
    def __init__(self, rectTuple, level):
        self.rect = Rect(rectTuple)
        self.level = level
        self.fired = False
        self.debugSprite = TriggerZoneDebugSprite(self)
    def fire(self, firer=None):
        #print 'firing triggerzone'
        self.fired = True
    def end(self):
        del self.level
        del self.debugSprite

    def doEnemy(self, cls, args, pos, firer):
        enemy = cls(*args)
        enemy.feetPos = pos
        enemy.walkMask = self.level.walkMask
        enemy.showAvatar(firer)
        events.Fire('EnemyBirth', enemy)

class GoalZone(TriggerZone):
    def fire(self, firer):
        if self.fired:
            return
        TriggerZone.fire(self)

        print "GOOOOOOAL"
        events.Fire('LevelCompletedEvent', getActiveLevel())

# XXX - this sucks

class EnemySpawnLvl1_1(TriggerZone):
    def fire(self, firer):
        if self.fired:
            return
        TriggerZone.fire(self)

        self.doEnemy(TalkingTeddy, [Speeches.ohHai], (200,248), firer)
        self.end()

class EnemySpawnLvl1_2(TriggerZone):
    def fire(self, firer):
        if self.fired:
            return
        TriggerZone.fire(self)
        self.doEnemy(TalkingKitty, [Speeches.hugs], (945,350), firer)
        self.end()

class EnemySpawnLvl1_3(TriggerZone):
    def fire(self, firer):
        if self.fired:
            return
        TriggerZone.fire(self)
        self.doEnemy(TalkingTeddy, [Speeches.ohHai], (2200, 150), firer)
        self.end()

class EnemySpawnLvl1_4(TriggerZone):
    def fire(self, firer):
        if self.fired:
            return
        TriggerZone.fire(self)
        self.doEnemy(TalkingTeddy, [[]], (2200, 275), firer)
        self.end()

class EnemySpawnLvl2_1(TriggerZone):
    def fire(self, firer):
        if self.fired:
            return

        self.fired = True
        self.doEnemy(ThrowingKitty, [], (140, 800-460), firer)
        self.doEnemy(TalkingTeddy, [Speeches.nohugs], (75, 800-520), firer)
        self.end()

class EnemySpawnLvl2_2(TriggerZone):
    def fire(self, firer):
        if self.fired:
            return
        TriggerZone.fire(self)
        self.doEnemy(ThrowingKitty, [], (1230, 800-490), firer)
        self.doEnemy(ThrowingKitty, [], (1350, 800-490), firer)
        self.end()

class EnemySpawnLvl2_3(TriggerZone):
    def fire(self, firer):
        if self.fired:
            return
        TriggerZone.fire(self)
        self.doEnemy(ThrowingKitty, [], (2540, 800-440), firer)
        self.doEnemy(ThrowingKitty, [], (2720, 800-490), firer)
        self.doEnemy(ThrowingKitty, [], (2910, 800-490), firer)
        self.end()

class EnemySpawnLvl3_1(TriggerZone):
    def fire(self, firer):
        if self.fired:
            return
        TriggerZone.fire(self)
        self.doEnemy(TalkingTeddy, [[]], (130, 880-520), firer)
        self.doEnemy(TalkingTeddy, [[]], (130, 880-820), firer)
        self.doEnemy(ThrowingKitty, [], (500, 880-520), firer)
        self.doEnemy(ThrowingKitty, [], (500, 880-820), firer)
        self.doEnemy(ThrowingKitty, [], (500, 880-820), firer)
        self.end()

class EnemySpawnLvl3_2(TriggerZone):
    def fire(self, firer):
        if self.fired:
            return
        TriggerZone.fire(self)

        self.doEnemy(TalkingTeddy, [[]], (860, 880-860), firer)
        self.doEnemy(TalkingTeddy, [[]], (600, 880-860), firer)
        self.doEnemy(TalkingTeddy, [[]], (1070, 880-860), firer)
        self.doEnemy(ThrowingKitty, [], (590, 880-500), firer)
        self.end()

class EnemySpawnLvl3_3(TriggerZone):
    def fire(self, firer):
        if self.fired:
            return
        TriggerZone.fire(self)

        self.doEnemy(TalkingTeddy, [[]], (1650, 880-500), firer)
        self.doEnemy(ThrowingKitty, [], (1650, 880-500), firer)
        self.doEnemy(TalkingTeddy, [[]], (1500, 880-860), firer)
        self.doEnemy(ThrowingKitty, [], (1500, 880-860), firer)
        self.doEnemy(TalkingTeddy, [[]], (2046, 880-860), firer)
        self.doEnemy(ThrowingKitty, [], (2046, 880-860), firer)
        self.doEnemy(TalkingTeddy, [[]], (2246, 880-500), firer)
        self.doEnemy(ThrowingKitty, [], (2246, 880-500), firer)
        self.end()

class EnemySpawnLvl4_1(TriggerZone):
    def fire(self, firer):
        if self.fired:
            return
        TriggerZone.fire(self)

        self.doEnemy(TalkingTeddy, [[]], (650, 880-500), firer)
        self.doEnemy(ThrowingKitty, [], (650, 880-500), firer)
        self.doEnemy(TalkingTeddy, [[]], (500, 880-860), firer)
        self.doEnemy(ThrowingKitty, [], (500, 880-860), firer)
        self.doEnemy(TalkingTeddy, [[]], (1046, 880-860), firer)
        self.doEnemy(ThrowingKitty, [], (1046, 880-860), firer)
        self.doEnemy(TalkingTeddy, [[]], (1246, 880-500), firer)
        self.doEnemy(ThrowingKitty, [], (1246, 880-500), firer)
        self.end()

class EnemySpawnLvl4_2(TriggerZone):
    def fire(self, firer):
        if self.fired:
            return
        TriggerZone.fire(self)

        self.doEnemy(TalkingTeddy, [[]], (2100, 880-860), firer)
        self.doEnemy(ThrowingKitty, [], (2100, 880-860), firer)
        self.doEnemy(TalkingTeddy, [[]], (2100, 880-760), firer)
        self.doEnemy(ThrowingKitty, [], (2100, 880-760), firer)
        self.doEnemy(TalkingTeddy, [[]], (2100, 880-660), firer)
        self.doEnemy(ThrowingKitty, [], (2100, 880-660), firer)
        self.doEnemy(TalkingTeddy, [[]], (2100, 880-560), firer)
        self.doEnemy(ThrowingKitty, [], (2100, 880-560), firer)
        self.end()

class TriggerZoneDebugSprite(pyglet.sprite.Sprite):
    def __init__(self, zone):
        pat = pyglet.image.SolidColorImagePattern((255,255,0,100))
        img = pyglet.image.create(zone.rect.width, zone.rect.height, pat)
        self.origX = zone.rect.x
        self.origY = zone.rect.y
        pyglet.sprite.Sprite.__init__(self, img, self.origX, self.origY)

    def update(self, timeChange=None):
        self.x = self.origX + window.bgOffset[0]
        self.y = self.origY + window.bgOffset[1]

class PickupSprite(pyglet.sprite.Sprite):
    def __init__(self, imgName, zone, x, y):
        self.zone = zone
        img = data.pngs[imgName]
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

class YoyoPickupSprite(PickupSprite):
    def __init__(self, zone, x, y):
        PickupSprite.__init__(self, 'yoyo_pickup.png', zone, x, y)

class StringPickupSprite(PickupSprite):
    def __init__(self, zone, x, y):
        PickupSprite.__init__(self, 'string_pickup.png', zone, x, y)


class YoyoPickup(TriggerZone):
    def __init__(self, rectTuple, level):
        TriggerZone.__init__(self, rectTuple, level)
        self.sprite = YoyoPickupSprite(self, *self.rect.center)
    def fire(self, firer):
        if self.fired:
            return
        if not isinstance(firer, Avatar):
            return

        ##print 'yoyo pickup!'

        self.fired = True
        yoyo = LogicalYoyo()
        firer.pickupYoyo(yoyo)
        events.Fire('TriggerZoneRemove', self)

class StringPickup(TriggerZone):
    def __init__(self, rectTuple, level):
        TriggerZone.__init__(self, rectTuple, level)
        self.sprite = StringPickupSprite(self, *self.rect.center)

    def fire(self, firer):
        if self.fired:
            return
        if not isinstance(firer, Avatar):
            return
        #print 'string pickup!'
        self.fired = True
        firer.pickupString()
        del self.sprite
        events.Fire('TriggerZoneRemove', self)

class Heart(pyglet.sprite.Sprite):
    def __init__(self):
        imageFile = data.pngs['small-heart.png']
        pyglet.sprite.Sprite.__init__(self, imageFile, 0, 0)

class HeartMeter:
    def __init__(self):
        pass

    def update(self, tick):
        pass

    def draw(self, avatar):
        #TODO: its not efficient to create sprites in here every time
        for i in range(avatar.health):
            heart = Heart()
            heart.x = i * 41 + 10
            heart.y = 5
            heart.draw()

class YoyoHud(pyglet.sprite.Sprite):
    def __init__(self):
        imageFile = data.pngs['yorect_small.png']
        pyglet.sprite.Sprite.__init__(self, imageFile, 0, 0)

class StringHud(pyglet.sprite.Sprite):
    def __init__(self):
        imageFile = data.pngs['string_hud.png']
        pyglet.sprite.Sprite.__init__(self, imageFile, 0, 0)

class EnergyMeter(object):
    def __init__(self, pos):
        events.AddListener(self)
        self.pos = pos
        self.yoImg = YoyoHud()
        self.yoImgShake = [0,0]
        self.pulse = 0

    def draw(self, avatar):
        x = self.pos[0]
        self.yoImg.x = x
        self.yoImg.y = self.pos[1]
        if self.yoImgShake[0] or self.yoImgShake[1]:
            import random
            self.yoImgShake[0] = abs(self.yoImgShake[0]) - random.randint(0,4)
            self.yoImgShake[1] = abs(self.yoImgShake[1]) - random.randint(0,4)
            self.yoImgShake[0] *= random.choice([1,-1])
            self.yoImgShake[1] *= random.choice([1,-1])
            self.yoImg.x += self.yoImgShake[0]
            self.yoImg.y += self.yoImgShake[1]
            
        x += 30
        #TODO: its not efficient to create sprites in here every time
        for i in range(avatar.getStringLength()):
            stringImg = StringHud()
            if i > 4:
                # more than 5 strings are volatile
                self.pulse += 10
                self.pulse %= 256
                stringImg.opacity = self.pulse
            stringImg.x = x - (i*2)
            stringImg.y = self.pos[1]
            stringImg.draw()
            x += stringImg.width
        if avatar.yoyo:
            self.yoImg.draw()

    def On_AttackHit(self, attack, attacker, victim):
        if isinstance(attacker, Avatar):
            self.yoImgShake = [10,10]

class Level(Scene):
    def __init__(self, levelNum, sound=True):
        global soundtrack
        events.AddListener(self)
        self.done = False
        self.deathDelay = 0
        self.levelNum = levelNum
        strLevelNum = '%02d' % levelNum
        triggers = data.levelTriggers['leveltriggers'+strLevelNum]
        if not levelNum % 2:
            # even levels are repeats of previous images
            strLevelNum = '%02d' % (levelNum-1)
        self.walkMask = data.levelMasks[strLevelNum]
        filePath= os.path.join(data.data_dir, 'levelbg%s-?.png' % strLevelNum)
        self.sound = sound

        bgPngs = glob.glob(filePath)
        bgPngs.sort()
        self.bgImages = [data.pngs[png] for png in bgPngs]

        if self.levelNum == 1:
            self.avatar = Avatar()
            self.visualEffects = visualeffects.EffectManager()

        self.miscSprites = []
        healthFont = font.load('Oh Crud BB', 28)
        #self.healthText = font.Text(healthFont, x=10, y=25, text='Health:')
        self.healthBar = HeartMeter()
        self.energyBar = EnergyMeter((240,5))

        self.fpsText = font.Text(healthFont, x=650, y=25)

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
            if DEBUG and hasattr(zone, 'debugSprite'):
                self.miscSprites.append(zone.debugSprite)

        self.enemySprites = {}

        self.startLoc = [key for key,val in triggers.items()
                        if val == 'start location'][0]

        if levelNum == 1 and self.sound:
            soundtrack = \
                queueSoundtrack('8bp077-01-nullsleep-her_lazer_light_eyes.mp3')
            soundtrack.play()

    def getNextScene(self):
        #print 'getting next scene for ', self.levelNum
        nextScene = getLevel(self.levelNum+1, self.sound)
        nextScene.avatar = self.avatar
        nextScene.visualEffects = self.visualEffects
        return nextScene

    def end(self):
        events.RemoveListener(self)
        print "E"*80, 'end'
        self.done = True
        self.avatar.triggerZones = []
        self.avatar.newLevel()
        del self.enemySprites
        del self.miscSprites
        #del self.avatar
        del self.walkMask
        del self.triggerZones
        #del self.visualEffects
        del self.bgImages
        del self.healthBar
        del self.energyBar

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
        global soundtrack
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

            if soundtrack and self.sound:
                soundtrack.dispatch_events()

            events.ConsumeEventQueue()
            win.dispatch_events()

            if self.deathDelay:
                self.deathDelay -= timeChange
                if self.deathDelay <= 0:
                    self.done = True

            if self.done:
                break

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

            # find the combined height of the background images

            bgWidth = 0
            bgHeight = 0

            for bg in self.bgImages:
                bgWidth += bg.width
                bgHeight += bg.height

            offset = self.calcBGOffset(self.avatar.x, self.avatar.y,
                                       win.width, win.height,
                                       bgWidth, bgHeight)

            window.bgOffset[0] = offset[0]
            window.bgOffset[1] = offset[1]

            #self.bg.blit(*window.bgOffset)
            #[bg.blit(*window.bgOffset) for bg in self.bgImages]

            for count, bg in enumerate(self.bgImages):
                bg.blit(count * 1024 + window.bgOffset[0], window.bgOffset[1])

            for miscSprite in self.miscSprites:
                miscSprite.draw()
            avSprite.draw()

            for enemySprite in self.enemySprites.values():
                enemySprite.draw()
            for sprite in self.visualEffects.sprites:
                sprite.draw()

            #self.healthText.draw()
            self.healthBar.draw(self.avatar)
            self.energyBar.draw(self.avatar)

            if DEBUG:
                self.fpsText.text = "fps: %d" % clock.get_fps()
                self.fpsText.draw()

            win.flip()

        return self.getNextScene()

    def On_LevelCompletedEvent(self, level):
        # just assume it's me.
        self.end()

    def On_AvatarDeath(self, avatar):
        # wait 5 seconds then cutscene
        self.deathDelay = 5.0
        def getNextScene():
            scene = DeathCutscene()
            scene.avatar = None
            return scene
        self.getNextScene = getNextScene

    def On_EnemyBirth(self, enemy):
        #print 'handling enemy birth'
        cls = getattr(enemysprite, enemy.spriteClass)
        enemySprite = cls(enemy)
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
        scene.visualEffects = self.visualEffects
        scene.nextLevelNum = 3
        scene.sound = self.sound
        return scene

def renderTriangle():
    glPushAttrib(GL_ENABLE_BIT)

    # resets the state machine to 0, 0 (the identity matrix)
    glLoadIdentity()

    # moves the state machine to 200, 200
    glTranslatef(200, 200, 0)
    glColor3ub(255, 0, 0)

    # draws the triangle in the relative position
    glBegin(GL_TRIANGLES)
    glVertex3f(100.0, -100.0, 0.0)
    glVertex3f(-100.0, -100.0, 0.0)
    glVertex3f(0.0, 100.0, 0.0)
    glEnd()

    glColor3ub(255, 255, 255)
    glLoadIdentity()

    glPopAttrib()

def queueSoundtrack(song):
    global soundtrack
    if not soundtrack:
        soundtrack = media.Player()
        soundtrack.eos_action = 'loop'
    soundtrack.queue(media.load(os.path.join(data.data_dir, song)))
    return soundtrack

