#! /usr/bin/python

'''Game main module.

Contains the entry point used by the run_game.py script.

'''
import pyglet
import window
import scene
import events

import soundeffects

def main(vsync=False, sound=True):
    global visualEffects
    if vsync:
        win = pyglet.window.Window(width=800, height=600)
    else:
        win = pyglet.window.Window(width=800, height=600, vsync=0)
        
    window.setWindow(win)

    menu = scene.Menu(sound)
    currentScene = menu

    #win.push_handlers(pyglet.window.event.WindowEventLogger())

    soundEffects = soundeffects.EffectManager()

    while currentScene and not win.has_exit:
        currentScene = currentScene.run()
        if soundEffects not in events.__listeners:
            events.AddListener(soundEffects)

if __name__ == '__main__':
    main()
