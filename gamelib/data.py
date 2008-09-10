'''Simple data loader module.

Loads data files from the "data" directory shipped with a game.

Enhancing this to handle caching etc. is left as an exercise for the reader.
'''

from logging import info as log_info, debug as log_debug
import pyglet
from pyglet import font
import os
import pickle
from array import array

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
                except Exception, ex:
                        log_debug( ' Cannot load image: '+ name )
                        log_debug( 'Raising: '+ str(ex) )
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

class TriggerLoader(DynamicCachingLoader):
        def LoadResource(self, resourceName):
                name = os.path.join( data_dir, resourceName )
                if not name.endswith('.py'):
                        name += '.py'
                try:
                    glbs = {}
                    execfile(name, glbs)
                except Exception, ex:
                        log_debug( 'Cannot load triggers: '+ name )
                        log_debug( 'Raising: '+ str(ex) )
                        raise

                self._d[resourceName] = glbs['triggers']

oggs = OggLoader()
pngs = PngLoader()
levelTriggers = TriggerLoader()

class BinaryMask(object):
    def __init__(self, png):
        format = 'R' #only care about the red
        pitch = png.width * len(format)
        self.width = png.width
        pixeldata = png.get_data(format, pitch)
        self.truthArray = array('b', [x == '\x00' for x in pixeldata])

    def __getitem__(self, key):
        x,y = key
        #print 'returning ', self.pixeldata[ y*self.width + x ] == '\x00'
        return self.truthArray[ y*self.width + x ]
    

class MaskLoader(DynamicCachingLoader):
    def LoadResource(self, resourceName):
        resourceName = str(resourceName)
        png = pngs['levelmask'+resourceName+'.png']
        pickleFname = 'levelmask'+resourceName+'.pkl'
        pickleFname = os.path.join( data_dir, pickleFname )
        mask = None
        if os.path.exists(pickleFname):
            fp = file(pickleFname, 'rb')
            try:
                mask = pickle.load(fp)
            except Exception, ex:
                log_info('Failed loading pickle')
            finally:
                fp.close()
        if not mask:
            mask = BinaryMask(png)
            try:
                fp = file(pickleFname, 'wb')
                pickle.dump(mask, fp)
                fp.close()
            except Exception, ex:
                log_info('Failed saving pickle')
        self._d[resourceName] = mask

levelMasks = MaskLoader()

class FontLoader(DynamicCachingLoader):
    def __init__(self):
        DynamicCachingLoader.__init__(self)
        font.add_directory(data_dir)

    def LoadResource(self, resourceName):
        if resourceName == 'ohcrud':
            name = 'Oh Crud BB'
        elif resourceName == 'schoolgirl':
            name = 'CatholicSchoolGirls BB'
        elif resourceName == 'default':
            name = 'SmackAttack BB'
        else:
            name = resourceName
        try:
            myFont = font.load(name, 14, bold=True)
        except Exception, ex:
            log_info('Failed loading font')
            myFont = font.load('Arial', 14, bold=True)
        self._d[resourceName] = myFont

fonts = FontLoader()



