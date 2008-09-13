#! /usr/bin/python

# this defines them in "Image Editor" coordinates, ie, topleft is 0,0
#
# in the image editor, hover over the * lower left * corner.  That's your
# Rect origin, then just add its width and height
triggers = {

(200,660): 'start location',
(361,1000,10,500): 'EnemySpawnLvl3_1',
(686,540,340,70): 'EnemySpawnLvl3_2',
(1760,680,150,110): 'EnemySpawnLvl3_3',
#(1590,1000,10,500): 'EnemySpawnLvl3_4',
#(1600,1000,10,500): 'EnemySpawnLvl3_5',
#(2048,592,640,5):   'EnemySpawnLvl3_6',
#(2048,597,640,5):   'EnemySpawnLvl3_7',
(730,500,60,20): 'StringPickup',
(830,510,60,20): 'StringPickup',
(920,500,60,20): 'StringPickup',
(1820,620,80,34): 'YoyoPickup',
(2046,420,210,50): 'GoalZone',
(300,800,75,400): 'GoalZone',


(2730,800,60,20): 'StringPickup',
(2750,730,60,20): 'StringPickup',
(2930,790,60,20): 'StringPickup',
(2700,850,60,20): 'StringPickup',

}

def rewriteToCartesian():
    global triggers
    IMG_HEIGHT = 880

    newTriggers = {}
    for key, val in triggers.items():
        newKey = list(key)
        newKey[1] = IMG_HEIGHT - newKey[1]
        newTriggers[tuple(newKey)] = val

    triggers = newTriggers

rewriteToCartesian()

