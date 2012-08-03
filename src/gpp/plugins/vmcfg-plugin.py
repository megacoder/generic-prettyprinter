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
        super( PrettyPrint, self ).reset()
        self.keys   = None
        self.code   = None
        self.locals = None
        return

    def compile( self ):
        try:
            self.code = compile( self.script, self.filename, 'exec' )
        except:
            self.error( 'File "%s" appears to be corrupt.' % self.filename )
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
            self.filename = '{stdin}'
            self.script = sys.stdin.readlines()
        else:
            self.script = f.readlines()
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
