
# System Imports
import os
import select
import traceback
import sys
import copy
import signal
from errno import EINTR

CONNECTION_LOST = -1
CONNECTION_DONE = -2

theApplication = None

# Twisted Imports

from twisted.python import threadable, log
threadable.requireInit()

# Sibling Imports

import task, tcp

class Application(log.Logger):
    running = 0
    def __init__(self, name, uid=None, gid=None):
        self.name = name
        self.ports = []
        self.delayeds = []
        if os.name == "posix":
            self.uid = uid or os.getuid()
            self.gid = gid or os.getgid()

    def __repr__(self):
        return "<%s app>" % self.name
    
    def __getstate__(self):
        dict = copy.copy(self.__dict__)
        if dict.has_key("running"):
            del dict['running']
        return dict

    def listenOn(self, port, factory):
        """
        Connects a given protocol factory to the given numeric TCP/IP port.
        """
        self.addPort(tcp.Port(port, factory))

    def addPort(self, port):
        """
        Adds a listening port (an instance of a twisted.internet.tcp.Port) to
        this Application, to be bound when it's running.
        """
        self.ports.append(port)
        if self.running:
            port.startListening()

    def addDelayed(self, delayed):
        """
        Adds a twisted.python.delay.Delayed object for execution in my event
        loop.
        
        The timeout for select() will be calculated based on the sum of all
        Delayed instances attached to me, using their 'ticktime' attribute.  In
        this manner, delayed instances should have their various callbacks
        called approximately when they're supposed to be (based on when they
        were registered).

        This is not hard realtime by any means; depending on server load, the
        callbacks may be called in more or less time.  However, 'simulation
        time' for each Delayed instance will be monotonically increased on a
        regular basis.
        
        See the documentation for twisted.python.delay.Delayed for details.
        """
        self.delayeds.append(delayed)
        if running:
            delayeds.append(delayed)

    def setUID(self):
        if hasattr(os, 'getgid'):
            if not os.getgid():
                os.setgid(self.gid)
                os.setuid(self.uid)
                log.msg('set uid/gid %s/%s' % (self.uid, self.gid))

    def shutDownSave(self):
        self.save("shutdown")

    def save(self, tag=None):
        from cPickle import dump
        if tag:
            filename = self.name+'-'+tag+'-2.spl'
            finalname = self.name+'-'+tag+'.spl'
        else:
            filename = self.name+"-2.spl"
            finalname = self.name+".spl"
        log.msg("Saving "+self.name+" application to "+finalname+"...")
        f = open(filename, 'wb')
        dump(self, f, 1)
        f.flush()
        f.close()
        os.rename(filename, finalname)
        log.msg("Saved.")

    def logPrefix(self):
        return self.name+" application"

    def run(self):
        """Run this application, running the main loop if necessary.
        """
        if not self.running:
            threadable.dispatcher.own(self)
            delayeds.extend(self.delayeds)
            shutdowns.append(self.shutDownSave)
            for port in self.ports:
                port.startListening()
            self.running = 1
            threadable.dispatcher.disown(self)
        if not running:
            threadable.dispatcher.own(self)
            self.setUID()
            run()
            threadable.dispatcher.disown(self)

reads = {}
writes = {}
running = None
delayeds = [task.theScheduler]
shutdowns = []

def shutDown(a=None, b=None):
    """Save a copy of this Selector to disk in SHUTDOWN.spl and exit.

    This is called by various signal handlers which should cause the
    process to exit.
    """
    global running
    running = 0
    log.msg('Starting Shutdown Sequence.')
    threadable.dispatcher.stop()
    for callback in shutdowns:
        callback()


def doSelect(timeout,
             # Since this loop should really be as fast as possible, I'm
             # caching these global attributes so the interpreter will hit them
             # in the local namespace.
             reads=reads,
             writes=writes,
             rhk=reads.has_key,
             whk=writes.has_key,
             own=threadable.dispatcher.own,
             disown=threadable.dispatcher.disown):
    """Run one iteration of the I/O monitor loop.

    This will run all selectables who had input or output readiness waiting
    for them.
    """
    while 1:
        try:
            r, w, ignored = select.select(reads.keys(),
                                          writes.keys(),
                                          [], timeout)
            break
        except select.error,se:
            if se.args[0] == EINTR:
                # If this is just an interrupted system call, continue on
                # unless it was generated by a signal handler which will
                # set running to false.
                if not running:
                    return
                # If the timeout is 0 anyway, just bail.
                if not timeout:
                    return
            else:
                raise

    for selectables, method, dict in ((r, "doRead", reads),
                                      (w,"doWrite", writes)):
        hkm = dict.has_key
        for selectable in selectables:
            # if this was disconnected in another thread, kill it.
            if not hkm(selectable):
                continue
            # This for pausing input when we're not ready for more.
            own(selectable)
            try:
                why = getattr(selectable, method)()
                handfn = getattr(selectable, 'fileno', None)
                if not handfn or handfn() == -1:
                    why = CONNECTION_LOST
            except:
                traceback.print_exc(file=log.logfile)
                why = CONNECTION_LOST
            if why:
                removeReader(selectable)
                removeWriter(selectable)
                try:
                    selectable.connectionLost()
                except:
                    traceback.print_exc(file=log.logfile)
            disown(selectable)


def iterate():
    """Do one iteration of the main loop.

    I will run any simulated (delayed) code, and process any pending I/O.
    I will not block.  This is meant to be called from a high-freqency
    updating loop function like the frame-processing function of a game.
    """
    for delayed in delayeds:
        delayed.runUntilCurrent()
    doSelect(0)
    threadable.dispatcher.work()

def run():
    """Run input/output and dispatched/delayed code.

    This call never returns.  It is the main loop which runs threadable workers
    (see twisted.threadable), delayed timers (see twisted.python.delay and
    addDelayed), and the I/O monitor (doSelect).
    """
    global running
    running = 1
    threadable.registerAsIOThread()
    # Register signal handlers on platforms that support them.
    if os.name != 'java':
        signal.signal(signal.SIGINT, shutDown)
        signal.signal(signal.SIGTERM, shutDown)
        if os.name == 'posix':
            signal.signal(signal.SIGCHLD, process.reapProcess)
            
    work = threadable.dispatcher.work
    try:
        try:
            while running:
                # Advance simulation time in delayed event
                # processors.
                timeout = None
                for delayed in delayeds:
                    delayed.runUntilCurrent()
                    newTimeout = delayed.timeout()
                    if ((newTimeout is not None) and
                        ((timeout is None) or
                         (newTimeout < timeout))):
                        timeout = newTimeout
                threadable.dispatcher.work()
                doSelect(timeout)
        except select.error:
            log.msg('shutting down after select() loop interruption')
            if running:
                log.msg('Warning!  Shutdown not called properly!')
                traceback.print_exc(file=log.logfile)
                shutDown()
            if os.name =='nt':
                log.msg("(Logging traceback for WinXX exception info)")
                traceback.print_exc(file=log.logfile)
        except:
            log.msg("Unexpected error in Selector.run.")
            traceback.print_exc(file=log.logfile)
            shutDown()
            raise
        else:
            log.msg('Select loop terminated.')

    finally:
        for reader in reads.keys():
            if reads.has_key(reader):
                del reads[reader]
            if writes.has_key(reader):
                del writes[reader]
            threadable.dispatcher.own(reader)
            try:
                reader.connectionLost()
            except:
                traceback.print_exc(file=log.logfile)
            threadable.dispatcher.disown(reader)

def addReader(reader):
    """Add a FileDescriptor for notification of data available to read.
    """
    reads[reader] = 1

def addWriter(writer):
    """Add a FileDescriptor for notification of data available to write.
    """
    writes[writer] = 1

def removeReader(reader):
    """Remove a Selectable for notification of data available to read.
    """
    if reads.has_key(reader):
        del reads[reader]

def removeWriter(writer):
    """Remove a Selectable for notification of data available to write.
    """
    if writes.has_key(writer):
        del writes[writer]

if os.name == 'nt':
    """redefine iterate on WinXX to handle wierd error case when passing empty lists to select
    """
    def iterate():
        for delayed in delayeds:
            delayed.runUntilCurrent()
        if (not reads) and (not writes):
            pass
        else:
            doSelect(0)
        threadable.dispatcher.work()

if threadable.threaded:
    if os.name == 'nt':
        class _Waker:
            """I am a workaround for the lack of pipes on win32.

            I am a pair of connected sockets which can wake up the main loop
            from another thread.
            """
            def __init__(self):
                """Initialize.
                """
                # Following select_trigger (from asyncore)'s example;
                address = ("127.0.0.1",19939)
                server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.setsockopt(socket.IPPROTO_TCP, 1, 1)
                server.bind(address)
                server.listen(1)
                client.connect(address)
                reader, clientaddr = server.accept()
                client.setblocking(1)
                reader.setblocking(0)
                self.r = reader
                self.w = client
                self.fileno = self.r.fileno

            def wakeUp(self):
                """Send a byte to my connection.
                """
                self.w.send('x')

            def doRead(self):
                """Read some data from my connection.
                """
                self.r.recv(8192)
    else:
        class _Waker:
            """This class provides a simple interface to wake up the select() loop.

            This is necessary only in multi-threaded programs.
            """
            def __init__(self):
                """Initialize.
                """
                i, o = os.pipe()
                self.i = os.fdopen(i,'r')
                self.o = os.fdopen(o,'w')
                self.fileno = self.i.fileno

            def doRead(self):
                """Read one byte from the pipe.
                """
                self.i.read(1)

            def wakeUp(self):
                """Write one byte to the pipe, and flush it.
                """
                self.o.write('x')
                self.o.flush()

            def connectionLost(self):
                """Close both ends of my pipe.
                """
                self.i.close()
                self.o.close()

    waker = _Waker()
    addReader(waker)
    def wakeUp():
        if not threadable.isInIOThread():
            waker.wakeUp()
            
    def addReader(reader):
        """Selector.addReader(selectable) -> None
        Adds a Selectable to the list of objects monitored for data being
        available to read. (waking up the main I/O thread if necessary)"""
        reads[reader] = 1
        wakeUp()

    def addWriter(writer):
        """Selector.addWriter(selectable) -> None
        Adds a Selectable to the list of objects monitored for data being
        available to write. (waking up the main I/O thread if necessary)"""
        writes[writer] = 1
        wakeUp()

# Sibling Import
import process
