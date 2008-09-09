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

from logging import info as log_info

#------------------------------------------------------------------------------
# Module-Level stuff
#------------------------------------------------------------------------------

#outside objects can feel free to add themselves to this list
#YES, it is pretty lazy.  Bad programmer!  No cookie!
__listeners = []

__validEvents = []

__eventQueue = []

def AddListener( newListener ):
	__listeners.append( newListener )

def RemoveListener( listener ):
	try:
		__listeners.remove( listener )
	except ValueError:
		pass

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

def ConsumeEventQueue():
	i = 0
	global __eventQueue
	while i < len( __eventQueue ):
		evName, args, kwargs = __eventQueue[i]
		#log_info( 'firing event' + str( evName ) )
		for listener in __listeners:
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
'''.strip().split()
