#! /usr/bin/python

# this defines them in "Image Editor" coordinates, ie, topleft is 0,0
triggers = {

(240,660): 'start location',
(366,770,75,210): 'EnemySpawn',

}

def rewriteToCartesian():
    global triggers
    IMG_HEIGHT = 1000

    newTriggers = {}
    for key, val in triggers.items():
        newKey = list(key)
        newKey[1] = IMG_HEIGHT - newKey[1]
        newTriggers[tuple(newKey)] = val

    triggers = newTriggers

rewriteToCartesian()

