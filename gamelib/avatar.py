#! /usr/bin/python

import math
import pyglet
import events
from walker import Walker
import attacks
from attacks import State as attStates
from util import clamp, outOfBounds, Facing, Rect

GODMODE = False

class State:
    normal = 'normal'
    stunned = 'stunned'
    attacking = 'attacking'

def GetFriction(orig, absFriction):
    '''Return the friction.  Makes sure that the friction opposes the orig'''
    if abs(orig) < 1:
        return 0
    elif orig < 0:
        return +absFriction
    elif orig > 0:
        return -absFriction

class AvatarAttack(object):
    '''Abstract class for the various avatar attacks'''

    def GetVictimsAndAmount(self, origin):
        '''returns a list of pairs (victim, amount of attack power)'''
        raise NotImplementedError('abstract class')

    def GetVictimsInRange(self, origin):
        '''given an origin point, return a list of all victims that this
        attack would hit
        '''
        raise NotImplementedError('abstract class')
        

class Avatar(Walker):
    '''This is the duder that a player controls'''
    attackImg = 'subAttack'
    deadImg = 'subdeath'

    def __init__(self):
        Walker.__init__(self)
        events.AddListener(self)
        self.health = 3
        self.state = State.normal
        self.upPressed = False
        self.rightPressed = False
        self.downPressed = False
        self.leftPressed = False
        self.xFriction = 1
        self.yFriction = 2
        self.xAccel = 1
        self.yAccel = 1 
        self.xMax = 6
        self.xMin = -6
        self.yMax = 2
        self.yMin = -2
        self.stunCounter = 0
        self.yoyo = LogicalYoyo()
        self.attacks = attacks.makeYoyoAttacks(self.yoyo)
        self.strings = []
        self.selectedAttack = None

    def getEnergy(self):
        # max energy is 5
        return min(self.getStringLength(), 5)

    def getStringLength(self):
        if GODMODE:
            self.strings = [1,1,1,1,1,1]
        #always 1 string inside the yoyo
        return 1 + len(self.strings)

    def pickupString(self):
        self.strings.append(1)

    def pickupYoyo(self, yoyo):
        self.strings.append(1)
        self.strings.append(1)
        self.strings.append(1)
        self.strings.append(1)
        self.strings.append(1)
        #self.yoyo = yoyo
        #if yoyo:
            #self.attacks = attacks.makeYoyoAttacks(yoyo)
        #events.Fire('AvatarPickup', self, yoyo)
        
    def setAttack(self, attackName):
        # you can only do looping attack until you get the 3rd string
        if self.getStringLength() < 3:
            attackName = 'looping'
        newAttack = self.attacks.get(attackName)
        if newAttack:
            self.selectedAttack = newAttack

    def getAttackables(self):
        import level # avoid circular imports
        return level.getActiveLevel().getAttackables()

    def doAttack(self):
        if not self.selectedAttack:
            print 'fail no attack slected'
            return
        if self.state == State.stunned:
            self.stunCounter += 0.1
            return
        if self.state == State.attacking:
            # already in the middle of it
            return
        print 'really attacking', self.selectedAttack
        self.state = State.attacking
        self.selectedAttack.wipe()
        self.selectedAttack.start()
        #targets = self.getAttackables()
        #self.selectedAttack.instantAttack(self.feetPos, self.facing, targets)
        #victimsAndAmount = self.selectedAttack.GetVictimsAndAmount()
        #for victim, attackAmt in victimsAndAmount:
            #power = attackAmt*self.getEnergy()
            #victim.Hurt(power)
            #print 'Avatar hit victim', power
            #events.Fire('AttackHit', self.selectedAttack, self, victim)


    def On_UpKeyPress(self):
        self.yFacing = Facing.up
        self.upPressed = True
    def On_UpKeyRelease(self):
        self.upPressed = False
    def On_RightKeyPress(self):
        self.facing = Facing.right
        self.rightPressed = True
    def On_RightKeyRelease(self):
        self.rightPressed = False
    def On_DownKeyPress(self):
        self.yFacing = Facing.down
        self.downPressed = True
    def On_DownKeyRelease(self):
        self.downPressed = False
    def On_LeftKeyPress(self):
        self.facing = Facing.left
        self.leftPressed = True
    def On_LeftKeyRelease(self):
        self.leftPressed = False
            
    def update(self, timeChange=None):
        if self.state == State.normal:
            self.update_endAttack(timeChange)
            return self.update_walk(timeChange)
        elif self.state == State.stunned:
            #self.update_endAttack(timeChange)
            return self.update_stunned(timeChange)
        elif self.state == State.attacking:
            self.update_walk(timeChange)
            return self.update_attack(timeChange)

    def update_attack(self, timeChange):
        if not self.yoyo.gfxYoyo:
            # todo this is a hack fix
            return
        attStates = attacks.State

        self.selectedAttack.update(timeChange, self.feetPos, self.facing,
                                   self.getAttackables(), self.yoyo.gfxYoyo)
        victimsAndAmount = self.selectedAttack.GetVictimsAndAmount()
        for victim, attackAmt in victimsAndAmount:
            power = attackAmt*self.getEnergy()
            victim.Hurt(power)
            events.Fire('AttackHit', self.selectedAttack, self, victim)
        if self.selectedAttack.state == attStates.done:
            self.state = State.normal

    def fireSpecial(self):
        if not self.yoyo:
            return
        if not self.yoyo.gfxYoyo:
            # hack hack todo
            return
        x = self.yoyo.gfxYoyo.yoyoX
        y = self.yoyo.gfxYoyo.yoyoY
        if self.getStringLength() <= 5:
            events.Fire('WhiffSpecial', (x,y))
        else:
            events.Fire('ExplosionSpecial', (x,y))
            self.strings.pop()
            #todo: move this into ExplosionAttack
            targets = self.getAttackables()
            for t in targets:
                xdistance = abs(t.feetPos[0] - x)
                ydistance = abs(t.feetPos[1] - y)
                if math.sqrt(xdistance**2 + ydistance**2) < 150:
                    t.Hurt(self.getEnergy())
                    events.Fire('AttackHit', attacks.ExplosionAttack(), self, t)

    def update_endAttack(self, timeChange):
        if ( self.selectedAttack and
             self.selectedAttack.state == attStates.endingAttack):
            self.selectedAttack.update(timeChange, self.feetPos, self.facing,
                                   self.getAttackables(), self.yoyo.gfxYoyo)

    def update_stunned(self, timeChange):
        self.stunCounter += timeChange
        if self.stunCounter >= 0.5:
            self.unstun()

    def update_walk(self, timeChange):
        oldRect = self.rect.move(0,0)

        isXWalking = self.leftPressed or self.rightPressed
        isYWalking = self.upPressed or self.downPressed
        
        hPower = 0
        vPower = 0

        if isXWalking:
            hPower = self.xAccel * self.facing
        else:
            hPower = GetFriction(self.velocity[0], self.xFriction)

        if isYWalking:
            vPower = self.yAccel * self.yFacing
        else:
            vPower = GetFriction(self.velocity[1], self.yFriction)

        newRect = self.walkTo(oldRect, hPower, vPower)

        self.rect = newRect

        self.fireTriggers()

    def fireTriggers(self):
        #Note : this is the exact object from the level, NOT A COPY
        if not self.triggerZones:
            print 'no trig zones!'
            return
        for zone in self.triggerZones:
            if zone.rect.collidepoint(self.feetPos):
                zone.fire(self)

    def stun(self):
        print 'Avatar got stunned.  nooooo'
        self.state = State.stunned
        self.stunCounter = 0.0

    def unstun(self):
        self.state = State.normal
        self.stunCounter = 0

    def Hurt(self, amount):
        # Note: Hurt is instantaneous, unlike On_AttackHit, which is called
        # when the events module dispatches its events
        if amount <= 0:
            return #not actually hurt
        print 'reducing heatlh', self.health
        self.health -= amount
        if self.health == 0 and self.strings:
            self.health = 1
            self.strings = []
        if self.health > 0:
            events.Fire('AvatarHurt', self)
        else:
            events.Fire('AvatarDeath', self)

    def On_AttackHit(self, attack, attacker, victim):
        if victim != self:
            return
        if self.state == State.stunned:
            return

        if isinstance(attack, attacks.Hug):
            self.stun()

class LogicalYoyo(object):
    def __init__(self):
        self.stringLength = 120
        self.gfxYoyo = None
