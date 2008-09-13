#! /usr/bin/python

# this defines them in "Image Editor" coordinates, ie, topleft is 0,0
#
# in the image editor, hover over the * lower left * corner.  That's your
# Rect origin, then just add its width and height
triggers = {

(200,660): 'start location',
(361,1000,10,500): 'EnemySpawnLvl2_1',
(371,1000,10,500): 'EnemySpawnLvl2_2',
(1024,1000,10,500): 'EnemySpawnLvl2_3',
(1354,640,60,20): 'StringPickup',
(1590,1000,10,500): 'EnemySpawnLvl2_4',
(1600,1000,10,500): 'EnemySpawnLvl2_5',
(2048,592,640,5): 'EnemySpawnLvl2_6',
(2048,597,640,5): 'EnemySpawnLvl2_7',
(2488,560,200,50): 'GoalZone',
(3108,950,60,20): 'StringPickup',
(3108,900,60,20): 'StringPickup',

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

