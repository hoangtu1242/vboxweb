#!/usr/bin/env python
# ***** BEGIN LICENSE BLOCK *****
#
# The MIT License
#
# Copyright (c) 2009 Josh Wright
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# ***** END LICENSE BLOCK *****

import os, sys

USAGE = """

VBoxWeb - A web-based frontend for Sun's VirtualBox

Usage:
    -h, --help
        Print this usage list and exit
    -p, --port [port number]
        Set the port number VBoxWeb should listen on
"""

try:
    import cherrypy
    major_version = int(cherrypy.__version__[0])
    if major_version < 3:
        raise ImportError
except ImportError:
    print """
            VBoxWeb requires CherryPy (version 3.0 or higher).

            You can download the latest version of CherryPy
                    from http://www.cherrypy.org/
          """
    sys.exit()

sys.path.append('/usr/lib/virtualbox')

import xpcom.vboxxpcom
import xpcom
import xpcom.components

from content import Root

class LocalManager:
    def getSessionObject(self, vbox):
        return xpcom.components.classes["@virtualbox.org/Session;1"].createInstance()

vbox = xpcom.components.classes["@virtualbox.org/VirtualBox;1"].createInstance()

def main(argv):

    port = 8080

    if len(argv) > 1:
        i = iter(argv)
        executable = i.next()
        for arg in i:
            if arg in ('-p', '--port'):
                port = i.next()
            if arg in ('-h', '--help'):
                print USAGE
                sys.exit(0)
            else:
                print "\nUnknown command: %s" % arg
                print USAGE
                sys.exit(1)

    cherrypy.config.update({
        'server.socket_port': port,
        'tools.encode.on': True, 'tools.encode.encoding': 'utf-8',
        'tools.decode.on': True,
        'tools.trailing_slash.on': True,
        'tools.staticdir.root': os.path.abspath(os.path.dirname(__file__)),
    })

    root = Root(LocalManager(), vbox)

    cherrypy.quickstart(root, '/', {
        '/media': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'media'
        }
    })

if __name__ == '__main__':
    main(sys.argv)
