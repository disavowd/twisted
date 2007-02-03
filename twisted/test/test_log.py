# Copyright (c) 2001-2004,2007 Twisted Matrix Laboratories.
# See LICENSE for details.

import os, sys, time

from twisted.trial import unittest

from twisted.python import log
from twisted.python import failure

class LogTest(unittest.TestCase):

    def setUp(self):
        self.catcher = []
        log.addObserver(self.catcher.append)

    def tearDown(self):
        log.removeObserver(self.catcher.append)

    def testObservation(self):
        catcher = self.catcher
        log.msg("test", testShouldCatch=True)
        i = catcher.pop()
        self.assertEquals(i["message"][0], "test")
        self.assertEquals(i["testShouldCatch"], True)
        self.failUnless(i.has_key("time"))
        self.assertEquals(len(catcher), 0)

    def testContext(self):
        catcher = self.catcher
        log.callWithContext({"subsystem": "not the default",
                             "subsubsystem": "a",
                             "other": "c"},
                            log.callWithContext,
                            {"subsubsystem": "b"}, log.msg, "foo", other="d")
        i = catcher.pop()
        self.assertEquals(i['subsubsystem'], 'b')
        self.assertEquals(i['subsystem'], 'not the default')
        self.assertEquals(i['other'], 'd')
        self.assertEquals(i['message'][0], 'foo')

    def testErrors(self):
        for e, ig in [("hello world","hello world"),
                      (KeyError(), KeyError),
                      (failure.Failure(RuntimeError()), RuntimeError)]:
            log.err(e)
            i = self.catcher.pop()
            self.assertEquals(i['isError'], 1)
            self.flushLoggedErrors(ig)

    def testErrorsWithWhy(self):
        for e, ig in [("hello world","hello world"),
                      (KeyError(), KeyError),
                      (failure.Failure(RuntimeError()), RuntimeError)]:
            log.err(e, 'foobar')
            i = self.catcher.pop()
            self.assertEquals(i['isError'], 1)
            self.assertEquals(i['why'], 'foobar')
            self.flushLoggedErrors(ig)


    def testErroneousErrors(self):
        L1 = []
        L2 = []
        log.addObserver(lambda events: L1.append(events))
        log.addObserver(lambda events: 1/0)
        log.addObserver(lambda events: L2.append(events))
        log.msg("Howdy, y'all.")

        # XXX - use private _flushErrors so we don't also catch
        # the deprecation warnings
        excs = [f.type for f in log._flushErrors(ZeroDivisionError)]
        self.assertEquals([ZeroDivisionError], excs)

        self.assertEquals(len(L1), 2)
        self.assertEquals(len(L2), 2)

        self.assertEquals(L1[1]['message'], ("Howdy, y'all.",))
        self.assertEquals(L2[0]['message'], ("Howdy, y'all.",))

        # The observer has been removed, there should be no exception
        log.msg("Howdy, y'all.")

        self.assertEquals(len(L1), 3)
        self.assertEquals(len(L2), 3)
        self.assertEquals(L1[2]['message'], ("Howdy, y'all.",))
        self.assertEquals(L2[2]['message'], ("Howdy, y'all.",))


class FakeFile(list):
    def write(self, bytes):
        self.append(bytes)

    def flush(self):
        pass

class EvilStr:
    def __str__(self):
        1/0

class EvilRepr:
    def __str__(self):
        return "Happy Evil Repr"
    def __repr__(self):
        1/0

class EvilReprStr(EvilStr, EvilRepr):
    pass

class LogPublisherTestCaseMixin:
    def setUp(self):
        # Fuck you Python.
        reload(sys)
        self._origEncoding = sys.getdefaultencoding()
        sys.setdefaultencoding('ascii')

        self.out = FakeFile()
        self.lp = log.LogPublisher()
        self.flo = log.FileLogObserver(self.out)
        self.lp.addObserver(self.flo.emit)

    def tearDown(self):
        for chunk in self.out:
            self.failUnless(isinstance(chunk, str), "%r was not a string" % (chunk,))
        # Fuck you very much.
        sys.setdefaultencoding(self._origEncoding)
        del sys.setdefaultencoding



class LogPublisherTestCase(LogPublisherTestCaseMixin, unittest.TestCase):
    def testSingleString(self):
        self.lp.msg("Hello, world.")
        self.assertEquals(len(self.out), 1)


    def testMultipleString(self):
        # Test some stupid behavior that will be deprecated real soon.
        # If you are reading this and trying to learn how the logging
        # system works, *do not use this feature*.
        self.lp.msg("Hello, ", "world.")
        self.assertEquals(len(self.out), 1)


    def testSingleUnicode(self):
        self.lp.msg(u"Hello, \N{VULGAR FRACTION ONE HALF} world.")
        self.assertEquals(len(self.out), 1)
        self.assertIn('with str error Traceback', self.out[0])
        self.assertIn('UnicodeEncodeError', self.out[0])



class FileObserverTestCase(LogPublisherTestCaseMixin, unittest.TestCase):
    def test_getTimezoneOffset(self):
        """
        Attempt to verify that L{FileLogObserver.getTimezoneOffset} returns
        correct values for the current C{TZ} environment setting.  Do this
        by setting C{TZ} to various well-known values and asserting that the
        reported offset is correct.
        """
        localDaylightTuple = (2006, 6, 30, 0, 0, 0, 4, 181, 1)
        utcDaylightTimestamp = time.mktime(localDaylightTuple)
        localStandardTuple = (2007, 1, 31, 0, 0, 0, 2, 31, 0)
        utcStandardTimestamp = time.mktime(localStandardTuple)

        originalTimezone = os.environ.get('TZ', None)
        try:
            # Test something west of UTC
            os.environ['TZ'] = 'US/Eastern'
            time.tzset()
            self.assertEqual(
                self.flo.getTimezoneOffset(utcDaylightTimestamp),
                14400)
            self.assertEqual(
                self.flo.getTimezoneOffset(utcStandardTimestamp),
                18000)

            # Test something east of UTC
            os.environ['TZ'] = 'Europe/Berlin'
            time.tzset()
            self.assertEqual(
                self.flo.getTimezoneOffset(utcDaylightTimestamp),
                -7200)
            self.assertEqual(
                self.flo.getTimezoneOffset(utcStandardTimestamp),
                -3600)

            # Test a timezone that doesn't have DST
            os.environ['TZ'] = 'Africa/Johannesburg'
            time.tzset()
            self.assertEqual(
                self.flo.getTimezoneOffset(utcDaylightTimestamp),
                -7200)
            self.assertEqual(
                self.flo.getTimezoneOffset(utcStandardTimestamp),
                -7200)
        finally:
            if originalTimezone is None:
                del os.environ['TZ']
            else:
                os.environ['TZ'] = originalTimezone
            time.tzset()
    if getattr(time, 'tzset', None) is None:
        test_getTimezoneOffset.skip = (
            "Platform cannot change timezone, cannot verify correct offsets "
            "in well-known timezones.")


    def test_timeFormatting(self):
        """
        Test the method of L{FileLogObserver} which turns a timestamp into a
        human-readable string.
        """
        # There is no function in the time module which converts a UTC time
        # tuple to a timestamp.
        when = time.mktime((2001, 2, 3, 4, 5, 6, 7, 8, 0)) - time.timezone

        # Pretend to be in US/Eastern for a moment
        self.flo.getTimezoneOffset = lambda when: 18000
        self.assertEquals(self.flo.formatTime(when), '2001-02-02 23:05:06-0500')

        # Okay now we're in Eastern Europe somewhere
        self.flo.getTimezoneOffset = lambda when: -3600
        self.assertEquals(self.flo.formatTime(when), '2001-02-03 05:05:06+0100')

        # And off in the Pacific or someplace like that
        self.flo.getTimezoneOffset = lambda when: -39600
        self.assertEquals(self.flo.formatTime(when), '2001-02-03 15:05:06+1100')

        # One of those weird places with a half-hour offset timezone
        self.flo.getTimezoneOffset = lambda when: 5400
        self.assertEquals(self.flo.formatTime(when), '2001-02-03 02:35:06-0130')

        # Half-hour offset in the other direction
        self.flo.getTimezoneOffset = lambda when: -5400
        self.assertEquals(self.flo.formatTime(when), '2001-02-03 05:35:06+0130')

        # If a strftime-format string is present on the logger, it should
        # use that instead.  Note we don't assert anything about day, hour
        # or minute because we cannot easily control what time.strftime()
        # thinks the local timezone is.
        self.flo.timeFormat = '%Y %m'
        self.assertEquals(self.flo.formatTime(when), '2001 02')


    def testLoggingAnObjectWithBroken__str__(self):
        #HELLO, MCFLY
        self.lp.msg(EvilStr())
        self.assertEquals(len(self.out), 1)
        # Logging system shouldn't need to crap itself for this trivial case
        self.assertNotIn('UNFORMATTABLE', self.out[0])


    def testFormattingAnObjectWithBroken__str__(self):
        self.lp.msg(format='%(blat)s', blat=EvilStr())
        self.assertEquals(len(self.out), 1)
        self.assertIn('Invalid format string or unformattable object', self.out[0])


    def testBrokenSystem__str__(self):
        self.lp.msg('huh', system=EvilStr())
        self.assertEquals(len(self.out), 1)
        self.assertIn('Invalid format string or unformattable object', self.out[0])


    def testFormattingAnObjectWithBroken__repr__Indirect(self):
        self.lp.msg(format='%(blat)s', blat=[EvilRepr()])
        self.assertEquals(len(self.out), 1)
        self.assertIn('UNFORMATTABLE OBJECT', self.out[0])


    def testSystemWithBroker__repr__Indirect(self):
        self.lp.msg('huh', system=[EvilRepr()])
        self.assertEquals(len(self.out), 1)
        self.assertIn('UNFORMATTABLE OBJECT', self.out[0])


    def testSimpleBrokenFormat(self):
        self.lp.msg(format='hooj %s %s', blat=1)
        self.assertEquals(len(self.out), 1)
        self.assertIn('Invalid format string or unformattable object', self.out[0])


    def testRidiculousFormat(self):
        self.lp.msg(format=42, blat=1)
        self.assertEquals(len(self.out), 1)
        self.assertIn('Invalid format string or unformattable object', self.out[0])


    def testEvilFormat__repr__And__str__(self):
        self.lp.msg(format=EvilReprStr(), blat=1)
        self.assertEquals(len(self.out), 1)
        self.assertIn('PATHOLOGICAL', self.out[0])

