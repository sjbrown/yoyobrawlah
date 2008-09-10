#! /usr/bin/python

import pyglet
import events
from walker import Walker
from util import clamp, outOfBounds, Facing, Rect
import attacks

class State:
    idle = 'idle'
    talking = 'talking'
    fastWalking = 'fast walking'
    slowWalking = 'slow walking'
    startingAttack = attacks.State.startingAttack
    attacking = attacks.State.attacking
    endingAttack = attacks.State.endingAttack

    walkingStates = [fastWalking, slowWalking]
    attackingStates = [startingAttack, attacking, endingAttack]


class Enemy(Walker):
    def __init__(self):
        Walker.__init__(self)
        self.health = 10
        self.energy = 1
        self.xMax = 4
        self.xMin = -4
        self.yMax = 2
        self.yMin = -2
        self.state = State.fastWalking
        self.knownAvatars = []
        self.xFightingReach = 10
        self.yFightingReach = 4
        self.attack = attacks.Hug()

    def Hurt(self, amount):
        self.health -= amount
        if self.health > 0:
            print 'enemy hurt!'
            events.Fire('EnemyHurt', self)
        else:
            print 'enemy death!'
            events.Fire('EnemyDeath', self)

    def getDesiredLocation(self):
        if not self.knownAvatars:
            return self.feetPos
        # go after the avatar
        avPos = self.knownAvatars[0].feetPos
        if avPos[0] > self.feetPos[0]:
            desiredX = avPos[0] - 60
        else:
            desiredX = avPos[0] + 60
        return (desiredX, avPos[1])

    def desireWithinReach(self):
        desiredLoc = self.getDesiredLocation()
        xdelta = desiredLoc[0] - self.feetPos[0]
        ydelta = desiredLoc[1] - self.feetPos[1]
        if (abs(xdelta) <= self.xFightingReach and
            abs(ydelta) < self.yFightingReach):
            return True
        return False


    def showAvatar(self, avatar):
        self.knownAvatars.append(avatar)

    def update(self, timeChange=None):
        if self.state in State.attackingStates:
            return self.update_attack(timeChange)
        elif self.state in State.walkingStates:
            return self.update_walk(timeChange)

    def update_attack(self, timeChange):
        attStates = attacks.State

        target = self.knownAvatars[0]
        self.attack.update(timeChange, self.feetPos, self.facing, target)
        self.state = self.attack.state #HACK!!!
        victimsAndAmount = self.attack.GetVictimsAndAmount()
        for victim, attackAmt in victimsAndAmount:
            power = attackAmt*self.energy
            victim.Hurt(power)
            print 'Enemy hit victim', timeChange
            events.Fire('AttackHit', self.attack, self, victim)
        if (self.attack.state == attStates.attacking and
            not self.desireWithinReach()):
            self.attack.end()
        if self.attack.state == attStates.done:
            self.state = State.fastWalking

    def update_walk(self, timeChange):
        oldRect = self.rect.move(0,0)

        desiredLoc = self.getDesiredLocation()
        xdelta = desiredLoc[0] - self.feetPos[0]
        ydelta = desiredLoc[1] - self.feetPos[1]
        if self.desireWithinReach():
            print 'in position.  starting attack'
            self.state = State.startingAttack
            self.attack.start()
            return


        hPower = 0
        vPower = 0

        isXWalking = xdelta != 0
        isYWalking = ydelta != 0

        slowXApproachDistance = self.xFightingReach*2
        slowYApproachDistance = self.yFightingReach*2

        if isXWalking:
            if xdelta > 0:
                self.facing = Facing.right
            else:
                self.facing = Facing.left
            if abs(xdelta) < slowXApproachDistance and abs(self.velocity[0]):
                self.state = State.slowWalking
                hPower = int(abs(self.velocity[0])*0.9) * -self.facing
            else:
                self.state = State.fastWalking
                hPower = self.xAccel * self.facing
        else:
            hPower = -self.velocity[0]

        if isYWalking:
            if ydelta > 0:
                self.yFacing = Facing.up
            else:
                self.yFacing = Facing.down
            if abs(ydelta) < slowYApproachDistance and abs(self.velocity[1]):
                vPower = int(abs(self.velocity[1])*0.5) * -self.yFacing
            else:
                vPower = self.yAccel * self.yFacing
        else:
            vPower = -self.velocity[1]

        newRect = self.walkTo(oldRect, hPower, vPower)

        self.rect = newRect
        #self.fireTriggers() #TODO: maybe enemys should fire triggers?

class WackyEnemy(Enemy):
    def getDesiredLocation(self):
        if not self.knownAvatars:
            return self.feetPos
        # go after the avatar
        return self.knownAvatars[0].feetPos

    def update(self, timeChange=None):
        oldRect = self.rect.move(0,0)

        desiredLoc = self.getDesiredLocation()
        xdelta = desiredLoc[0] - self.feetPos[0]
        ydelta = desiredLoc[1] - self.feetPos[1]
        isXWalking = xdelta != 0
        isYWalking = ydelta != 0
        
        hPower = 0
        vPower = 0

        if isXWalking:
            if xdelta > 0:
                self.facing = Facing.right
            else:
                self.facing = Facing.left
            hPower = self.xAccel * self.facing
        else:
            hPower = -self.velocity[0]

        if isYWalking:
            if ydelta > 0:
                self.yFacing = Facing.up
            else:
                self.yFacing = Facing.down
            vPower = self.yAccel * self.yFacing
        else:
            vPower = -self.velocity[1]

        newRect = self.walkTo(oldRect, hPower, vPower)

        self.rect = newRect

class TalkingEnemy(Enemy):
    def __init__(self):
        Enemy.__init__(self)
        self.state = State.talking
        self.speech = [(2, 'OH HAI'),
                       (3, 'CAN IT BE HUGZ TEIM NOW?'),
                      ]
        self.speechCounter = 0.0
        self.speechIter = None
        self.currentPart = None

    def update(self, timeChange=None):
        if self.state in State.attackingStates:
            return self.update_attack(timeChange)
        elif self.state in State.walkingStates:
            return self.update_walk(timeChange)
        elif self.state == State.talking:
            return self.update_talk(timeChange)

    def update_talk(self, timeChange):
        if self.currentPart == None:
            events.Fire('StartSpeech', self)
            self.speechIter = iter(self.speech)
            self.currentPart = self.speechIter.next()
            events.Fire('SpeechPart', self, self.currentPart[1])
            return

        self.speechCounter += timeChange
        if self.speechCounter > self.currentPart[0]:
            self.speechCounter = 0.0
            try:
                self.currentPart = self.speechIter.next()
                events.Fire('SpeechPart', self, self.currentPart[1])
            except StopIteration:
                events.Fire('StopSpeech', self)
                self.state = State.fastWalking
                
