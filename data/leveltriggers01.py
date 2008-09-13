#! /usr/bin/python

# this defines them in "Image Editor" coordinates, ie, topleft is 0,0
#
# in the image editor, hover over the * lower left * corner.  That's your
# Rect origin, then just add its width and height
triggers = {

(200,460): 'start location',
(366,800,75,330): 'EnemySpawnLvl1_1',
(750,460,60,20): 'StringPickup',
(750,800,75,350): 'EnemySpawnLvl1_2',
(1825,800,15,550): 'EnemySpawnLvl1_3',
(1840,800,15,550): 'EnemySpawnLvl1_4',
(1410,670,60,20): 'StringPickup',
(1440,750,60,20): 'StringPickup',
(1540,355,60,20): 'StringPickup',
(300,800,75,400): 'GoalZone',
(3038,800,75,400): 'GoalZone',

}

def rewriteToCartesian():
    global triggers
    IMG_HEIGHT = 800

    newTriggers = {}
    for key, val in triggers.items():
        newKey = list(key)
        newKey[1] = IMG_HEIGHT - newKey[1]
        newTriggers[tuple(newKey)] = val

    triggers = newTriggers

rewriteToCartesian()

