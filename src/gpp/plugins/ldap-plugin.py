#!/usr/bin/python

import  sys
import  superclass

class   PrettyPrint( superclass.MetaPrettyPrinter ):

    NAME = 'ldap'
    DESCRIPTION="""Show ldap.conf files in canonical style."""

    def __init__( self ):
        super( PrettyPrint, self ).__init__()
        return

    def reset( self ):
        super( PrettyPrint, self ).reset()
        self.settings = []
        return

    def next_line( self, line ):
        # Remove comment and strip leading/trailing blanks
        line = line.split('#',1)[0].strip()
        tokens = line.split()
        if len(tokens) > 0:
            name = tokens[0].upper()
            self.settings.append( (name, ' '.join(tokens[1:])) )
        return

    def _flush( self ):
        self.settings.sort( key = lambda (n,v): n )
        max_name = 0
        for (n,v) in self.settings:
            max_name = max( max_name, len(n) )
        fmt = ' %%%ds  %%s' % max_name
        for (n,v) in self.settings:
            print fmt % (n, v)
        self.reset()
        return

    def end_file( self, fn ):
        self._flush()
        super( PrettyPrint, self ).end_file( fn )
        return

    def finish( self ):
        self._flush()
        return
