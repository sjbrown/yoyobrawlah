import math
import pyglet

from pyglet.gl import *
from pyglet.window.key import *

FACING_RIGHT = 1
FACING_LEFT = -1

class Sprite:
    def __init__(self, fileName='svgs/ship.svg'):
        #self.sprite = \
        #    squirtle.SVG(fileName, anchor_x='center', anchor_y='center')
        self.angle = 0
        self.rotation = 0

    def update(self, tick):
        pass

    def collidePoint(self, x, y):
        pass

    def draw(self):
        self.sprite.draw(self.position.x, self.position.y, angle=self.angle)

class YoYo(Sprite):
    def __init__(self, moveType=''):
        self.quad = gluNewQuadric()
        self.x = 300
        self.y = 300

        self.yoyoX = self.x 
        self.yoyoY = self.y

        self.moveType = moveType
        self.time = 0
        self.yoyoReturn = False
        self.bends = []

        self.facing = FACING_LEFT

        self.color = (250, 100, 100)
        self.stringMaxLength = 200

        self.angle = 0

    def throw(self, moveType):
        self.yoyoX = self.x
        self.yoyoY = self.y

        if self.facing == FACING_LEFT:
            self.angle = 90
        else:
            self.angle = 270

        self.bends = []

        self.yoyoReturn = False
        self.moveType = moveType


    def update(self, tick):
        if not self.moveType:
            return

        if self.moveType in ['outandback', 'looping', 'shootthemoon',
                             'windmill']:
            self.angle += 500 * tick

        if self.moveType == 'looping':
            self.loop(tick, False)
        elif self.moveType == 'shootthemoon':
            self.shootTheMoon(tick)
        elif self.moveType == 'walkthedog':
            self.walkTheDog(tick)
        elif self.moveType == 'windmill':
            self.loop(tick, True)

    def walkTheDog(self, tick):
        if not self.yoyoReturn:
            stringLength = tick * 500

            print "strlen = %f" % stringLength

            if self.facing == FACING_RIGHT:
                dirAngle = -45
            else:
                dirAngle = 225

            x = math.cos(math.radians(dirAngle)) * abs(stringLength)
            y = math.sin(math.radians(dirAngle)) * abs(stringLength)

            print "x=%f y=%f" % (x, y)
            opp = max(self.yoyoY, self.y) - min(self.yoyoY, self.y) + abs(y)
            adj = max(self.yoyoX, self.x) - min(self.yoyoX, self.x) + abs(x)

            totalLength = math.sqrt(opp * opp + adj * adj)
            print "total = %f" % totalLength
            
            if totalLength > 60 and totalLength < self.stringMaxLength:
                print "line"
                point = (self.yoyoX, self.yoyoY, 0)
                if point not in self.bends:
                    self.bends.append(point)
                if self.facing == FACING_RIGHT:
                    self.yoyoX += stringLength
                else:
                    self.yoyoX -= stringLength

            elif totalLength < self.stringMaxLength:
                print "angle"
                self.yoyoX += x
                self.yoyoY += y
            else:
                print "end of rope"
        else:
            self._yoyoReturn(tick)  

    def shootTheMoon(self, tick):
        self.outAndBack(tick, True)

    def outAndBack(self, tick, shootTheMoon=False):
        if not self.yoyoReturn:
            stringLength = math.cos(math.radians(self.angle)) * \
                           self.stringMaxLength

            if self.facing == FACING_RIGHT:
                if shootTheMoon and stringLength < 0:
                    dirAngle = 92
                else:
                    dirAngle = 42
            else:
                if shootTheMoon and stringLength < 0:
                    dirAngle = 138
                else:
                    dirAngle = 88

            x = math.cos(math.radians(dirAngle)) * abs(stringLength)
            y = math.sin(math.radians(dirAngle)) * abs(stringLength)

            self.yoyoX = self.x + x
            self.yoyoY = self.y + y

        else:
            self._yoyoReturn(tick)  


    def loop(self, tick, windmill=True):
        stringLengthY = 40

        if not self.yoyoReturn:

            if windmill:
                stringLengthX = 40
            else:
                # change the length to form an ellipse
                if self.angle % 360 > 90 and self.angle % 360 < 270:
                    if self.facing == FACING_RIGHT:
                        stringLengthX = 40
                    else:
                        stringLengthX = self.stringMaxLength
                else:
                    if self.facing == FACING_RIGHT:
                        stringLengthX = self.stringMaxLength
                    else:
                        stringLengthX = 40

            self.yoyoX = math.cos(math.radians(self.angle)) * stringLengthX
            self.yoyoY = math.sin(math.radians(self.angle)) * stringLengthY

            # under handed throw
            if self.facing == FACING_LEFT:
                self.yoyoY = -self.yoyoY

            self.yoyoX += self.x
            self.yoyoY += self.y

        else:
            self._yoyoReturn(tick)  

    def _yoyoReturn(self, tick):
        self.bends = []

        opp = self.yoyoX - self.x
        adj = self.yoyoY - self.y
        rad = math.atan2(opp, adj)

        mov_x = 750 * math.sin(rad) * tick
        mov_y = 750 * math.cos(rad) * tick

        if abs(self.x - self.yoyoX) < 6 and \
           abs(self.y - self.yoyoY) < 6:
            self.yoyoX = self.x
            self.yoyoY = self.y
            self.yoyoReturn = False
            self.moveType = ''
            return

        self.yoyoX -= mov_x
        self.yoyoY -= mov_y


    def _drawString(self):
        # draw the string
        glBegin(GL_LINES)
        glVertex3f(self.x, self.y, 0)
        for bend in self.bends:
            glVertex3f(*bend)
            glVertex3f(*bend)
        glVertex3f(self.yoyoX, self.yoyoY, 0)
        glEnd()

    def draw(self):
        glPushAttrib(GL_ENABLE_BIT)

        self._drawString()

        # draw the yo-yo
        glColor3ub(*self.color)
        gluQuadricDrawStyle(self.quad, GLU_FILL)

        glLoadIdentity()

        glTranslatef(self.yoyoX, self.yoyoY, 0)

        gluDisk(self.quad, 0, 7, 50, 1)
        glColor4f(1.0, 1.0, 1.0, 1.0)
        #glColor4f(0.0, 0.0, 0.0, 1.0)

        glLoadIdentity()

        glPopAttrib()



if __name__ == '__main__':
    from pyglet import window
    from pyglet import clock
    from pyglet.gl import *

    win = window.Window(width=800, height=600)

    yoyo1 = YoYo()

    keysPressed = {}

    @win.event
    def on_key_press(symbol, modifiers):
        keysPressed[symbol] = True

        if symbol == LCTRL:

            if keysPressed.get(DOWN):
                yoyo1.throw('walkthedog')
            elif keysPressed.get(UP):
                yoyo1.throw('shootthemoon')
            elif keysPressed.get(RIGHT) or keysPressed.get(LEFT):
                yoyo1.throw('looping')
            else:
                yoyo1.throw('windmill')

        elif symbol == LEFT:
            yoyo1.facing = FACING_LEFT
            if keysPressed.get(LCTRL):
                yoyo1.throw('looping')
                
        elif symbol == RIGHT:
            yoyo1.facing = FACING_RIGHT
            if keysPressed.get(LCTRL):
                yoyo1.moveType = 'looping'

    @win.event
    def on_key_release(symbol, modifiers):
        keysPressed[symbol] = False

        if symbol == LCTRL:
            yoyo1.yoyoReturn = True

        elif symbol == LEFT or symbol == RIGHT and keysPressed.get(LCTRL):
            yoyo1.moveType = 'windmill'
        
        #elif symbol == LSHIFT:
        #    yoyo1.yoyoReturn = True

    while not win.has_exit:
        win.dispatch_events()
        tick = clock.tick()

        yoyo1.update(tick)

        win.clear()

        yoyo1.draw()
        win.flip()


