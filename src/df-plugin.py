#!/usr/bin/python

import	os
import	sys
import  superclass
import  align

class   PrettyPrint( superclass.MetaPrettyPrinter ):

    NAME = 'df-pp'
    DESCRIPTION = """Display df(1) output in canonical style."""

    def __init__( self ):
        super( PrettyPrint, self ).__init__()
        self.pre_open_file()
        return

    def pre_open_file( self ):
        self.items   = []
        self.headers = None
        self.pending = None
        return

    def next_line( self, line ):
        parts = map(
            str.strip,
            line.split( '#', 1 )[0].split()
        )
        # If the partition name was very, very long, its
        # line was folded, so unfold it here
        if self.pending:
            parts += self.pending
            self.pending = None
        if self.headers:
            N = len( parts )
            if N:
                if N < 6:
                    self.pending = parts
                else:
                    self.items.append( parts )
        else:
            if line.startswith( 'Filesystem' ):
                # Coalesce 'Mounted' 'on' into 'Mounted on'
                parts[-2] = ' '.join( parts[-2:] )
                # Save all but isolated 'on', which is the final arg
                self.headers = parts[ : -1 ]
        return

    def report( self, final = False ):
        if not final:
            a = align.align()
            if self.headers:
                a.add( self.headers )
            self.items.sort( key = lambda p: p[-1] )
            for parts in self.items:
                a.add( parts )
            for parts in a.get_items():
                self.println( ' '.join( parts ) )
        return
