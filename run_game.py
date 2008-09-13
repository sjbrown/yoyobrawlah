#! /usr/bin/env python

from gamelib import main
import getopt
import sys

vsync = False
sound = True

def usage(argv):
    print "Usage: %s [OPTIONS]" % argv[0]
    print
    print "Option           Description"
    print "--nosound        Turn off in game music"
    print "--vsync          Turn on monitor verticle sync"
    print

try:
    opts, args = getopt.getopt(sys.argv[1:], '', ['vsync', 'nosound'])
except getopt.GetoptError, err:
    print "unrecognized command"
    usage(sys.argv)
    sys.exit(1)

for opt, arg in opts:

    if opt == '--vsync':
        print "vsync on"
        vsync = True
    elif opt == '--nosound':
        print "sound off"
        sound = False
        

main.main(vsync, sound)
