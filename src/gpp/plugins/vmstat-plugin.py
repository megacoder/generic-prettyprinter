#!/usr/bin/python
# vim: et sw=4 ts=4

import  os
import  sys
import  csv
import  superclass

class   PrettyPrint( superclass.MetaPrettyPrinter ):

    NAME = 'vmstat-pp'
    DESCRIPTION = """Display vmstat(1) output in a canonical style."""

    def __init__( self ):
        super( PrettyPrint, self ).__init__()
        return

    def reset( self ):
        super( PrettyPrint, self ).reset()
        self._prepare()
        return

    def _prepare( self ):
        self.timestamp = None
        self.titles    = None
        self.widths    = {}
        self.entries   = []
        return

    def begin_file( self, name ):
        super( PrettyPrint, self ).begin_file( name )
        self._prepare()
        return

    def end_file( self, name ):
        super( PrettyPrint, self ).end_file( name )
        return

    def next_line( self, line ):
        if line.startswith( 'Linux OSW' ):
            self.report()
        elif line.startswith( 'zzz ***' ):
            self.timestamp = line[7:]
        elif line.startswith( 'procs' ):
            pass
        elif line.startswith( ' r ' ):
            self.titles = line.split()
        else:
            self.entries.append( line.split() )
        return

    def _calc_widths( self ):
        self.widths = {}
        if self.titles:
            for i in xrange( 0, len(self.titles) ):
                self.widths[i] = len( self.titles[i] )
            for entry in self.entries:
                for i in xrange( 0, len(entry) ):
                    try:
                        self.widths[i] = max( self.widths[i], len( entry[i] ) )
                    except:
                        self.widths[i] = len( entry[i] )
        return

    def _show( self, tokens ):
        line = ''
        sep  = ''
        for i in xrange( 0, len(tokens) ):
            fmt = '%%s%%%ds' % self.widths[i]
            line += fmt % (sep, tokens[i])
            sep = '  '
        self.println( line )
        return

    def report( self, final = False ):
        if self.titles:
            if self.timestamp:
                self.println( '' )
                self.println( self.timestamp )
                self.println( '' )
            self._calc_widths()
            self._show( self.titles )
            for entry in self.entries:
                self._show( entry )
        if not final:
            self._prepare()
        return
