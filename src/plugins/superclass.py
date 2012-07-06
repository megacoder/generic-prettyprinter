#!/usr/bin/python
# vim: et sw=4 ts=4

import  os
import  sys

class   MetaPrettyPrinter( object ):
    def __init__( self ):
        self.reset()
        return
    def reset( self ):
        return
    def do_name( self, name ):
        if os.path.isfile( name ):
            self.do_file( name )
        elif os.path.isdir( name ):
            self.do_dir( name )
        else:
            self.error( 'unknown file type, ignoring "%s".' % name )
            raise ValueError
        return
    def do_file( self, fn ):
        try:
            f = open( fn, 'rt' )
        except Exception, e:
            self.error( 'cannot open "%s" for reading.' % fn, e )
            raise e
        self.process( f )
        f.close()
        return
    def do_dir( self, dn ):
        try:
            files = os.listdir( dn )
        except Exception, e:
            self.error( 'cannot list directory "%s".' % dn, e )
            raise e
        files.sort()
        for fn in files:
            if not self.ignore( fn ):
                self.do_name( os.path.join( dn, fn ) )
        return
    def process( self, f = sys.stdin ):
        for line in f:
            print line,
        return
    def ignore( self, name ):
        return False
    def finish( self ):
        return
    def error( self, msg, e = None ):
        print >>sys.stderr, msg
        if e is not None:
            print >>sys.stderr, e
            raise e
        return
