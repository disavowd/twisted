# -*- test-case-name: twisted.test.test_formmethod -*-
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
Form-based method objects.

This module contains support for descriptive method signatures that can be used
to format methods.  Currently this is only used by woven.
"""


class InputError(Exception):
    """
    An error occurred with some input.
    """


class FormException(Exception):
    """An error occured calling the form method.
    """
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args)
        self.descriptions = kwargs


class Argument:
    """Base class for form arguments."""

    # default value for argument, if no other default is given
    defaultDefault = None

    def __init__(self, name, default=None, shortDesc=None, longDesc=None, hints=()):
        self.name = name
        if default is None:
            default = self.defaultDefault
        self.default = default
        self.shortDesc = shortDesc
        self.longDesc = longDesc

    def addHint(self, hint):
        self.hints.append(hint)
        hint.added(self)

    def getShortDescription(self):
        return self.shortDesc or self.name.capitalize()

    def getLongDescription(self):
        return self.longDesc or self.shortDesc or "The %s." % self.name

    def coerce(self, val):
        """Convert the value to the correct format."""
        raise UnimplementedError, "implement in subclass"


class String(Argument):
    """A single string.
    """
    defaultDefault = ''

    def coerce(self, val):
        return str(val)


class Text(String):
    """A long string.
    """


class Password(String):
    """A string which should be obscured when input.
    """


class Hidden(String):
    """A string which is not displayed.

    The passed default is used as the value.
    """


class Integer(Argument):
    """A single integer.
    """
    
    defaultDefault = None

    def __init__(self, name, allowNone=1, default=None, shortDesc=None, longDesc=None, hints=()):
        Argument.__init__(self, name, default, shortDesc, longDesc, hints)
        self.allowNone = allowNone
    
    def coerce(self, val):
        if not val.strip() and self.allowNone:
            return None
        try:
            return int(val)
        except ValueError:
            raise InputError, "Invalid integer: %s" % val


class Float(Argument):
    
    defaultDefault = None

    def __init__(self, name, allowNone=1, default=None, shortDesc=None, longDesc=None, hints=()):
        Argument.__init__(self, name, default, shortDesc, longDesc, hints)
        self.allowNone = allowNone

    def coerce(self, val):
        if not val.strip() and self.allowNone:
            return None
        try:
            return float(val)
        except ValueError:
            raise InputError, "Invalid float: %s" % val


class Choice(Argument):
    """The result of a choice between enumerated types.
    """
    def __init__(self, name, choices=[], default=None, shortDesc=None, longDesc=None, hints=()):
        self.choices = choices
        Argument.__init__(self, name, default, shortDesc, longDesc, hints)

    def coerce(self, inIdent):
        for ident, val, desc in self.choices:
            if ident == inIdent:
                return val
        else:
            raise InputError("Invalid Choice: %s" % inIdent)


class Flags(Argument):
    """The result of a checkbox group or multi-menu.
    """
    def __init__(self, name, flags=(), default=(), shortDesc=None, longDesc=None, hints=()):
        self.flags = flags
        Argument.__init__(self, name, default, shortDesc, longDesc, hints)

    def coerce(self, inFlagKeys):
        outFlags = []
        for inFlagKey in inFlagKeys:
            for flagKey, flagVal, flagDesc in self.flags:
                if inFlagKey == flagKey:
                    outFlags.append(flagVal)
                    break
            else:
                raise InputError("Invalid Flag: %s" % inFlagKey)
        return outFlags


class CheckGroup(Flags):
    pass


class RadioGroup(Choice):
    pass


class Boolean(Argument):
    def coerce(self, inVal):
        if not inVal:
            return 0
        lInVal = str(inVal).lower()
        if lInVal in ('no', 'n', 'f', 'false'):
            return 0
        return 1


class Submit(Argument):
    """Submit button or a reasonable facsimile thereof."""

    def __init__(self, name, buttons=["Submit"], reset=0, shortDesc=None, longDesc=None):
        Argument.__init__(self, name, shortDesc=shortDesc, longDesc=longDesc)
        self.buttons = buttons
        self.reset = reset

    def coerce(self, val):
        if val in self.buttons:
            return val
        else:
            raise InputError, "no such action"


class PresentationHint:
    """
    A hint to a particular system.
    """


class MethodSignature:

    def __init__(self, *sigList):
        """
        """
        self.methodSignature = sigList

    def addHintTo(self, **kw):
        for k,v in kw.items():
            for a in self.methodSignature:
                if a.name == k:
                    a.name == k
                    a.addHint(v)
                    continue

    def getArgument(self, name):
        for a in self.methodSignature:
            if a.name == name:
                return a

    def method(self, callable):
        return FormMethod(self, callable)


class FormMethod:
    """A callable object with a signature."""
    
    def __init__(self, signature, callable):
        self.signature = signature
        self.callable = callable

    def getArgs(self):
        return tuple(self.signature.methodSignature)

    def call(self,*args,**kw):
        return self.callable(*args,**kw)

