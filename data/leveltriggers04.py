#! /usr/bin/python

# this defines them in "Image Editor" coordinates, ie, topleft is 0,0
#
# in the image editor, hover over the * lower left * corner.  That's your
# Rect origin, then just add its width and height
triggers = {

(200,760): 'start location',
(200,637,60,20): 'StringPickup',
(140,637,60,20): 'StringPickup',
(80,637,60,20): 'StringPickup',
(400, 1000,75, 400): 'EnemySpawnLvl4_1',
(1700, 1000,75, 400): 'EnemySpawnLvl4_2',
(1820,637,80,34): 'YoyoPickup',
(2046,520,210,50): 'GoalZone',
(300,800,75,400): 'GoalZone',


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

