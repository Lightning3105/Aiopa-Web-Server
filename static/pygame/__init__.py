##    pygame - Python Game Library
##    Copyright (C) 2000-2001  Pete Shinners
##
##    This library is free software; you can redistribute it and/or
##    modify it under the terms of the GNU Library General Public
##    License as published by the Free Software Foundation; either
##    version 2 of the License, or (at your option) any later version.
##
##    This library is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
##    Library General Public License for more details.
##
##    You should have received a copy of the GNU Library General Public
##    License along with this library; if not, write to the Free
##    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
##
##    Pete Shinners
##    pete@shinners.org

'''Top-level Pygame module.

Pygame is a set of Python modules designed for writing games.
It is written on top of the excellent SDL library. This allows you
to create fully featured games and multimedia programs in the Python
language. The package is highly portable, with games running on
Windows, MacOS, OS X, BeOS, FreeBSD, IRIX, and Linux.
'''

__docformat__ = 'restructuredtext'
__version__ = '$Id$'

import os
import sys

class MissingModule:
    def __init__(self, name, info='', urgent=0):
        self.name = name
        self.info = str(info)
        self.urgent = urgent
        if urgent:
            self.warn()

    def __getattr__(self, var):
        if not self.urgent:
            self.warn()
            self.urgent = 1
        MissingPygameModule = "%s module not available" % self.name
        raise NotImplementedError(MissingPygameModule)

    def __nonzero__(self):
        return 0

    def warn(self):
        if self.urgent: type = 'import'
        else: type = 'use'
        message = '%s %s: %s' % (type, self.name, self.info)
        try:
            import warnings
            if self.urgent: level = 4
            else: level = 3
            warnings.warn(message, RuntimeWarning, level)
        except ImportError:
            print(message)



#we need to import like this, each at a time. the cleanest way to import
#our modules is with the import command (not the __import__ function)

#first, the "required" modules
#from _pygame_array import *  #brython fix me
from _pygame_base import *
from _pygame_constants import *
from _pygame_version import *
from _pygame_rect import Rect
import _pygame_color as color
#Color = color.Color
__version__ = ver

#added by earney
import _pygame_time as time
import _pygame_display as display
import _pygame_constants as constants
import _pygame_event as event
import _pygame_font as font
import _pygame_mixer as mixer
import _pygame_sprite as sprite
from _pygame_surface import Surface
import _pygame_image as image
import _pygame_mouse as mouse
import _pygame_transform as transform
import _pygame_draw as draw

#next, the "standard" modules
#we still allow them to be missing for stripped down pygame distributions
'''
try: import _pygame_cdrom
except (ImportError,IOError), msg:cdrom=MissingModule("cdrom", msg, 1)

try: import _pygame_cursors
except (ImportError,IOError), msg:cursors=MissingModule("cursors", msg, 1)

try: import _pygame_display
except (ImportError,IOError), msg:display=MissingModule("display", msg, 1)

try: import _pygame_draw
except (ImportError,IOError), msg:draw=MissingModule("draw", msg, 1)

try: import _pygame_event
except (ImportError,IOError), msg:event=MissingModule("event", msg, 1)

try: import _pygame_image
except (ImportError,IOError), msg:image=MissingModule("image", msg, 1)

try: import _pygame_joystick
except (ImportError,IOError), msg:joystick=MissingModule("joystick", msg, 1)

try: import _pygame_key
except (ImportError,IOError), msg:key=MissingModule("key", msg, 1)

try: import _pygame_mouse
except (ImportError,IOError), msg:mouse=MissingModule("mouse", msg, 1)

try: import _pygame_sprite
except (ImportError,IOError), msg:sprite=MissingModule("sprite", msg, 1)

try: from _pygame_surface import Surface
except (ImportError,IOError):Surface = lambda:Missing_Function

try: from _pygame_overlay import Overlay
except (ImportError,IOError):Overlay = lambda:Missing_Function

try: import _pygame_time
except (ImportError,IOError), msg:time=MissingModule("time", msg, 1)

try: import _pygame_transform
except (ImportError,IOError), msg:transform=MissingModule("transform", msg, 1)


#lastly, the "optional" pygame modules
try:
    import _pygame_font
    import _pygame_sysfont
    _pygame_font.SysFont = _pygame_sysfont.SysFont
    _pygame_font.get_fonts = _pygame_sysfont.get_fonts
    _pygame_font.match_font = _pygame_sysfont.match_font
except (ImportError,IOError), msg:font=MissingModule("font", msg, 0)

try: import _pygame_mixer
except (ImportError,IOError), msg:mixer=MissingModule("mixer", msg, 0)

#try: import _pygame_movie
#except (ImportError,IOError), msg:movie=MissingModule("movie", msg, 0)

#try: import _pygame_movieext
#except (ImportError,IOError), msg:movieext=MissingModule("movieext", msg, 0)

try: import _pygame_surfarray
except (ImportError,IOError), msg:surfarray=MissingModule("surfarray", msg, 0)

try: import _pygame_sndarray
except (ImportError,IOError), msg:sndarray=MissingModule("sndarray", msg, 0)

#try: import _pygame_fastevent
#except (ImportError,IOError), msg:fastevent=MissingModule("fastevent", msg, 0)

#there's also a couple "internal" modules not needed
#by users, but putting them here helps "dependency finder"
#programs get everything they need (like py2exe)
try: import _pygame_imageext; del _pygame_imageext
except (ImportError,IOError):pass

try: import _pygame_mixer_music; del _pygame_mixer_music
except (ImportError,IOError):pass

def packager_imports():
    """
    Some additional things that py2app/py2exe will want to see
    """
    import OpenGL.GL
'''
#make Rects pickleable
import copyreg
def __rect_constructor(x,y,w,h):
	return Rect(x,y,w,h)
def __rect_reduce(r):
	assert type(r) == Rect
	return __rect_constructor, (r.x, r.y, r.w, r.h)
copyreg.pickle(Rect, __rect_reduce, __rect_constructor)

#cleanup namespace
del os, sys, #TODO rwobject, surflock, MissingModule, copy_reg
