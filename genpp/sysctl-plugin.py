#!/usr/bin/python

import  os
import  sys
import  math
import  superclass

class   PrettyPrint( superclass.MetaPrettyPrinter ):

    NAME = 'sysctl-pp'
    DESCRIPTION="""Output /etc/sysctl.conf in canonical form."""

    def __init__( self ):
        super( PrettyPrint, self ).__init__()
        return

    def reset( self ):
        super( PrettyPrint, self ).reset()
        self.out    = sys.stdout
        self.fmt    = "%31s\t%s"
        self._prepare()
        return

    def _prepare( self ):
        self.maxlen = 0
        self.lines  = []
        return

    def ignore( self, name ):
        return not name.endswith( '.conf' )

    def begin_file( self, name ):
        super( PrettyPrint, self ).begin_file( name )
        self._prepare()
        return

    def next_line( self, line ):
        n = line.find( '#' )
        if n > -1: line = line[:n]
        try:
            key, value = line.split( '=', 1 )
        except Exception, e:
            return
        k = key.strip()
        self.maxlen = max( self.maxlen, len(k) )
        self.lines.append( (k, value.strip()) )
        return

    def report( self, final = False ):
        self.fmt = "%%%ds = %%s" % self.maxlen
        self.lines.sort( key = lambda (key,value): key.lower() )
        for key,value in self.lines:
            print self.fmt % (key, value)
        self._prepare()
        return
