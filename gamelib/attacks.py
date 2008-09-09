#! /usr/bin/python

from util import Rect

class State:
    startingAttack = 'starting attack' #NOTE THIS MUST STAY == TO ENEMY STATE
    attacking = 'attacking' #NOTE THIS MUST STAY == TO ENEMY STATE
    endingAttack = 'ending attack' #NOTE THIS MUST STAY == TO ENEMY STATE
    done = 'done'

    attackingStates = [startingAttack, attacking, endingAttack]


class Attack(object):
    def start(self):
        self.counter = self.startDuration
        self.state = State.startingAttack
        self.victimsAndAmounts = []

    def wipe(self):
        self.victimsAndAmounts = []

    def end(self):
        self.state = State.endingAttack
        self.counter = self.endDuration

    def update_start(self, timeChange, feetPos, facing, target):
        self.counter -= timeChange
        if self.counter <= 0:
            self.state = State.attacking
            self.counter = self.attackDuration
            # POW! the moment we get into attacking state, don't wait for the
            # next tick when we're going through update_attack
            self.instantAttack(feetPos, facing, target)

    def update_attack(self, timeChange, feetPos, facing, target):
        self.counter -= timeChange
        if self.counter <= 0:
            self.end()

    def update_end(self, timeChange, feetPos, facing, target):
        self.counter -= timeChange
        if self.counter <= 0:
            self.state = State.done

    def GetVictimsAndAmount(self):
        return self.victimsAndAmounts[:]


class Hug(Attack):
    startDuration = 0 # Hugs are instantaneous
    attackDuration = 4
    endDuration = 1.1 # give them a chance to escape
    baseAmount = 0

    def start(self):
        Attack.start(self)
        self.upCounter = 0.0

    def update(self, timeChange, feetPos, facing, target):
        self.wipe()
        if self.state == State.startingAttack:
            return self.update_start(timeChange, feetPos, facing, target)
        elif self.state == State.attacking:
            # keep hugging every half second
            self.upCounter += timeChange
            if self.upCounter > 0.5:
                self.upCounter -= 0.5 
                self.instantAttack(feetPos, facing, target)
            self.update_attack(timeChange, feetPos, facing, target)
        elif self.state == State.endingAttack:
            return self.update_end(timeChange, feetPos, facing, target)

    def endImmediately(self):
        self.state = State.done

    def instantAttack(self, feetPos, facing, target):
        self.victimsAndAmounts.append((target,0))
            

class YoyoAttack(Attack):
    startDuration = 0
    attackDuration = 0.3
    endDuration = 0.1
    baseAmount = 1

    def __init__(self, yoyo):
        self.yoyo = yoyo
        self.victimsAndAmounts = []

    def update(self, timeChange, feetPos, facing, target):
        self.wipe()
        if self.state == State.startingAttack:
            return self.update_start(timeChange, feetPos, facing, target)
        elif self.state == State.attacking:
            self.update_attack(timeChange, feetPos, facing, target)
        elif self.state == State.endingAttack:
            return self.update_end(timeChange, feetPos, facing, target)

    def instantAttack(self, feetPos, facing, target):
        for t in target:
            vDistance = t.feetPos[0] - feetPos[0]
            if facing * vDistance < 0: #facing the wrong way
                continue
            if abs(vDistance) <= self.yoyo.stringLength:
                self.victimsAndAmounts.append((t,1))

class YoLoop(YoyoAttack):
    pass

class YoWalkTheDog(YoyoAttack):
    pass

class YoShootTheMoon(YoyoAttack):
    pass

def makeYoyoAttacks(yoyo):
    return { 'looping': YoLoop(yoyo),
             'walkthedog': YoWalkTheDog(yoyo),
             'shootthemoon': YoShootTheMoon(yoyo),
           }
