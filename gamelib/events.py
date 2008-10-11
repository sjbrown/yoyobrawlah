"""
events.py
---------
This is a weird module and uses difficult to read code to make an event
broker with the minimum of typing.  Basically whenever an event is created,
it is automatically broadcast using the module-level function, EventFired()

Note: this is much less sophisticated than an EventManager (as in sjbeasts
and my tutorial).  In particular, it suffers from the ABC->ACB event "out of
order" phenomenon and doesn't use weakrefs, so it keeps all listeners
unessecarily alive.

It's only advantage is that it saves me some typing.

"""

import gc
import weakref
from logging import info as log_info

#------------------------------------------------------------------------------
# Module-Level stuff
#------------------------------------------------------------------------------

#outside objects can feel free to add themselves to this list
#YES, it is pretty lazy.  Bad programmer!  No cookie!
__listeners = weakref.WeakKeyDictionary()

__validEvents = []

__eventQueue = []

def AddListener( newListener ):
	__listeners[ newListener ] = 1

def RemoveListener( listener ):
	global __listeners
	try:
		del __listeners[ listener ]
	except KeyError:
		pass

def Reset():
	global __listeners
	__listeners = weakref.WeakKeyDictionary()

def AddEvent( newEvent ):
	__validEvents.append( newEvent )
	
def Fire( evName, *args, **kwargs ):
	#NOTE: by just taking the evName as a string, this won't be checked
	#      at load-time, it will be checked at runtime.

	# run-time check. looks in the module-level globals for the named event
	global __eventQueue
	if evName not in __validEvents + globals().keys():
		raise Exception( "event not defined" )

	__eventQueue.append( (evName, args, kwargs) )

def CleanWeakrefs():
	# with a really tight update / draw cycle the garbage collector 
	# apparently doesn't get a chance to sweep up the weakrefs, so 
	# we need to do it explicitly
	gc.collect()

def ConsumeEventQueue():
	i = 0
	global __eventQueue
	while i < len( __eventQueue ):
		evName, args, kwargs = __eventQueue[i]
		keys = __listeners.keys()
		for listener in keys:
			methodName = "On_"+ evName
			#if the listener has a handler, call it
			try:
				#get the method
				listenerMethod = getattr( listener, methodName )
			except AttributeError, ex:
				pass
			else:
				#call that method
				# the method can potentially add more
				# items onto the eventQueue
				listenerMethod( *args, **kwargs )
		i += 1
	#all code paths that could possibly add more events to the eventQueue
	# have been exhausted at this point, so it's safe to empty the queue
	__eventQueue = []


#------------------------------------------------------------------------------
__validEvents += '''
LevelStartedEvent
AutonomousAvatarReachedGoal
LevelCompletedEvent
AvatarBirth
AvatarDeath
EnemyBirth
EnemyDeath
EnemyAquiredTarget
AvatarAttack
AvatarHurt
EnemyAttack
EnemyHurt
AttackHit
AvatarPickup
AvatarHealthAdd
AvatarHealthRemove
AvatarEnergyAdd
AvatarEnergyRemove
PowerupConsume
SpriteRemove
TriggerZoneRemove
StartSpeech
SpeechPart
StopSpeech
WhiffSpecial
ExplosionSpecial
LowFPS30
'''.strip().split()
