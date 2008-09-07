#! /usr/bin/python

'''Game main module.

Contains the entry point used by the run_game.py script.

Feel free to put all your game code here, or in other modules in this "lib"
directory.
'''
import data
import pyglet
from pyglet import window
from pyglet import clock
from pyglet import font


def main():
    window = pyglet.window.Window()
    label = pyglet.text.Label('Hello, world',
                          font_name='Times New Roman',
                          font_size=36,
                          x=window.width//2, y=window.height//2,
                          anchor_x='center', anchor_y='center')

    bg = data.pngs['levelbg01.png']
    @window.event
    def on_draw():
        window.clear()
        bg.blit(0,0,0)
        label.draw()

    pyglet.app.run()

if __name__ == '__main__':
    main()
