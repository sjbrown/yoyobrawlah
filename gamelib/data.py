'''Simple data loader module.

Loads data files from the "data" directory shipped with a game.

Enhancing this to handle caching etc. is left as an exercise for the reader.
'''

from logging import info as log_info, debug as log_debug
import pyglet
import os

data_py = os.path.abspath(os.path.dirname(__file__))
data_dir = os.path.normpath(os.path.join(data_py, '..', 'data'))

def filepath(filename):
    '''Determine the path to a file in the data directory.
    '''
    return os.path.join(data_dir, filename)

def load(filename, mode='rb'):
    '''Open a file in the data directory.

    "mode" is passed as the second arg to open().
    '''
    return open(os.path.join(data_dir, filename), mode)


# DynamicCachingLoader is an **ABSTRACT** class.  It must be inherited
# from and the subclas MUST implement LoadResource( attname )
class DynamicCachingLoader(dict):
        def __init__(self):
                self._d = {}
        def __getattr__(self, attname):
                try:
                        return self.__dict__[attname]
                except KeyError:
                        log_info( 'loader got key err' )
                        try:
                                return self._d[attname]
                        except KeyError:
                                self.LoadResource( attname )
                                return self._d[attname]

        def __getitem__(self, key):
                try:
                        return self._d[key]
                except KeyError:
                        self.LoadResource( key )
                        return self._d[key]

        def LoadResource(self, resourceName):
                raise NotImplementedError()


class PngLoader(DynamicCachingLoader):
        def LoadResource(self, resourceName):
                name = os.path.join( data_dir, resourceName )
                if not name.endswith('.png'):
                        name += '.png'
                try:
                        image = pyglet.image.load(name)
                except pygame.error, message:
                        log_debug( ' Cannot load image: '+ name )
                        log_debug( 'Raising: '+ str(message) )
                        raise

                self._d[resourceName] = image

soundPlayer = None
class OggLoader(DynamicCachingLoader):
        def LoadResource(self, resourceName):
                if not soundPlayer:
                        try:
                            soundPlayer = pyglet.media.Player()
                        except Exception, ex:
                            log_info('Could not construct sound Player:%s' % ex)
                            return

                name = os.path.join( data_dir, resourceName )
                if not name.endswith('.ogg'):
                        name += '.ogg'

                try:
                    sound = pyglet.media.StaticSource(pyglet.media.load(name))
                except Exception, ex:
                    log_info('Could not construct sound Source: %s' % ex)
                    return

                self._d[resourceName] = sound

oggs = OggLoader()
pngs = PngLoader()


