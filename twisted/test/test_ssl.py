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

from __future__ import nested_scopes
from twisted.trial import unittest
from twisted.internet import protocol, reactor
from twisted.protocols import basic

from OpenSSL import SSL
from twisted.internet import ssl

import os
import test_tcp


certPath = os.path.join(os.path.split(test_tcp.__file__)[0], "server.pem")

class StolenTCPTestCase(test_tcp.ProperlyCloseFilesTestCase, test_tcp.WriteDataTestCase):
    
    def setUp(self):
        f = protocol.ServerFactory()
        f.protocol = protocol.Protocol
        self.listener = reactor.listenSSL(
            0, f, ssl.DefaultOpenSSLContextFactory(certPath, certPath), interface="127.0.0.1",
        )
        
        f = protocol.ClientFactory()
        f.protocol = test_tcp.ConnectionLosingProtocol
        f.protocol.master = self
        
        L = []
        def connector():
            p = self.listener.getHost()[2]
            ctx = ssl.ClientContextFactory()
            return reactor.connectSSL('127.0.0.1', p, f, ctx)
        self.connector = connector

        self.totalConnections = 0

class ClientTLSContext(ssl.ClientContextFactory):
    isClient = 1
    def getContext(self):
        return SSL.Context(ssl.SSL.TLSv1_METHOD)

class UnintelligentProtocol(basic.LineReceiver):
    pretext = [
        "first line",
        "last thing before tls starts",
        "STARTTLS",
    ]
    
    posttext = [
        "first thing after tls started",
        "last thing ever",
    ]
    
    def connectionMade(self):
        for l in self.pretext:
            self.sendLine(l)

    def lineReceived(self, line):
        if line == "READY":
            self.transport.startTLS(ClientTLSContext())
            for l in self.posttext:
                self.sendLine(l)
            self.transport.loseConnection()
        
class ServerTLSContext(ssl.DefaultOpenSSLContextFactory):
    isClient = 0
    def __init__(self, *args, **kw):
        kw['sslmethod'] = SSL.TLSv1_METHOD
        ssl.DefaultOpenSSLContextFactory.__init__(self, *args, **kw)

class LineCollector(basic.LineReceiver):
    def __init__(self, doTLS):
        self.doTLS = doTLS

    def connectionMade(self):
        self.factory.rawdata = ''
        self.factory.lines = []

    def lineReceived(self, line):
        self.factory.lines.append(line)
        if line == 'STARTTLS':
            self.sendLine('READY')
            if self.doTLS:
                ctx = ServerTLSContext(
                    privateKeyFileName=certPath,
                    certificateFileName=certPath,
                )
                self.transport.startTLS(ctx)
            else:
                self.setRawMode()
    
    def rawDataReceived(self, data):
        self.factory.rawdata += data
        self.factory.done = 1
    
    def connectionLost(self, reason):
        self.factory.done = 1

class TLSTestCase(unittest.TestCase):
    def testTLS(self):
        cf = protocol.ClientFactory()
        cf.protocol = UnintelligentProtocol
        
        sf = protocol.ServerFactory()
        sf.protocol = lambda: LineCollector(1)
        sf.done = 0

        port = reactor.listenTCP(0, sf)
        portNo = port.getHost()[2]
        
        reactor.connectTCP('0.0.0.0', portNo, cf)
        
        i = 0
        while i < 5000 and not sf.done:
            reactor.iterate(0.01)
            i += 1
        
        self.failUnless(sf.done, "Never finished reading all lines")
        self.assertEquals(
            sf.lines,
            UnintelligentProtocol.pretext + UnintelligentProtocol.posttext
        )
    
    def testUnTLS(self):
        cf = protocol.ClientFactory()
        cf.protocol = UnintelligentProtocol
        
        sf = protocol.ServerFactory()
        sf.protocol = lambda: LineCollector(0)
        sf.done = 0

        port = reactor.listenTCP(0, sf)
        portNo = port.getHost()[2]
        
        reactor.connectTCP('0.0.0.0', portNo, cf)
        
        i = 0
        while i < 5000 and not sf.done:
            reactor.iterate(0.01)
            i += 1
        
        self.failUnless(sf.done, "Never finished reading all lines")
        self.assertEquals(
            sf.lines,
            UnintelligentProtocol.pretext
        )
        self.failUnless(sf.rawdata, "No encrypted bytes received")
