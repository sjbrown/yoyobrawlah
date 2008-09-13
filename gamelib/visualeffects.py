#! /usr/bin/python

from pyglet.gl import *
from pyglet import font
import pyglet
import random
from random import randint
import events
import window
import data
import attacks

import euclid

def toScreenPos(pos):
    return [pos[0] + window.bgOffset[0], pos[1] + window.bgOffset[1]]

class EffectManager(object):
    def __init__(self):
        self.sprites = []
        events.AddListener(self)
        self.speechBubbles = {}

    def On_EnemyHurt(self, enemy):
        pos = toScreenPos(enemy.feetPos)
        pos[1] += 50
        direction = {-1: Blood.left, 1:Blood.right}[enemy.facing]
        for drop in range(0, randint(5, 20)):
            bl = Blood(pos, direction + euclid.Vector2(randint(-2, 3),
                                                       randint(-2, 3)))
            self.sprites.append(bl)

    def On_ExplosionSpecial(self, pos):
        print 'splode'
        pos = toScreenPos(pos)
        for drop in range(0, randint(4, 8)):
            vector = euclid.Vector2(randint(-2,3), randint(-2,3))
            fb = Fireball(pos, vector)
            self.sprites.append(fb)

    def On_WhiffSpecial(self, pos):
        print 'whiff'
        pos = toScreenPos(pos)
        for drop in range(0, randint(5, 8)):
            vector = euclid.Vector2(randint(-2,3), randint(-2,3))
            puff = Puff(pos, vector)
            self.sprites.append(puff)

    def On_SpriteRemove(self, sprite):
        if sprite in self.sprites:
            self.sprites.remove(sprite)

    def On_AttackHit(self, attack, attacker, victim):
        if isinstance(attack, attacks.Hug):
            pos = list(attacker.center)
            pos[0] += 10* attacker.facing
            self.sprites.append(HeartFloaty(pos))

    def On_SpeechPart(self, speaker, part):
        if speaker in self.speechBubbles:
            self.sprites.remove(self.speechBubbles[speaker])
        pos = list(speaker.center)
        bubble = SpeechBubble(pos, part)
        self.speechBubbles[speaker] = bubble
        self.sprites.append(bubble)

    def On_StopSpeech(self, speaker):
        if speaker in self.speechBubbles:
            self.sprites.remove(self.speechBubbles[speaker])
            del self.speechBubbles[speaker]

    def On_EnemyDeath(self, enemy):
        cls = random.choice([EnemyDeath1, EnemyDeath2])
        self.sprites.append(cls(enemy))


class SpeechBubble(pyglet.sprite.Sprite):
    xPadding = 10
    yPadding = 10
    def __init__(self, pos, part):
        myFont = data.fonts['default']
        self.text = font.Text(myFont, part, color=(0,255,0,1))
        #self.text = font.Text(myFont, part)
        pat = pyglet.image.SolidColorImagePattern((255,255,255,128))
        img = pyglet.image.create(self.text.width + self.xPadding*2,
                                  self.text.height + self.yPadding*2,
                                  pat)
        pyglet.sprite.Sprite.__init__(self, img, 0, 0)

        self.logicalXCenter = pos[0]
        self.logicalY = pos[1] + 40

    def draw(self):
        pyglet.sprite.Sprite.draw(self)
        self.text.draw()

    def update(self, timeChange=None):
        wWidth = window.window.width
        wHeight = window.window.height
        self.x = self.logicalXCenter-(self.width/2) + window.bgOffset[0]

        # keep it on the screen...
        if self.x < 0:
            self.x = 0
        if self.x + self.width > wWidth:
            self.x = wWidth-self.width

        self.y = self.logicalY + window.bgOffset[1]
        self.text.x = self.x + self.xPadding
        self.text.y = self.y + self.yPadding

class HeartFloaty(pyglet.sprite.Sprite):
    def __init__(self, pos):
        img = data.pngs['heartfloaty.png']
        pyglet.sprite.Sprite.__init__(self, img, 0, 0)
        self.logicalX = pos[0]
        self.logicalY = pos[1]

    def update(self, timeChange=None):
        self.x = self.logicalX + window.bgOffset[0]
        self.y = self.logicalY + window.bgOffset[1]
        self.logicalX += randint(-2, 2)
        self.logicalY += 1
        self.opacity -= 2
        self.scale += 0.01
        if self.opacity < 80:
            events.Fire('SpriteRemove', self)

class EnemyDeath1(pyglet.sprite.Sprite):
    def __init__(self, enemy):
        img = data.pngs[enemy.deathImg]
        pyglet.sprite.Sprite.__init__(self, img, 0, 0)
        self.logicalX = enemy.feetPos[0]
        self.logicalY = enemy.feetPos[1]

    def update(self, timeChange=None):
        self.x = self.logicalX + window.bgOffset[0]
        self.y = self.logicalY + window.bgOffset[1]
        self.logicalX += randint(-2, 2)
        self.logicalY += 5
        self.opacity -= 2
        self.scale += 0.01
        if self.opacity < 80:
            events.Fire('SpriteRemove', self)

class EnemyDeath2(EnemyDeath1):
    def __init__(self, enemy):
        EnemyDeath1.__init__(self, enemy)
        self.logicalX -= 75
        self.logicalY -= 14
        self.color = (255,255,255)

    def update(self, timeChange=None):
        self.x = self.logicalX + window.bgOffset[0]
        self.y = self.logicalY + window.bgOffset[1]
        self.color = (self.color[0] -2,
                      self.color[1] -2,
                      self.color[2] -2,
                     )
        self.opacity -= 2
        if self.color[0] < 20:
            events.Fire('SpriteRemove', self)



class Blood(object):
    pink = (220, 0, 0)
    red = (255, 0, 0)
    lightred = (240, 0, 0)
    colors = [pink, red, lightred]
    lifetimeRange = (1, 5)

    left = euclid.Vector2(-2, 0)
    right = euclid.Vector2(2, 0)

    def __init__(self, position, velocity):
        self.color = random.choice(self.colors)
        self.lifetime = random.randint(*self.lifetimeRange) / 10.0
        self.quad = gluNewQuadric()

        self.position = position
        self.velocity = velocity

    def die(self):
        events.Fire('SpriteRemove', self)

    def update(self, tick):
        self.lifetime -= tick
        self.position += self.velocity
        if self.lifetime <= 0:
            self.die()

    def draw(self):
        glPushAttrib(GL_ENABLE_BIT)

        glColor3ub(*self.color)
        gluQuadricDrawStyle(self.quad, GLU_FILL)

        glLoadIdentity()
        glTranslatef(self.position.x, self.position.y, 0)

        gluDisk(self.quad, 0, 2, 50, 1)
        glLoadIdentity()

        glColor3ub(255,255,255)
        glPopAttrib()

class Puff(Blood):
    pink = (250, 200, 200)
    red = (255, 250, 200)
    lightred = (240, 255, 255)
    colors = [pink, red, lightred]
    lifetimeRange = (1, 2)
    left = euclid.Vector2(-2, 0)


class Fireball(Blood):
    pink = (250, 200, 200, 128)
    red = (255, 25, 20, 128)
    lightred = (240, 255, 25, 128)
    colors = [pink, red, lightred]
    lifetimeRange = (3, 3)

    def draw(self):
        glPushAttrib(GL_ENABLE_BIT)

        glColor4ub(*self.color)
        gluQuadricDrawStyle(self.quad, GLU_FILL)

        glLoadIdentity()
        glTranslatef(self.position.x, self.position.y, 0)

        gluDisk(self.quad, 0, 6, 50, 1)
        glLoadIdentity()

        glColor4ub(255,255,255,255)
        glPopAttrib()


if __name__ == '__main__':
    from pyglet import window
    from pyglet import clock

    from random import randint

    win = window.Window(width=800, height=600)

    blood = []

    def splatter(direction):
        for drop in range(0, randint(15, 20)):
            blood.append(Blood(euclid.Vector2(200, 200), direction + 
                               euclid.Vector2(randint(-2, 2), randint(-2, 2))))

    @win.event
    def on_key_press(symbol, modifiers):
        if symbol == window.key.RIGHT:
            splatter(Blood.right)
        elif symbol == window.key.LEFT:
            splatter(Blood.left)

    while not win.has_exit:
        win.dispatch_events()
        tick = clock.tick()

        for drop in blood:
            drop.update(tick)
            if drop.lifetime < 0:
                blood.remove(drop)

        win.clear()

        [drop.draw() for drop in blood]

        win.flip()

