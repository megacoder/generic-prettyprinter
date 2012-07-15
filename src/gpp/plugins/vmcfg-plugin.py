#!/usr/bin/python

import  pprint
import  sys
import  superclass

class   PrettyPrint( superclass.MetaPrettyPrinter ):

    NAME = 'vmcfg'
    DESCRIPTION = """Display vm.cfg files in canonical style."""

    def __init__( self ):
        super( PrettyPrint, self ).__init__()
        return

    def reset( self ):
        self.keys   = None
        self.code   = None
        self.fn     = None
        self.locals = None
        return

    def compile( self ):
        try:
            self.code = compile( self.script, self.fn, 'exec' )
        except:
            self.error( 'File "%s" appears to be corrupt.' % self.fn )
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

    def do_file( self, fn ):
        self.fn = fn
        self.compile()
        return

    def process( self, f = None ):
        if f is None:
            self.fn = '{stdin}'
            self.script = sys.stdin.readlines()
            self.compile()
        return

    def finish( self ):
        if self.keys is None:
            self.error( 'No input detected.' )
        else:
            for key in self.keys:
                print '%13s = ' % key,
                s = pprint.PrettyPrint.pformat( self.locals[key] )
                lines = s.split( '\n' )
                leadin = ''
                for line in lines:
                    print '%s%s' % (leadin, line)
                    leadin = ' '*(16+2)
        return
