#!/usr/bin/python

import  os
import  sys
import  math
import  superclass

class   PrettyPrint( superclass.MetaPrettyPrinter ):

    NAME = 'nocomment-pp'
    DESCRIPTION="""Drop splat comments from plain text."""

    def __init__( self ):
        super( PrettyPrint, self ).__init__()
        return

    def next_line( self, line ):
        tokens = map(
            str.rstrip,
            line.split( '#', 1 )
        )
        if len(tokens) and len(tokens[0]):
            self.println( tokens[0] )
        return
