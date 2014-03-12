#!/usr/bin/python
# Print free(1) output in canonical form

import	os
import	sys
import  superclass

class   PrettyPrint( superclass.MetaPrettyPrinter ):

    NAME = 'free-pp'
    DESCRIPTION = """Display free(1) output in canonical style."""
    GLOB = None

    def __init__( self ):
        super( PrettyPrint, self ).__init__()
        self.reset()
        return

    def reset( self ):
        super( PrettyPrint, self ).reset()
        self._prepare()
        return

    def _prepare( self ):
        self.widths = {}
        self.entries = []
        return

    def begin_file( self, name ):
        super( PrettyPrint, self ).begin_file( name )
        self._prepare()
        self.lines = 0
        return

    def next_line( self, line ):
        self.lines += 1
        tokens = line.split( '#', 1 )[0].strip().split()
        if self.lines == 1:
            self.names = tokens
        elif line.startswith( 'Mem:' ):
            self.mem = dict( zip( self.names, tokens[1:] ) )
        elif line.startswith( '-/+ buffers/cache:' ):
            self.cache = dict( zip( self.names[1:], tokens[2:] ) )
        elif line.startswith( 'Swap:' ):
            self.swap = dict( zip( self.names, tokens[1:] ) )
        return

    def print_dict( self, d, title = None ):
        if title:
            self.println( title )
        width = max( map( len, self.names ) )
        fmt = '%%-%ds %%s' % width
        for key in sorted( d.keys() ):
            self.println( fmt % ( key, d[key] ) )
        return

    def report( self, final = False ):
        self.print_dict( self.mem, 'Memory' )
        self.print_dict( self.cache, 'Cache' )
        self.print_dict( self.swap, 'Swap' )
        return

    def end_file( self, name ):
        self._prepare()
        super( PrettyPrint, self ).end_file( name )
        return
