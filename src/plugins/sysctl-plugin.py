#!/usr/bin/python

import  os
import  sys
import  math

from    superclass  import  MetaPrettyPrinter

class   PrettyPrint( MetaPrettyPrinter ):

    NAME = 'sysctl-pp'
    DESCRIPTION="""Output /etc/sysctl.conf in canonical form."""

    def __init__( self, out = sys.stdout ):
        super( PrettyPrint, self ).__init__()
        return

    def reset( self ):
        self.out    = sys.stdout
        self.lines  = []
        self.fmt    = "%31s\t%s"
        self.maxlen = 0
        return

    def ignore( self, name ):
        return not name.endswith( '.conf' )

    def process( self, fyle = sys.stdin ):
        for line in fyle:
            n = line.find( '#' )
            if n > -1: line = line[:n]
            try:
                key, value = line.split( '=', 1 )
            except Exception, e:
                continue
            k = key.strip()
            self.maxlen = max( self.maxlen, len(k) )
            self.lines.append( (k, value.strip()) )
        return

    def finish( self ):
        self.fmt = "%%%ds = %%s" % self.maxlen
        self.lines.sort( key = lambda (key,value): key.lower() )
        for key,value in self.lines:
            print self.fmt % (key, value)
        return
