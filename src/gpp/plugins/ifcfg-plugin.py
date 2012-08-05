#!/usr/bin/python

import  sys
import  superclass

class   PrettyPrint( superclass.MetaPrettyPrinter ):

    NAME = 'ifcfg-pp'
    DESCRIPTION="""Show ifcfg network files in canonical style."""

    def __init__( self ):
        super( PrettyPrint, self ).__init__()
        return

    def reset( self ):
        super( PrettyPrint, self ).reset()
        self.prolog   = []
        self.settings = []
        self.max_name = 0
        return

    def next_line( self, line ):
        if line.startswith( '#' ):
            self.prolog.append( line )
        else:
            parts = line.rstrip().split( '=', 1 )
            if len(parts) != 2:
                self.prolog.append( line )
            else:
                name  = parts[0]
                value = parts[1]
                if not value.startswith('"') and not value.startswith("'"):
                    value = '"' + value + '"'
                self.settings.append( (name,value) )
                self.max_name = max( self.max_name, len(name) )
        return

    def _flush( self ):
        if len(self.settings) > 0 and len(self.prolog) > 0:
            self.settings.sort( key = lambda (n,v): n )
            for line in self.prolog:
                print line
            fmt = '%%%ds=%%s' % self.max_name
            for name,value in self.settings:
                print fmt % (name, value)
        self.reset()
        return

    def begin_file( self, fn ):
        print '#'*72
        print '# %s' % fn
        print '#'*72
        return

    def end_file( self, fn ):
        self._flush()
        print
        return

    def finish( self ):
        self._flush()
        return
