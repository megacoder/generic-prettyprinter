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

    def do_open_file( self, f = None ):
        return

    def finish( self ):
        for name in sorted(
            os.listdir( sys.path[0] )
        ):
            if name.endswith( '-plugin.py' ):
                self.println( name )
                try:
                    dll = __import__( name[:-3] )
                    dll.help()
                except Exception, e:
                    print >>sys.stderr, 'help: cannot import "%s".' % (
                        name.split( '.' )[0]
                    )
                    print >>sys.stderr, e
                    raise e
        return
