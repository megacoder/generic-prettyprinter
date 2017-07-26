#!/usr/bin/python

import  sys
import  superclass

class   PrettyPrint( superclass.MetaPrettyPrinter ):

    NAME = 'swapon-pp'
    DESCRIPTION="""Show swap areas in canonical style."""

    def __init__( self ):
        super( PrettyPrint, self ).__init__()
        return

    def pre_begin_file( self, name = None ):
        self.titles = []
        self.areas  = dict()
        self.widths = dict()
        return

    def next_line( self, line ):
        tokens = line.split()
        L = len( tokens )
        if L > 0:
            if not self.titles:
                self.titles = tokens
                self.widths = map(
                    len,
                    self.titles
                )
            elif L == len(self.titles):
                mountpoint = tokens[0]
                self.areas[ mountpoint ] = tokens
                self.widths = map(
                    lambda i : max(
                        self.widths[i],
                        len( tokens[i] )
                    ),
                    range( L )
                )
        return

    def report( self, final = False ):
        if final:
            pass
        elif len( self.areas ) > 0:
            N = len( self.widths )
            fmts = map(
                '{{0:<{0}}}'.format( self.widths[ i ] ),
                range( N )
            )
            titles = map(
                fmts[i].format( self.titles[i] ),
                range( N )
            )
            self.println()
            self.println( ' '.join( titles ) )
            for mountpoint in sorted(
                self.areas,
                # Sort by name within priority
                key = lambda f : '{0:d} {1}'.format( f[4], f[0] )
            ):
                tokens = self.areas[ mountpoint ]
                columns = map(
                    fmts[i].format( tokens[i] ),
                    range( len( tokens ) )
                )
                self.println( ' '.join( columns ) )
            pass
        return
