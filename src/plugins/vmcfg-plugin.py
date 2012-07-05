#!/usr/bin/python

import  pprint
import  sys

class   PrettyPrint( object ):

    def __init__( self ):
        self.reset()
        return

    def reset( self ):
        self.keys   = None
        self.code   = None
        self.fn     = None
        self.locals = None
        self.pp     = pprint.PrettyPrint()
        return

    def compile( self ):
        try:
            self.code = compile( self.script, self.fn, 'exec' )
        except:
            raise SyntaxError
        self.locals = dict()
        globals = dict()
        try:
            eval( self.code, globals, self.locals )
        except:
            raise SyntaxError
        self.keys =  self.locals.keys()
        self.keys.sort()
        return

    def finish( self ):
        for key in self.keys:
            print '%13s = ' % key,
            s = self.pp.pformat( self.locals[key] )
            lines = s.split( '\n' )
            leadin = ''
            for line in lines:
                print '%s%s' % (leadin, line)
                leadin = ' '*(16+2)
        return
