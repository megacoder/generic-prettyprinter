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
        self.prolog   = []
        self.settings = []
        self.max_name = 0
        return

    def process( self, f = sys.stdin ):
        for line in f:
            line = line.rstrip()
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

    def finish( self ):
        self.settings.sort( key = lambda (n,v): n )
        for line in self.prolog:
            print line
        fmt = '%%%ds=%%s' % self.max_name
        for name,value in self.settings:
            print fmt % (name, value)
        return
