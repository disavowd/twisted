
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
I am a support module for making SSH servers with mktap.
"""

from twisted.secsh import factory
from twisted.python import usage
import sys

class Options(usage.Options):
    synopsis = "Usage: mktap sshd [-i <interface>] [-p <port>] [-d <dir>]"
    optParameters = [["interface", "i", "127.0.0.1", "local interface to which we listen"],
                  ["port", "p", 5822],
                  ["data", "d", "/etc", "directory to look for host keys in"]]

    longdesc = "Makes a SSH server.."

def updateApplication(app, config):
    if config.interface != "127.0.0.1":
        print
        print "WARNING:"
        print "  You have chosen to listen on a non-local interface."
        print "  This may allow intruders to access your local network"
        print "  if you run this on a firewall."
        print
    t =factory.OpenSSHFactory()
    t.dataRoot = config.opts['data']
    portno = int(config.opts['port'])
    app.listenTCP(portno, t, interface=config.opts['interface'])
