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

class EffectManager(object):
    def __init__(self):
        events.AddListener(self)


    def On_EnemyHurt(self, enemy):
        data.mp3s['oww%d.mp3' % randint(1, 2)].play()

    def On_ExplosionSpecial(self, pos):
        data.mp3s['explosion.mp3'].play()

    def On_WhiffSpecial(self, pos):
        data.mp3s['string-back.mp3'].play()
        pass

    def On_SpriteRemove(self, sprite):
        pass

    def On_AttackHit(self, attack, attacker, victim):
        pass

    def On_SpeechPart(self, speaker, part):
        pass

    def On_StopSpeech(self, speaker):
        pass

    def On_EnemyDeath(self, enemy):
        #print "enemy death"
        data.mp3s['death%d.mp3' % randint(1, 2)].play()
        pass


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

