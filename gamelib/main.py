#! /usr/bin/python

'''Game main module.

Contains the entry point used by the run_game.py script.

'''
import pyglet
import window
import level


def main():
    win = pyglet.window.Window( width=800, height=600 )
    window.setWindow(win)

    scene = level.Level(1)

    #win.push_handlers(pyglet.window.event.WindowEventLogger())

    while scene and not win.has_exit:
        scene = scene.run()

if __name__ == '__main__':
    main()
