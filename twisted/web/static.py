
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

"""I deal with static resources.
"""


# System Imports
import os, stat, string
import cStringIO
import traceback
import types
StringIO = cStringIO
del cStringIO
import urllib

# Sibling Imports
import server
import error
import resource
import widgets

# Twisted Imports
from twisted.protocols import http
from twisted.python import threadable, log, components, failure
from twisted.internet import abstract, interfaces, defer
from twisted.spread import pb
from twisted.persisted import styles

class Data(resource.Resource):
    """
    This is a static, in-memory resource.
    """

    def __init__(self, data, type):
        resource.Resource.__init__(self)
        self.data = data
        self.type = type

    def render(self, request):
        request.setHeader("content-type", self.type)
        if request.method == "HEAD":
            request.setHeader("content-length", len(self.data))
            return ''
        return self.data

def addSlash(request):
    return "http%s://%s%s/" % (
        request.isSecure() and 's' or '',
        request.getHeader("host"),
        (string.split(request.uri,'?')[0]))

def redirectTo(URL, request):
    request.redirect(URL)
    return """
<html>
    <head>
        <meta http-equiv=\"refresh\" content=\"0;URL=%(url)s\">
    </head>
    <body bgcolor=\"#FFFFFF\" text=\"#000000\">
    <!- The user\'s browser must be incredibly feeble if they have to click...-->
        Click <a href=\"%(url)s\">here</a>.
    </body>
</html>
""" % {'url': URL}

class Redirect(resource.Resource):
    def __init__(self, request):
        resource.Resource.__init__(self)
        self.url = addSlash(request)

    def render(self, request):
        return redirectTo(self.url, request)

from twisted.internet.interfaces import IServiceCollection
from twisted.internet.app import ApplicationService

class Registry(components.Componentized):
    """
    I am a Componentized object that will be made available to internal Twisted
    file-based dynamic web content such as .rpy and .epy scripts.
    """
    def _grabService(self, svc, sclas):
        """
        Find an instance of a particular class in a service collection and all
        subcollections.
        """
        for s in svc.services.values():
            if isinstance(s, sclas):
                return s
            if components.implements(s, IServiceCollection):
                ss = self._grabService(s, sclas)
                if ss:
                    return ss

    def getComponent(self, interface):
        """
        Very similar to Componentized.getComponent, with a little magic.

        This adds the additional default behavior that if no component already
        exists and 'interface' is a subclass of
        L{twisted.internet.app.ApplicationService}, it will automatically scan
        through twisted.internet.app.theApplication and look for instances of
        'interface'.

        This has the general effect that if your web script (in an RPY, EPY, or
        anywhere else that a Registry is present) wishes to locate a Service in
        a default webserver, it can say 'registry.getComponent(MyServiceClass)'
        and if there is a service of that type registered with the Application,
        it will be found.  Additionally, in a more complex server, the registry
        can be explicitly given a service to locate for that interface using
        setComponent(MyServiceClass, myServiceInstance). Separate File
        instances can be used to represent access to different services.
        """
        c = components.Componentized.getComponent(self, interface)
        if c is not None:
            return c
        elif issubclass(interface, ApplicationService):
            from twisted.internet.app import theApplication
            gs = self._grabService(theApplication, interface)
            if gs:
                self.setComponent(interface, gs)
                return gs


def _upgradeRegistry(registry):
    from twisted.internet import app
    registry.setComponent(interfaces.IServiceCollection,
                          app.theApplication)


class File(resource.Resource, styles.Versioned):
    """
    File is a resource that represents a plain non-interpreted file.
    It's constructor takes a file path.
    """

    # we don't implement IConfigCollection
    __implements__ = resource.IResource

    #argh, we need a MIME db interface
    contentTypes = {
        ".css": "text/css",
        ".exe": "application/x-executable",
        ".flac": "audio/x-flac",
        ".gif": "image/gif",
        ".gtar": "application/x-gtar",
        ".html": "text/html",
        ".htm": "text/html",
        ".java": "text/plain",
        ".jpeg": "image/jpeg",
        ".jpg": "image/jpeg",
        ".lisp": "text/x-lisp",
        ".mp3":  "audio/mpeg",
        ".oz": "text/x-oz",
        ".ogg": "application/x-ogg",
        ".pdf": "application/x-pdf",
        ".png": "image/png",
        ".py": "text/x-python",
        ".swf": "application/x-shockwave-flash",
        ".tar": "application/x-tar",
        ".tgz": "application/x-gtar",
        ".tif": "image/tiff",
        ".tiff": "image/tiff",
        ".txt": "text/plain",
        ".zip": "application/x-zip",
        }

    contentEncodings = {
        ".gz" : "application/x-gzip",
        ".bz2": "appliation/x-bzip2"
        }

    processors = {}

    indexNames = ["index", "index.html", "index.trp", "index.rpy"]

    ### Versioning

    persistenceVersion = 5

    def upgradeToVersion5(self):
        if not isinstance(self.registry, Registry):
            self.registry = Registry()
            from twisted.internet import reactor
            reactor.callLater(0, _upgradeRegistry, self.registry)

    def upgradeToVersion4(self):
        if not hasattr(self, 'registry'):
            self.registry = {}

    def upgradeToVersion3(self):
        if not hasattr(self, 'allowExt'):
            self.allowExt = 0

    def upgradeToVersion2(self):
        self.defaultType = "text/html"

    def upgradeToVersion1(self):
        if hasattr(self, 'indexName'):
            self.indexNames = [self.indexName]
            del self.indexName

    def __init__(self, path, defaultType="text/html", allowExt=0, registry=None):
        """Create a file with the given path.
        """
        resource.Resource.__init__(self)
        self.path = path
        # Remove the dots from the path to split
        p = os.path.abspath(path)
        p, ext = os.path.splitext(p)
        self.encoding = self.contentEncodings.get(string.lower(ext))
        # if there was an encoding, get the next suffix
        if self.encoding is not None:
            p, ext = os.path.splitext(p)
        self.defaultType = defaultType
        self.allowExt = allowExt
        if not registry:
            self.registry = Registry()
        else:
            self.registry = registry

        self.type = self.contentTypes.get(string.lower(ext), defaultType)

    def getChild(self, path, request):
        """See twisted.web.Resource.getChild.
        """
        if path == '..':
            return error.NoResource("Invalid request URL.")

        childPath = os.path.join(self.path, path)
        try:
            mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime =\
                  os.stat(childPath)
        except OSError:
            mode=0

        if os.path.isdir(childPath): # 'stat.S_ISDIR(mode)' is faster but doesn't work on jython
            # If someone is looking for children with a PathReferenceContext,
            # the request won't have a prepath, and we shouldn't do this kind
            # of mangling anyway because it has already been done.
            if hasattr(request, 'postpath') and not request.postpath and request.uri[-1] != '/':
                return Redirect(request)
            if os.path.exists(childPath):
                if hasattr(request, 'postpath') and not request.postpath and not self.getIndex(request):
                    return widgets.WidgetPage(DirectoryListing(self.path))

        ##
        # If we're told to, allow requests for 'foo' to return
        # 'foo.bar'.
        ##
        if not os.path.exists(childPath):
            if self.allowExt and path and os.path.isdir(self.path):
                for fn in os.listdir(self.path):
                    if os.path.splitext(fn)[0]==path:
                        log.msg('    Returning %s' % fn)
                        newpath = os.path.join(self.path, fn)
                childPath = os.path.join(self.path, path)

        if not os.path.exists(childPath):
            # Before failing ask index.foo if it knows about this child
            index = self.getIndex(request)
            if index:
                child = index.getChild(path, request)
                if child:
                    return child
            return error.NoResource("File not found.")

        # forgive me, oh lord, for I know not what I do
        p, ext = os.path.splitext(childPath)
        processor = self.processors.get(ext)
        if processor:
            #the `registry' argument is new, so we have to do this nasty hack
            try: 
                p = processor(childPath, self.registry)
            except TypeError: # this isn't very robust :(
                potentialErrorMessage = widgets.formatFailure(failure.Failure())
                try:
                    p = processor(childPath)
                except TypeError:
                    #So it raised TypeError _both_ times, that means it's
                    #probably not because of processor's signature
                    return error.ErrorPage(500, "Internal Error", potentialErrorMessage)
                import warnings
                #this really should be a very short phase-out period; I doubt there are even any third-party processors
                warnings.warn("warning: Processor %s doesn't use the signature (childPath, registry), it should." % processor,
                              category=DeprecationWarning, stacklevel=2)
                              

            if components.implements(p, resource.IResource):
                return p
            else:
                adapter = components.getAdapter(p, resource.IResource, None)
                if not adapter:
                    raise NotImplementedError("%s instance does not implement "
                                              "IResource, and there is no "
                                              "registered adapter." %
                                              p.__class__)
                return adapter

        f = self.createSimilarFile(childPath)
        f.processors = self.processors
        f.indexNames = self.indexNames[:]
        return f

    # methods to allow subclasses to e.g. decrypt files on the fly:    
    def openForReading(self):
        """Open a file and return it."""
        return open(self.path,'rb')

    def getFileSize(self):
        """Return file size."""
        return os.path.getsize(self.path)


    def render(self, request):
        """You know what you doing."""

        if not os.path.exists(self.path):
            return error.NoResource("File not found.").render(request)

        mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime =\
              os.stat(self.path)

        #for content-length
        fsize = size = self.getFileSize()

        if os.path.isdir(self.path): # stat.S_ISDIR(mode) (see above)
            if self.path[-1] == os.sep:
                index = self.getIndex(request)
                if index:
                    return index.render(request)
            else:
                return self.redirect(request)

        request.setHeader('accept-ranges','bytes')

        if self.type:
            request.setHeader('content-type', self.type)
        if self.encoding:
            request.setHeader('content-encoding', self.encoding)

        try:
            f = self.openForReading()
        except IOError, e:
            import errno
            if e[0] == errno.EACCES:
                return error.ForbiddenResource().render(request)
            else:
                raise

        if request.setLastModified(mtime) is http.CACHED:
            return ''

        try:
            range = request.getHeader('range')

            if range is not None:
                # This is a request for partial data...
                bytesrange = string.split(range, '=')
                assert bytesrange[0] == 'bytes',\
                       "Syntactically invalid http range header!"
                start, end = string.split(bytesrange[1],'-')
                if start:
                    f.seek(int(start))
                if end:
                    end = int(end)
                    size = end
                else:
                    end = size
                request.setResponseCode(http.PARTIAL_CONTENT)
                request.setHeader('content-range',"bytes %s-%s/%s " % (
                    str(start), str(end), str(size)))
                #content-length should be the actual size of the stuff we're
                #sending, not the full size of the on-server entity.
                fsize = end - int(start)

            request.setHeader('content-length',fsize)
        except:
            traceback.print_exc(file=log.logfile)

        if request.method == 'HEAD':
            return ''

        # return data
        FileTransfer(f, size, request)
        # and make sure the connection doesn't get closed
        return server.NOT_DONE_YET

    def redirect(self, request):
        return redirectTo(addSlash(request), request)

    def getIndex(self, request):
        if not hasattr(request, 'prepath'): return
        for name in self.indexNames:
            ##
            # This next step is so urls like
            #     /foo/bar/baz/
            # will be represented (internally) as
            #     ['foo','bar','baz','index.qux']
            # So that request.childLink() will work correctly.
            ##
            if os.path.exists(os.path.join(self.path, name)):
                request.prepath[-1] = name
                request.acqpath[-1] = name
                return self.getChild(name, request)

    def listNames(self):
        if not os.path.isdir(self.path): return []
        directory = os.listdir(self.path)
        directory.sort()
        return directory

    def listEntities(self):
        return map(lambda fileName, self=self: self.createSimilarFile(os.path.join(self.path, fileName)), self.listNames())

    def createPickleChild(self, name, child):
        if not os.path.isdir(self.path):
            resource.Resource.putChild(self, name, child)
        # xxx use a file-extension-to-save-function dictionary instead
        if type(child) == type(""):
            fl = open(os.path.join(self.path, name), 'w')
            fl.write(child)
        else:
            if '.' not in name:
                name = name + '.trp'
            fl = open(os.path.join(self.path, name), 'w')
            from pickle import Pickler
            pk = Pickler(fl)
            pk.dump(child)
        fl.close()

    def createSimilarFile(self, path):
        return self.__class__(path, self.defaultType, self.allowExt, self.registry)


class DirectoryListing(widgets.StreamWidget):
    def __init__(self, pathname):
        self.path = pathname

    def getTitle(self, request):
        return "Directory Listing For %s" % request.path

    def stream(self, write, request):
        write("<ul>\n")
        directory = os.listdir(self.path)
        directory.sort()
        for path in directory:
            url = urllib.quote(path, "/:")
            if os.path.isdir(os.path.join(self.path, path)):
                url = url + '/'
            write('<li><a href="%s">%s</a></li>' % (url, path))
        write("</ul>\n")

class FileTransfer(pb.Viewable):
    """
    A class to represent the transfer of a file over the network.
    """
    request = None
    def __init__(self, file, size, request):
        self.file = file
        self.size = size
        self.request = request
        request.registerProducer(self, 0)

    def resumeProducing(self):
        if not self.request:
            return
        self.request.write(self.file.read(abstract.FileDescriptor.bufferSize))
        if self.file.tell() == self.size:
            self.request.unregisterProducer()
            self.request.finish()
            self.request = None

    def pauseProducing(self):
        pass

    def stopProducing(self):
        self.file.close()
        self.request = None

    # Remotely relay producer interface.

    def view_resumeProducing(self, issuer):
        self.resumeProducing()

    def view_pauseProducing(self, issuer):
        self.pauseProducing()

    def view_stopProducing(self, issuer):
        self.stopProducing()


    synchronized = ['resumeProducing', 'stopProducing']

threadable.synchronize(FileTransfer)
