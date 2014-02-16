#!/usr/bin/python

import  pprint
import  sys
from    superclass  import  MetaPrettyPrinter

class   PrettyPrint( MetaPrettyPrinter ):

    NAME = 'python'
    DESCRIPTION = """Display python files in canonical style."""

    def __init__( self ):
        super( PrettyPrint, self ).__init__()
        self._prepare()
        return

    def _prepare( self ):
        self.keys   = None
        self.code   = None
        self.locals = None
        self.script = ''
        return

    def compile( self ):
        if len(self.script) == 0:
            return
        try:
            self.code = compile( self.script, self.filename, 'exec' )
        except:
            self.error( 'File "%s" appears to be corrupt.' % self.filename )
            self.error( '%s' % self.script )
            return
        self.locals = dict()
        globals = dict()
        try:
            eval( self.code, globals, self.locals )
        except Exception, e:
            self.println( 'Could not evaluate code' )
            self.println( ' %s' % e )
            return
        self.keys =  self.locals.keys()
        return

    def begin_file( self, name ):
        super( PrettyPrint, self ).begin_file( name )
        self._prepare()
        return

    def next_line( self, line ):
        if line.startswith( '/' ):
            pass
        elif line.startswith( './' ):
            self.compile()
            self.report()
            self._prepare()
            if self.lineno > 1:
                self.println()
            self.println( '# --> %s' % line[1:] )
            self.println()
        elif len(line) > 0:
            self.script += '%s\n' % line
        return

    def end_file( self, name ):
        self.compile()
        self.report()
        self._prepare()
        super( PrettyPrint, self ).end_file( name )
        return

    def report( self, final = False ):
        if len(self.script) == 0:
            pass
        elif not self.keys:
            self.println( 'no content detected' )
        else:
            pp = pprint.PrettyPrinter()
            for key in sorted( self.keys ):
                print '%13s = ' % key,
                s = pp.pformat( self.locals[key] )
                lines = s.split( '\n' )
                leadin = ''
                for line in lines:
                    print '%s%s' % (leadin, line)
                    leadin = ' '*(16+2)
        return
