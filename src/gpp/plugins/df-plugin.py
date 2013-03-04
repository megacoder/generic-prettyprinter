#!/usr/bin/python

import	os
import	sys
import  superclass

class   PrettyPrint( superclass.MetaPrettyPrinter ):

    NAME = 'df-pp'
    DESCRIPTION = """Display df(1) output in canonical style."""

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
        self.first = True
        self.headers = None
        return

    def begin_file( self, name ):
        super( PrettyPrint, self ).begin_file( name )
        self._prepare()
        return

    def next_line( self, line ):
        parts = line.split( '#', 1 )[0].strip().split()
        n = len( parts )
        if self.first:
            if line.startswith( 'Filesystem' ):
                self.headers = parts
            self.first = false
        else:
            for i in xrange( 0, n ):
                w = len(parts[i])
                try:
                    self.widths[i] = max( self.widths[i], w )
                except:
                    self.widths[i] = w
            self.entries.append( parts )
        return

    def _print_tuples( self, tuples ):
        sep = ''
        for i in xrange( 0, len(tuples) ):
            fmt = '%%s%%-%ds' % self.widths[i]
            print fmt % ( sep, tuples[i] )
            sep = ' '
        return

    def report( self, final = False ):
        if self.headers:
            self._print_tuples( self.headers )
        for tuples in sorted( self.entries ):
            self._print_tuples( tuples )
        self._prepare()
        return
