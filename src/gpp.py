#!/usr/bin/python
# vim: et sw=4 ts=4

import  os
import  sys
import  optparse

canonical_me = 'gpp'
me = canonical_me

class Main( object ):

    def __init__( self, argv ):
        return

    def main( self, Obj, argv = [ '???' ], usage = '%prog [-o file] [file..]',
             description = """FIXME""", prog = None ):
        if prog is not None:
            self.me = prog
        else:
            self.me = os.path.basename( argv[0] )
        p = optparse.OptionParser(
            description = description,
            usage = usage,
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
                    o.do_file( arg )
                elif os.path.isdir( arg ):
                    o.do_dir( arg )
                else:
                    o.error( 'no such file "%s".' % arg )
        o.finish()
        return 0

if __name__ == '__main__':
    # Get base name of application, without any extention or '-pp' trailer
    bindir = os.path.dirname( sys.argv[0] )
    plugdir = os.path.join( bindir, 'plugins' )
    sys.path.insert( 0, plugdir )
    me = os.path.basename( sys.argv[0] ).split( '.' )[0].replace( '-pp', '' )
    if me == canonical_me:
        sys.argv.pop(0)
        me = sys.argv[0]
    dll_name = '%s-plugin' % me
    try:
        dll = __import__(dll_name)
    except Exception, e:
        print >>sys.stderr, 'Cannot import dll "%s".' % dll_name
        raise e
    m = Main( sys.argv )
    exit( m.main(
        dll.PrettyPrint,
        prog = dll.PrettyPrint.NAME,
        description = dll.PrettyPrint.DESCRIPTION
    ) )
