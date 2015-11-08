#!/usr/bin/python

import	os
import	sys
import  superclass
import  align

class   PrettyPrint( superclass.MetaPrettyPrinter ):

    NAME = 'nsswitch-pp'
    DESCRIPTION = """Display nsswitch.conf in canonical style."""

    def __init__( self ):
        super( PrettyPrint, self ).__init__()
        self.pre_open_file()
        return

    def pre_open_file( self ):
        self.lines   = []
        return

    def next_line( self, line ):
        # Drop comments
        parts = line.split( '#', 1 )[0].strip().split()
        if len( parts ) > 0:
            # Save non-blank lines
            self.lines.append( parts )
        return

    def report( self, final = False ):
        if not final:
            self.lines.sort()
            a = align.align()
            for parts in self.lines:
                a.add( parts )
            for parts in a.get_items():
                self.println( ' '.join( parts ) )
        return
