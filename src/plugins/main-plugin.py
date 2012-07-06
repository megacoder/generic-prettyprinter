#/usr/bin/pathon
# vim: et sw=4 ts=4

########################################################################
# Basic pretty-printer module just copies lines to stdout.
########################################################################

import  sys
from    superclass import MetaPrettyPrinter

class PrettyPrint( MetaPrettyPrinter ):
    NAME = 'main'
    DESCRIPTION = 'I am an 80/80 list.'
    def __init__( self ):
        super( PrettyPrint, self ).__init__()
        return
    def process( self, f = sys.stdin ):
        for line in f:
            print line,
        return
