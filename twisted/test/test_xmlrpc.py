# -*- test-case-name: twisted.test.test_xmlrpc -*-
#
# Twisted, the Framework of Your Internet
# Copyright (C) 2001-2002 Matthew W. Lefkowitz
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
# 

"""Test XML-RPC support."""
try:
    import xmlrpclib
except ImportError:
    xmlrpclib = None
    class XMLRPC: pass
else:
    from twisted.web import xmlrpc
    from twisted.web.xmlrpc import XMLRPC

from twisted.trial import unittest
from twisted.web import server
from twisted.internet import reactor, defer
from twisted.python import log


class Test(XMLRPC):

    def xmlrpc_add(self, a, b):
        return a + b

    def xmlrpc_defer(self, x):
        return defer.succeed(x)

    def xmlrpc_deferFail(self):
        return defer.fail(ValueError())

    def xmlrpc_fail(self):
        raise RuntimeError

    def xmlrpc_fault(self):
        return xmlrpc.Fault(12)


class XMLRPCTestCase(unittest.TestCase):

    def setUp(self):
        self.p = reactor.listenTCP(0, server.Site(Test()))
        self.port = self.p.getHost()[2]

    def tearDown(self):
        self.p.stopListening()
        reactor.iterate()
        reactor.iterate()

    def proxy(self):
        return xmlrpc.Proxy("http://localhost:%d/" % self.port)
    
    def testResults(self):
        x = self.proxy().callRemote("add", 2, 3)
        self.assertEquals(unittest.deferredResult(x), 5)
        x = self.proxy().callRemote("defer", "a")
        self.assertEquals(unittest.deferredResult(x), "a")

    def testErrors(self):
        for methodName in "fail", "deferFail", "fault", "noSuchMethod":
            l = []
            d = self.proxy().callRemote("fail").addErrback(l.append)
            while not l:
                reactor.iterate()
            l[0].trap(xmlrpc.Fault)
        log.flushErrors(RuntimeError)


if not xmlrpclib:
    del XMLRPCTestCase
