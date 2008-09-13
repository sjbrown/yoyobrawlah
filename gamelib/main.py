#! /usr/bin/python

'''Game main module.

Contains the entry point used by the run_game.py script.

'''
import pyglet
import window
import scene


def main():
    win = pyglet.window.Window( width=800, height=600 )
    window.setWindow(win)

    menu = scene.Menu()
    currentScene = menu

    #win.push_handlers(pyglet.window.event.WindowEventLogger())

    while currentScene and not win.has_exit:
        currentScene = currentScene.run()

if __name__ == '__main__':
    main()
