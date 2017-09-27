#!/usr/bin/python

import  os
import  sys
import  math
import  superclass

class   PrettyPrint( superclass.MetaPrettyPrinter ):

    NAME = 'text-pp'
    DESCRIPTION="""Plain text."""

    def __init__( self ):
        super( PrettyPrint, self ).__init__()
        return
