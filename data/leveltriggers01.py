#! /usr/bin/python

# this defines them in "Image Editor" coordinates, ie, topleft is 0,0
#
# in the image editor, hover over the * lower left * corner.  That's your
# Rect origin, then just add its width and height
triggers = {

(200,660): 'start location',
(366,770,75,210): 'EnemySpawn',
(505,660,20,20): 'YoyoPickup',
(585,660,20,20): 'StringPickup',
(1810,690,120,130): 'GoalZone',
(890,760,170,270): 'EnemySpawn2',

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

