#/usr/bin/python
# vim: et sw=4 ts=4

########################################################################
# Basic pretty-printer module just copies lines to stdout.
########################################################################

import  sys
import  superclass

class PrettyPrint( superclass.MetaPrettyPrinter ):
    NAME = 'main'
    DESCRIPTION = 'I am an 80/80 list.'
    def __init__( self ):
        super( PrettyPrint, self ).__init__()
        return
    def next_line( self, line ):
        print line
        return
