#! /usr/bin/python

import pyglet
from pyglet import clock
from pyglet.image import Animation, AnimationFrame

import data

class Anim(pyglet.sprite.Sprite):
    def __init__(self, prefix, numFrames):
        self.prefix = prefix
        imgs = []
        names = []
        # frames one to N
        for i in range(1, numFrames+1):
            name = prefix + ( '%02d' % i ) + '.png'
            names.append(name)
            imgs.append(data.pngs[name])
        # and back down, frames N-1 to 1
        for i in range(numFrames, 1, -1):
            name = prefix + ( '%02d' % (i-1) ) + '.png'
            names.append(name)
            imgs.append(data.pngs[name])

        
        flipImgs = []
        for name in names:
            flipImgs.append( pyglet.resource.image(name, flip_x=True) )
            
        #flipImgs = [x.texture.get_transform(flip_x=True, flip_y=True) for x in imgs]
        for flip in flipImgs:
            #flip.blit(0,0)
            #flip.get_texture().blit(0,0)
            #flip.get_image_data().blit(0,0)
            import window, time
            window.window.flip()
            #time.sleep(1)
        #flipImgs = [x.get_transform(flip_x=True).get_texture() for x in imgs]
            
        duration = 0.1
        frames = [ AnimationFrame(x,duration) for x in imgs ]
        flipFrames = [ AnimationFrame(x,duration) for x in flipImgs ]
        self.animation = Animation(frames)
        self.flipAnimation = Animation(flipFrames)
        pyglet.sprite.Sprite.__init__(self, self.animation)
        self.done = False

    def flip(self):
        self.animation, self.flipAnimation = self.flipAnimation, self.animation

    def end(self):
        self.done = True

    def update(self, timeChange):
        pass


def main():
    win = pyglet.window.Window( width=800, height=600 )
    anim = Anim('subWalkSquash', 5)
    while not win.has_exit:
        done = False
        clock.set_fps_limit(60)

        while not done:
            timeChange = clock.tick()

            win.dispatch_events()
            anim.update( timeChange )

            win.clear()
            if done or win.has_exit:
                break

            anim.draw()

            win.flip()

if __name__ == '__main__':
    main()
