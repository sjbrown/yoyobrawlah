#! /usr/bin/python

# this defines them in "Image Editor" coordinates, ie, topleft is 0,0
triggers = {

(240,660): 'start location',


}

def rewriteToCartesian():
    global triggers
    IMG_HEIGHT = 1000

    newTriggers = {}
    for key, val in triggers:
        x,y = key
        newTriggers[(x,IMG_HEIGHT-y)] = val

    triggers = newTriggers

rewriteToCartesian()

