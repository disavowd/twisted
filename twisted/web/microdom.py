# -*- test-case-name: twisted.test.test_persisted -*-

"""Micro Document Object Model: a partial DOM implementation with SUX.

This is an implementation of what we consider to be the useful subset of the
DOM.  The chief advantage of this library is that, not being burdened with
standards compliance, it can remain very stable between versions.  We can also
implement utility 'pythonic' ways to access and mutate the XML tree.

Since this has not subjected to a serious trial by fire, it is not recommended
to use this outside of Twisted applications.  However, it seems to work just
fine for the documentation generator, which parses a fairly representative
sample of XML.

"""

from twisted.protocols.sux import XMLParser

import copy

class Node:
    def __init__(self, parentNode=None):
        self.parentNode = parentNode
        self.childNodes = []
        self.nodeName = str(self.__class__)

    def writexml(self, stream, indent='', addindent='', newl=''):
        raise NotImplementedError()
    def toxml(self, indent='', newl=''):
        from cStringIO import StringIO
        s = StringIO()
        self.writexml(s, '', indent, newl)
        rv = s.getvalue()
        return rv
    def toprettyxml(self, indent='\t', newl='\n'):
        return self.toxml(indent, newl)
    def cloneNode(self, deep):
        if deep:
            return copy.deepcopy(self)
        else:
            return copy.copy(self)

    def appendChild(self, child):
        self.childNodes.append(child)
        child.parentNode = self
    def removeChild(self, child):
        self.childNodes.remove(child)
        child.parentNode = None
    def replaceChild(self, newChild, oldChild):
        if newChild.parentNode:
            newChild.parentNode.removeChild(newChild)
        assert oldChild.parentNode is self
        self.childNodes[self.childNodes.index(oldChild)] = newChild
        oldChild.parentNode = None
        newChild.parentNode = self

class _tee:
    def __init__(self, f):
        self.f = f

    def write(self, data):
        import sys
        self.f.write(data)
        sys.stdout.write(data)
        sys.stdout.flush()

from twisted.python.reflect import Accessor
class Document(Node, Accessor):
    def __init__(self, documentElement=None):
        Node.__init__(self)
        if documentElement:
            self.appendChild(documentElement)

    def get_documentElement(self):
        return self.childNodes[0]

    def appendChild(self, c):
        assert not self.childNodes, "Only one element per document."
        Node.appendChild(self, c)
    def writexml(self, stream, indent='', addindent='', newl=''):
        stream.write('<?xml version="1.0"?>' + newl)
        self.documentElement.writexml(stream, indent, addindent, newl)

    # of dubious utility (?)
    def createElement(self, name):
        return Element(name)

class EntityReference(Node):
    def __init__(self, eref, parentNode=None):
        Node.__init__(self, parentNode)
        self.eref = eref
        self.nodeValue = self.data = "&" + eref + ";"

    def writexml(self, stream, indent='', addindent='', newl=''):
        stream.write(self.nodeValue)

class CharacterData(Node):
    def __init__(self, data, parentNode=None):
        Node.__init__(self, parentNode)
        self.data = self.nodeValue = data

##     def cloneNode(self, deep):
##         return self.__class__(self.data)

class Text(CharacterData):
    def writexml(self, stream, indent='', addindent='', newl=''):
        stream.write(self.nodeValue)

class CDATASection(CharacterData):
    def writexml(self, stream, indent='', addindent='', newl=''):
        stream.write("<![CDATA[")
        stream.write(self.nodeValue)
        stream.write("]]>")

class Element(Node):
    def __init__(self, tagName, attributes=None, parentNode=None):
        Node.__init__(self, parentNode)
        if attributes is None:
            self.attributes = {}
        else:
            self.attributes = attributes
            for k, v in self.attributes.items():
                self.attributes[k] = v.replace('&quot;', '"')
        self.nodeName = self.tagName = tagName

    def getAttribute(self, name):
        return self.attributes[name]
    def setAttribute(self, name, attr):
        self.attributes[name] = attr
    def hasAttribute(self, name):
        return self.attributes.has_key(name)

    def appendChild(self, child):
        # should we be checking the type of the child?
        self.childNodes.append(child)

    def writexml(self, stream, indent='', addindent='', newl=''):
        # write beginning
        stream.write("<")
        stream.write(self.tagName)
        for attr, val in self.attributes.items():
            stream.write(" ")
            stream.write(attr)
            stream.write("=")
            stream.write('"')
            stream.write(val.replace('"', '&quot;'))
            stream.write('"')
        if self.childNodes:
            stream.write(">"+newl+addindent)
            for child in self.childNodes:
                child.writexml(stream, indent+addindent, addindent, newl)
            stream.write("</")
            stream.write(self.tagName)
            stream.write(">")
        else:
            stream.write("/>")
        

class MicroDOMParser(XMLParser):
    # Sorta SAX-ish API
    def __init__(self):
        self.elementstack = []
        self.documents = []

    def _getparent(self):
        if self.elementstack:
            parent = self.elementstack[-1]
        else:
            parent = None
        return parent

    def gotTagStart(self, name, attributes):
        parent = self._getparent()
        el = Element(name, attributes, parent)
        self.elementstack.append(el)
        if parent:
            parent.appendChild(el)

    def gotText(self, data):
        parent = self._getparent()
        te = Text(data, parent)
        if parent:
            parent.appendChild(te)

    def gotEntityReference(self, entityRef):
        parent = self._getparent()
        er = EntityReference(entityRef, parent)
        if parent:
            parent.appendChild(er)

    def gotCData(self, cdata):
        parent = self._getparent()
        cd = CDATASection(cdata, parent)
        if parent:
            parent.appendChild(cd)

    def gotTagEnd(self, name):
        el = self.elementstack.pop()
        if el.tagName != name:
            raise Exception("Foo! %s" % str(self.saveMark()))
        if not self.elementstack:
            self.documents.append(el)

def parse(readable):
    mdp = MicroDOMParser()
    mdp.makeConnection(None)
    r = readable.read(1024)
    while r:
        mdp.dataReceived(r)
        r = readable.read(1024)
    d = mdp.documents[0]
    return Document(d)

def parseString(st):
    mdp = MicroDOMParser()
    mdp.makeConnection(None)
    mdp.dataReceived(st)
    d = mdp.documents[0]
    return Document(d)

# parseString("<!DOCTYPE suck it> <foo> testing testing, one two <bar/> </foo>").toxml()

from types import ListType as NodeList

