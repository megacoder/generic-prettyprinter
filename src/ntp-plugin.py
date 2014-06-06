#!/usr/bin/python

import  os
import  sys
import  math
import  superclass

class   PrettyPrint( superclass.MetaPrettyPrinter ):

    NAME = 'ntp-pp'
    DESCRIPTION="""Output /etc/ntp.conf in canonical form."""

    def __init__( self ):
        super( PrettyPrint, self ).__init__()
        return

    def reset( self ):
        super( PrettyPrint, self ).reset()
        self._prepare()
        return

    def _prepare( self ):
        self.tokens  = []
        return

    def ignore( self, name ):
        return not name.endswith( '.conf' )

    def begin_file( self, name ):
        super( PrettyPrint, self ).begin_file( name )
        self._prepare()
        return

    def next_line( self, line ):
        tokens = line.split( '#', 1 )[0].split()
        if len(tokens) > 0:
            self.tokens.append( tokens )
        return

    def report( self, final = False ):
        # Space groups of similar lines similarly
        last_kind = None
        lines = []
        for tokens in sorted( self.tokens, key = lambda t : t[0].lower() ):
            kind = tokens[0].lower()
            if kind != last_kind:
                if len(lines) > 0:
                    self._print_group( lines )
                    lines = []
                lines.append( tokens )
                last_kind = kind
        if len(lines) > 0:
            self._print_group( lines )
        self._prepare()
        return

    def _print_group( self, lines ):
        # Calculate column widths
        widths = {}
        for tokens in lines:
            for i in xrange( 0, len(tokens) ):
                try:
                    widths[i] = max( widths[i], len(tokens[i]) )
                except:
                    widths[i] = max( 12, len(tokens[i]) )
        # Dump group using fixed-width columns
        for tokens in lines:
            s = ""
            sep = ""
            for i in xrange( 0, len(tokens) ):
                fmt = '%%s%%-%ds' % widths[i]
                s += fmt % (sep, tokens[i] )
                sep = " "
            self.println( s )
        return
