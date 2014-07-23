#/usr/bin/python
# vim: et sw=4 ts=4

########################################################################
# Basic pretty-printer module just copies lines to stdout.
########################################################################

import  os
import  sys
import  superclass

class PrettyPrint( superclass.MetaPrettyPrinter ):
    NAME        = 'plugins'
    DESCRIPTION = 'Display list of known plugins.'
    GLOB        = None

    def __init__( self ):
        super( PrettyPrint, self ).__init__()
        self.names = []
        return

    def _add_name( self, name ):
        if not name.endswith( '-plugin.py' ):
            name += '-plugin.py'
        self.names.append( name )
        return

    def do_open_file( self, name = None ):
        if name:
            self._add_name( name )
        return

    def do_name( self, name ):
        if name:
            self._add_name( name )
        return

    def finish( self ):
        if self.names == []:
            for name in os.listdir( sys.path[0] ):
                if name.endswith( '-plugin.py' ):
                    self._add_name( name )
        for name in sorted( self.names ):
            modname = name[:-3]
            try:
                dll = __import__( modname )
            except Exception, e:
                print >>sys.stderr, 'help: cannot import "%s".' % (
                    modname
                )
                print >>sys.stderr, e
                raise e
            try:
                o = dll.PrettyPrint()
                o.help()
            except Exception, e:
                pass
        return
