#!/usr/bin/python

import  pprint
import  sys
from    superclass  import  MetaPrettyPrinter

class   PrettyPrint( MetaPrettyPrinter ):

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
            print >>sys.stderr, self.script
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
        self.filename = fn
        try:
            f = open( fn, 'rt' )
        except Exception, e:
            self.error( 'Cannot open file for reading.' )
            self.filename = None
            raise e
        self.process( f )
        f.close()
        return

    def process( self, f = None ):
        if f is None:
            self.filename = '{stdin}'
            f = sys.stdin
        self.script = ''
        for line in f:
            self.script += line
        self.compile()
        return

    def finish( self ):
        if self.keys is None:
            self.error( 'No input detected.' )
        else:
            pp = pprint.PrettyPrinter()
            for key in self.keys:
                print '%13s = ' % key,
                s = pp.pformat( self.locals[key] )
                lines = s.split( '\n' )
                leadin = ''
                for line in lines:
                    print '%s%s' % (leadin, line)
                    leadin = ' '*(16+2)
        return
