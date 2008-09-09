#! /usr/bin/python

from util import Rect

class State:
    startingAttack = 'starting attack' #NOTE THIS MUST STAY == TO ENEMY STATE
    attacking = 'attacking' #NOTE THIS MUST STAY == TO ENEMY STATE
    endingAttack = 'ending attack' #NOTE THIS MUST STAY == TO ENEMY STATE
    done = 'done'

    attackingStates = [startingAttack, attacking, endingAttack]


class Attack(object):
    pass


class Hug(Attack):
    startDuration = 0 # Hugs are instantaneous
    attackDuration = 4
    endDuration = 0.6
    baseAmount = 0

    def start(self):
        self.counter = Hug.startDuration
        self.upCounter = 0
        self.state = State.startingAttack
        self.victimsAndAmounts = []

    def update(self, timeChange, feetPos, facing, target):
        self.victimsAndAmounts = []
        if self.state == State.startingAttack:
            self.counter -= timeChange
            if self.counter <= 0:
                self.state = State.attacking
                self.counter = Hug.attackDuration
                self.violate(target)
        elif self.state == State.attacking:
            self.upCounter += timeChange
            if self.upCounter > 500:
                self.upCounter -= 500
                self.violate(target)
            self.counter -= timeChange
            if self.counter <= 0:
                self.end()
        elif self.state == State.endingAttack:
            self.counter -= timeChange
            if self.counter <= 0:
                self.state = State.done

    def end(self):
        self.state = State.endingAttack
        self.counter = Hug.endDuration
        self.upCounter = 0

    def endImmediately(self):
        self.state = State.done

    def violate(self, target):
        self.victimsAndAmounts.append((target,0))
            
    def GetVictimsAndAmount(self):
        return self.victimsAndAmounts[:]
