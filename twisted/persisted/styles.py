
# Twisted, the Framework of Your Internet
# Copyright (C) 2001 Matthew W. Lefkowitz
# 
# This library is free software; you can redistribute it and/or
# modify it under the terms of version 2.1 of the GNU Lesser General Public
# License as published by the Free Software Foundation.
# 
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA


"""
Different styles of peristed objects.
"""

import os.path
import types
import cPickle
import cStringIO
import copy_reg
import copy
import string
import sys
import traceback


try:
    from new import instancemethod
except:
    from org.python.core import PyMethod
    instancemethod = PyMethod

## First, let's register support for some stuff that really ought to
## be registerable...

def pickleMethod(method):
    'support function for copy_reg to pickle method refs'
    return unpickleMethod, (method.im_func.__name__,
                             method.im_self,
                             method.im_class)

def unpickleMethod(im_name,
                    im_self,
                    im_class):
    'support function for copy_reg to unpickle method refs'
    try:
        unbound = getattr(im_class,im_name)
        if im_self is None:
            return unbound
        bound=instancemethod(unbound.im_func,
                                 im_self,
                                 im_class)
        return bound
    except AttributeError:
        log.msg("Method",im_name,"not on class",im_class)
        assert im_self is not None,"No recourse: no instance to guess from."
        # Attempt a common fix before bailing -- if classes have
        # changed around since we pickled this method, we may still be
        # able to get it by looking on the instance's current class.
        unbound = getattr(im_self.__class__,im_name)
        log.msg("Attempting fixup with",unbound)
        if im_self is None:
            return unbound
        bound=instancemethod(unbound.im_func,
                                 im_self,
                                 im_self.__class__)
        return bound

copy_reg.pickle(types.MethodType,
                pickleMethod,
                unpickleMethod)

def pickleModule(module):
    'support function for copy_reg to pickle module refs'
    return unpickleModule, (module.__name__,)

def unpickleModule(name):
    'support function for copy_reg to unpickle module refs'
    return __import__(name,None,None,'x')


copy_reg.pickle(types.ModuleType,
                pickleModule,
                unpickleModule)

def pickleStringO(stringo):
    'support function for copy_reg to pickle cStringIO.OutputTypes'
    return unpickleStringO, (stringo.getvalue(), stringo.tell())

def unpickleStringO(val, sek):
    x = cStringIO.StringIO()
    x.write(val)
    x.seek(sek)
    return x

if hasattr(cStringIO, 'OutputType'):
    copy_reg.pickle(cStringIO.OutputType,
                pickleStringO,
                unpickleStringO)
                
def pickleStringI(stringi):
    return unpickleStringI, (stringi.getvalue(), stringi.tell())

def unpickleStringI(val, sek):
    x = cStringIO.StringIO(val)
    x.seek(sek)
    return x


if hasattr(cStringIO, 'InputType'):
    copy_reg.pickle(cStringIO.InputType,
                pickleStringI,
                unpickleStringI)

class Ephemeral:
    """
    This type of object is never persisted; if possible, even references to it
    are eliminated.
    """

    def __getstate__(self):
        print "WARNING: serializing ephemeral", self
        return None

    def __setstate__(self, state):
        print "WARNING: unserializing ephemeral", self.__class__
        self.__class__ = Ephemeral
