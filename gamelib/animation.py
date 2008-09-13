#! /usr/bin/python

import pyglet
from util import Facing
from pyglet import clock
from pyglet.image import Animation, AnimationFrame

import data

class Anim(pyglet.sprite.Sprite):
    def __init__(self, prefix, numFrames, doOutroFrames = True):
        self.prefix = prefix
        self.facing = Facing.right

        imgs, flipImgs = self.loadImgsAndFlipImgs(doOutroFrames,
                                                  numFrames,
                                                  self.prefix)
            
        duration = 0.1
        frames = [ AnimationFrame(x,duration) for x in imgs ]
        flipFrames = [ AnimationFrame(x,duration) for x in flipImgs ]
        self.animation = Animation(frames)
        if flipFrames:
            self.flipAnimation = Animation(flipFrames)
        pyglet.sprite.Sprite.__init__(self, self.animation)
        self.done = False

    def loadImgsAndFlipImgs(self, doOutroFrames, numFrames, prefix):
        imgs = []
        flipImgs = []
        # frames one to N
        for i in range(1, numFrames+1):
            name = prefix + ( '%02d' % i ) + '.png'
            imgs.append(data.pngs[name])
            name = prefix +'_left'+ ( '%02d' % i ) + '.png'
            flipImgs.append(data.pngs[name])
        if doOutroFrames:
            # and back down, frames N-1 to 2
            for i in range(numFrames, 1, -1):
                name = prefix + ( '%02d' % (i-1) ) + '.png'
                imgs.append(data.pngs[name])
                name = prefix +'_left'+ ( '%02d' % (i-1) ) + '.png'
                flipImgs.append(data.pngs[name])

        #flipImgs = [x.texture.get_transform(flip_x=True, flip_y=True) for x in imgs]
        #for flip in flipImgs:
            #flip.blit(0,0)
            #flip.get_texture().blit(0,0)
            #flip.get_image_data().blit(0,0)
            #import window, time
            #window.window.flip()
            #time.sleep(1)
        #flipImgs = [x.get_transform(flip_x=True).get_texture() for x in imgs]

        return imgs, flipImgs

    def flip(self):
        self.facing = -1*self.facing
        self.animation, self.flipAnimation = self.flipAnimation, self.animation
        self.image = self.animation

    def end(self):
        self.done = True

    def update(self, timeChange):
        pass

class BeerThrowAnim(Anim):
    def __init__(self):
        self.prefix = 'beerthrow'
        numFrames = 3

        imgs, flipImgs = self.loadImgsAndFlipImgs(False,
                                                  numFrames,
                                                  self.prefix)
            
        duration = 0.1
        frames = [ AnimationFrame(x,duration) for x in imgs ]
        self.animation = Animation(frames)
        pyglet.sprite.Sprite.__init__(self, self.animation)
        self.done = False

    def update(self, timeChange):
        pass

    def loadImgsAndFlipImgs(self, doOutroFrames, numFrames, prefix):
        imgs = []
        flipImgs = []
        for i in range(1, numFrames+1):
            name = prefix + ( '%02d' % i ) + '.png'
            imgs.append(data.pngs[name])
        return imgs, flipImgs

class StabAnim(Anim):
    def __init__(self, prefix, numFrames):
        self.prefix = prefix

        imgs, flipImgs = self.loadImgsAndFlipImgs(False,
                                                  numFrames,
                                                  self.prefix)
            
        duration = 0.2
        frames = [ AnimationFrame(x,duration) for x in imgs ]
        flipFrames = [ AnimationFrame(x,duration) for x in flipImgs ]
        self.animation = Animation(frames)
        if flipFrames:
            self.flipAnimation = Animation(flipFrames)
        pyglet.sprite.Sprite.__init__(self, self.animation)
        self.done = False

    def end(self):
        self.done = True

    def update(self, timeChange):
        self.x = 40
        self.y = 4


FRAMES_PER_SECOND = 60

def main():
    win = pyglet.window.Window( width=800, height=600 )

    anims = []

    @win.event
    def on_key_press(symbol, modifiers):
        print 'Flipping', anims
        for anim in anims:
            anim.flip()

    anims.append( Anim('subWalkNorm', 5) )
    anims.append( BeerThrowAnim() )

    while not win.has_exit:
        done = False
        clock.set_fps_limit(FRAMES_PER_SECOND)

        while not done:
            timeChange = clock.tick()

            win.dispatch_events()
            for anim in anims:
                anim.update( timeChange )

            win.clear()
            if done or win.has_exit:
                break

            for anim in anims:
                anim.draw()

            win.flip()

if __name__ == '__main__':

    main()

