#!/usr/bin/python

import  sys
import  superclass

class   PrettyPrint( superclass.MetaPrettyPrinter ):

    NAME = 'iscsi-pp'
    DESCRIPTION="""Show iSCSI config files in canonical style."""

    def __init__( self ):
        super( PrettyPrint, self ).__init__()
        return

    def reset( self ):
        super( PrettyPrint, self ).reset()
        self._prepare()

    def _prepare( self ):
        self.items = []
        self.max_name = 0
        return

    def next_line( self, line ):
        tokens = line.split( '#', 1 )[0].split( '=', 1 )
        if len(tokens) == 2:
            name = tokens[0].strip()
            settings = tokens[1].strip()
            self.max_name = max( self.max_name, len(name) )
            self.items.append( (name, settings) )
        return

    def report( self, final = False ):
        fmt = '%%%ds = %%s' % self.max_name
        for (name,settings) in sorted( self.items):
            self.println( fmt % (name, settings) )
        self._prepare()
        return
