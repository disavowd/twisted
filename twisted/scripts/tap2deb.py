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


import sys, os, string, shutil

from twisted.python import usage

class MyOptions(usage.Options):
    optFlags = [["unsigned", "u"]]
    optParameters = [["tapfile", "t", "twistd.tap"],
                  ["maintainer", "m", ""],
                  ["protocol", "p", ""],
                  ["description", "e", ""],
                  ["long_description", "l", ""],
                  ["version", "v", "1.0"],
                  ["debfile", "d", None],
                  ["type", "y", "tap", "type of configuration: 'tap', 'xml, 'source' or 'python'"]]


type_dict = {
'tap': 'file',
'python': 'python',
'source': 'source',
'xml': 'xml',
}

def save_to_file(file, text):
    open(file, 'w').write(text)


def run():

    try:
        config = MyOptions()
        config.parseOptions()
    except usage.error, ue:
        sys.exit("%s: %s" % (sys.argv[0], ue))

    tap_file = config['tapfile']
    base_tap_file = os.path.basename(config['tapfile'])
    protocol = (config['protocol'] or os.path.splitext(base_tap_file)[0])
    deb_file = config['debfile'] or 'twisted-'+protocol
    version = config['version']
    maintainer = config['maintainer']
    description = config['description'] or ('A TCP server for %(protocol)s' %
                                            vars())
    long_description = config['long_description'] or 'Automatically created by tap2deb'
    twistd_option = type_dict[config['type']]
    date = string.strip(os.popen('822-date').read())
    directory = deb_file + '-' + version
    python_version = '%s.%s' % sys.version_info[:2]

    if os.path.exists(os.path.join('.build', directory)):
        os.system('rm -rf %s' % os.path.join('.build', directory))
    os.makedirs(os.path.join('.build', directory, 'debian'))

    shutil.copy(tap_file, os.path.join('.build', directory))

    save_to_file(os.path.join('.build', directory, 'debian', 'README.Debian'), 
    '''This package was auto-generated by tap2deb''')

    save_to_file(os.path.join('.build', directory, 'debian', 'conffiles'), 
    '''\
/etc/init.d/%(deb_file)s
/etc/default/%(deb_file)s
/etc/%(base_tap_file)s
''' % vars())

    save_to_file(os.path.join('.build', directory, 'debian', 'default'), 
    '''\
pidfile=/var/run/%(deb_file)s.pid \
rundir=/var/lib/%(deb_file)s/ \
file=/etc/%(tap_file)s \
logfile=/var/log/%(deb_file)s.log
 ''' % vars())

    save_to_file(os.path.join('.build', directory, 'debian', 'init.d'),
    '''\
#!/bin/sh

PATH=/sbin:/bin:/usr/sbin:/usr/bin

pidfile=/var/run/%(deb_file)s.pid \
rundir=/var/lib/%(deb_file)s/ \
file=/etc/%(tap_file)s \
logfile=/var/log/%(deb_file)s.log

[ -r /etc/default/%(deb_file)s ] && . /etc/default/%(deb_file)s

test -x /usr/bin/twistd%(python_version)s || exit 0
test -r $file || exit 0
test -r /usr/share/%(deb_file)s/package-installed || exit 0


case "$1" in
    start)
        echo -n "Starting %(deb_file)s: twistd"
        start-stop-daemon --start --quiet --exec /usr/bin/twistd%(python_version)s -- \
                          --pidfile=$pidfile \
                          --rundir=$rundir \
                          --%(twistd_option)s=$file \
                          --logfile=$logfile \
                          --quiet
        echo "."	
    ;;

    stop)
        echo -n "Stopping %(deb_file)s: twistd"
        start-stop-daemon --stop --quiet  \
            --pidfile $pidfile
        echo "."	
    ;;

    restart)
        $0 stop
        $0 start
    ;;

    force-reload)
        $0 restart
    ;;

    *)
        echo "Usage: /etc/init.d/%(deb_file)s {start|stop|restart|force-reload}" >&2
        exit 1
    ;;
esac

exit 0
''' % vars())

    os.chmod(os.path.join('.build', directory, 'debian', 'init.d'), 0755)

    save_to_file(os.path.join('.build', directory, 'debian', 'postinst'),
    '''\
#!/bin/sh
update-rc.d %(deb_file)s defaults >/dev/null
invoke-rc.d %(deb_file)s start
''' % vars())

    save_to_file(os.path.join('.build', directory, 'debian', 'prerm'),
    '''\
#!/bin/sh
invoke-rc.d %(deb_file)s stop
''' % vars())

    save_to_file(os.path.join('.build', directory, 'debian', 'postrm'),
    '''\
#!/bin/sh
if [ "$1" = purge ]; then
        update-rc.d %(deb_file)s remove >/dev/null
fi
''' % vars())

    save_to_file(os.path.join('.build', directory, 'debian', 'changelog'),
    '''\
%(deb_file)s (%(version)s) unstable; urgency=low

  * Created by tap2deb

 -- %(maintainer)s  %(date)s

''' % vars())

    save_to_file(os.path.join('.build', directory, 'debian', 'control'),
    '''\
Source: %(deb_file)s
Section: net
Priority: extra
Maintainer: %(maintainer)s
Build-Depends-Indep: debhelper
Standards-Version: 3.5.6

Package: %(deb_file)s
Architecture: all
Depends: python%(python_version)s-twisted
Description: %(description)s
 %(long_description)s
''' % vars())

    save_to_file(os.path.join('.build', directory, 'debian', 'copyright'),
    '''\
This package was auto-debianized by %(maintainer)s on
%(date)s

It was auto-generated by tap2deb

Upstream Author(s): 
Moshe Zadka <moshez@twistedmatrix.com> -- tap2deb author

Copyright:

tap2deb is released under the GNU Lesser General Public License,
and this package contains bits of code from tap2deb, and hence is
a derived work of tap2deb, and is under the GNU Lesser General
Public License
''' % vars())

    save_to_file(os.path.join('.build', directory, 'debian', 'dirs'),
    '''\
etc/init.d
etc/default
var/lib/%(deb_file)s
usr/share/doc/%(deb_file)s
usr/share/%(deb_file)s
''' % vars())

    save_to_file(os.path.join('.build', directory, 'debian', 'rules'),
    '''\
#!/usr/bin/make -f

export DH_COMPAT=1

build: build-stamp
build-stamp:
	dh_testdir
	touch build-stamp

clean:
	dh_testdir
	dh_testroot
	rm -f build-stamp install-stamp
	dh_clean

install: install-stamp
install-stamp: build-stamp
	dh_testdir
	dh_testroot
	dh_clean -k
	dh_installdirs

	# Add here commands to install the package into debian/tmp.
	cp %(base_tap_file)s debian/tmp/etc/
	cp debian/init.d debian/tmp/etc/init.d/%(deb_file)s
	cp debian/default debian/tmp/etc/default/%(deb_file)s
	cp debian/copyright debian/tmp/usr/share/doc/%(deb_file)s/
	cp debian/README.Debian debian/tmp/usr/share/doc/%(deb_file)s/
	touch debian/tmp/usr/share/%(deb_file)s/package-installed
	touch install-stamp

binary-arch: build install

binary-indep: build install
	dh_testdir
	dh_testroot
	dh_strip
	dh_compress
	dh_installchangelogs
	dh_fixperms
	dh_installdeb
	dh_shlibdeps
	dh_gencontrol
	dh_md5sums
	dh_builddeb

source diff:                                                                  
	@echo >&2 'source and diff are obsolete - use dpkg-source -b'; false

binary: binary-indep binary-arch
.PHONY: build clean binary-indep binary-arch binary install
''' % vars())

    os.chmod(os.path.join('.build', directory, 'debian', 'rules'), 0755)

    os.chdir('.build/%(directory)s' % vars())
    os.system('dpkg-buildpackage -rfakeroot'+ ['', ' -uc -us'][config['unsigned']])
