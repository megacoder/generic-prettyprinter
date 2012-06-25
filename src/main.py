#!/usr/bin/python
# vim: et sw=4 ts=4

import  os
import  sys
import  optparse

class Main( object ):

    def __init__( self, argv ):
        return

    def main( self, Obj, argv = [ '???' ] ):
        self.me = os.path.basename( argv[0] )
        p = optparse.OptionParser(
            description = """FIXME""",
            usage = '%prog [-o ofile] [file..]',
            prog = self.me
        )
        p.add_option(
            '-o',
            '--out',
            action='store',
            type='string',
            dest='ofile',
            help='Output written to file; defaults to stdout.',
            metavar='file'
        )
        p.set_defaults(
            ofile = None
        )
        opts, args = p.parse_args()
        o = Obj()
        if len(sys.argv) == 1:
            o.process()
        else:
            for arg in sys.argv[1:]:
                if arg == '-':
                    o.process()
                elif os.path.isfile( arg ):
                    try:
                        f = open( arg, 'rt' )
                    except Exception, e:
                        print >>sys.stderr, 'Cannot open "%s" to read.' % arg
                        raise e
                    o.process( f )
                    f.close()
                else:
                    for root, dirs, files in os.walk( arg ):
                        for file in files:
                            if not file.startswith( '.' ):
                                fn = os.path.join( root, file )
                                if o.notify( fn ):
                                    try:
                                        f = open( fn )
                                    except Exception, e:
                                        print >>sys.stderr, 'Cannot read "%s.".' % (
                                            fn
                                        )
                                        raise e
                                    o.process( f )
                                    f.close()
                        if '.git' in dirs:
                            dirs.remove( '.git' )
        o.finish()
        return 0

if __name__ == '__main__':
    class PrettyPrint( object ):
        def __init__( self ):
            return
        def process( self, f = sys.stdin ):
            for line in f:
                print line,
            return
        def finish( self ):
            return
        def notify( self, fn ):
            print fn
            return True
    m = Main( sys.argv )
    exit( m.main( PrettyPrint ) )
