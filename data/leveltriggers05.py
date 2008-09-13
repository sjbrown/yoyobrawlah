#! /usr/bin/python

# this defines them in "Image Editor" coordinates, ie, topleft is 0,0
#
# in the image editor, hover over the * lower left * corner.  That's your
# Rect origin, then just add its width and height
triggers = {

(200,760): 'start location',
(136,964,60,20): 'StringPickup',
(226,964,60,20): 'StringPickup',
(488,744,10,210): 'EnemySpawnLvl3_1',
(498,744,10,210): 'EnemySpawnLvl3_2',
(518,744,10,210): 'EnemySpawnLvl3_3',
(528,744,10,210): 'EnemySpawnLvl3_4',
(548,744,10,210): 'EnemySpawnLvl3_5',
(558,744,10,210): 'EnemySpawnLvl3_6',
(578,744,10,210): 'EnemySpawnLvl3_7',
(588,744,10,210): 'EnemySpawnLvl3_8',
(608,744,10,210): 'EnemySpawnLvl3_9',
(618,744,10,210): 'EnemySpawnLvl3_10',
(638,744,10,210): 'EnemySpawnLvl3_11',
(2600, 560, 50, 100): 'GoalZone' 
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

