#! /usr/bin/python

# this defines them in "Image Editor" coordinates, ie, topleft is 0,0
#
# in the image editor, hover over the * lower left * corner.  That's your
# Rect origin, then just add its width and height
triggers = {

(200,660): 'start location',
(366,1000,75,330): 'EnemySpawnLvl1_1',
(750,660,60,20): 'StringPickup',
(750,1000,75,350): 'EnemySpawnLvl1_2',
(1825,1000,15,550): 'EnemySpawnLvl1_3',
(1840,1000,15,550): 'EnemySpawnLvl1_4',
(1085,800,60,20): 'StringPickup',
(1785,900,60,20): 'StringPickup',
(1700,640,60,20): 'StringPickup',
(3038,1000,75,400): 'GoalZone',

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

