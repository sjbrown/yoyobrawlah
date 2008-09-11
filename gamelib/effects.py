from pyglet.gl import *
import random

import euclid

class Blood:
    pink = (220, 0, 0)
    red = (255, 0, 0)
    lightred = (240, 0, 0)
    colors = [pink, red, lightred]
    lifetimeRange = (1, 15)

    left = euclid.Vector2(-2, 0)
    right = euclid.Vector2(2, 0)

    def __init__(self, position, velocity):
        self.color = random.choice(self.colors)
        self.lifetime = random.randint(*self.lifetimeRange) / 10.0
        self.quad = gluNewQuadric()

        self.position = position
        self.velocity = velocity

    def update(self, tick):
        self.lifetime -= tick
        self.position += self.velocity

    def draw(self):
        glPushAttrib(GL_ENABLE_BIT)

        glColor3ub(*self.color)
        gluQuadricDrawStyle(self.quad, GLU_FILL)

        glLoadIdentity()
        glTranslatef(self.position.x, self.position.y, 0)

        gluDisk(self.quad, 0, 2, 50, 1)
        glLoadIdentity()

        glColor3ub(255, 255, 255)
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

