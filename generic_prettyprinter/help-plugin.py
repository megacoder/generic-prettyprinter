#/usr/bin/python
# vim: et sw=4 ts=4

########################################################################
# Basic pretty-printer module just copies lines to stdout.
########################################################################

import  os
import  sys
import  superclass

class PrettyPrint( superclass.MetaPrettyPrinter ):
    NAME = 'plugins'
    DESCRIPTION = 'Display list of known plugins.'

    def __init__( self ):
        super( PrettyPrint, self ).__init__()
        self.names = []
        return

    def do_open_file( self, f = None ):
        self.names = os.listdir( sys.path[0] )
        return

    def finish( self ):
        self.names.sort()
        for name in self.names:
            if name.endswith( '-plugin.py' ):
                dll = __import__( name[:-3] )
                print '%23s %s' % (
                    dll.PrettyPrint.NAME,
                    dll.PrettyPrint.DESCRIPTION
                )
        return 0
