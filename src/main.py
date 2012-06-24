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
            o._process()
        else:
            for arg in sys.argv[1:]:
                if arg == '-':
                    o.process()
                elif os.path.isfile( arg ):
                    o.process( arg )
                else:
                    for root, dirs, files in os.walk( arg ):
                        for file in files:
                            if not file.startswith( '.' ):
                                o.process( os.path.join( root, file ) )
                        if '.git' in dirs:
                            dirs.remove( '.git' )
        o.finish()
        return

if __name__ == '__main__':
    class PrettyPrint( object ):
        def __init__( self ):
            return
        def process( self, fn ):
            print fn
            return
        def finish( self ):
            return
    m = Main( sys.argv )
    m.main( PrettyPrint )
