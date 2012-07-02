#/usr/bin/pathon
# vim: et sw=4 ts=4

########################################################################
# Basic pretty-printer module just copies lines to stdout.
########################################################################

import  sys

class PrettyPrint( object ):
    def __init__( self ):
        return
    def process( self, f = sys.stdin ):
        for line in f:
            print line,
        return
    def finish( self ):
        return
    def notify( self, fn ):
        print fn
        return True
