#! /usr/bin/python

# this defines them in "Image Editor" coordinates, ie, topleft is 0,0
#
# in the image editor, hover over the * lower left * corner.  That's your
# Rect origin, then just add its width and height
triggers = {

(100,460): 'start location',
(366,800,75,330): 'EnemySpawnLvl2_1',
(450,660,60,20): 'StringPickup',
(950,800,75,350): 'EnemySpawnLvl2_2',
(2340,800,15,650): 'EnemySpawnLvl2_3',
(2260,380,60,20): 'StringPickup',
(3038,800,75,400): 'GoalZone',
#(300,800,75,400): 'GoalZone',


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

