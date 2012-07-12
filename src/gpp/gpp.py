#!/usr/bin/python
# vim: et sw=4 ts=4

import  os
import  sys
import  optparse

class GenericPrettyPrinter( object ):

    def __init__( self ):
        return

    def doit( self, Obj ):
        o = Obj()
        self.me = o.NAME
        try:
            usage = o.USAGE
        except Exception, e:
            usage = '%prog [-o file] [file..]'
        p = optparse.OptionParser(
            description = o.DESCRIPTION,
            usage = usage,
            prog = o.NAME
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
        if len(sys.argv) == 1:
            o.process()
        else:
            for arg in sys.argv[1:]:
                if arg == '-':
                    o.process()
                else:
                    o.do_name( arg )
        o.finish()
        return 0

    def prettyprint( self ):
        # Plugins are in "plugins/" directory under where we live.
        bindir = os.path.dirname( sys.argv[0] )
        plugdir = os.path.join( bindir, 'plugins' )
        sys.path.insert( 0, plugdir )
        # Intuit the kind of prettyprinter we want to be
        if sys.argv[0].endswith( '-pp' ):
            sys.argv[0] = os.path.basename( sys.argv[0] )[:-3]
        elif len(sys.argv) >= 2:
            sys.argv.pop(0)
            kind = sys.argv[0]
        else:
            print >>sys.stderr, 'usage: %s kind [file..]' % (
                os.path.basename( sys.argv[0] )
            )
            raise ValueError
        # Here we go...
        dll_name = '%s-plugin' % kind
        try:
            dll = __import__(dll_name)
        except Exception, e:
            print >>sys.stderr, 'Cannot import dll "%s".' % dll_name
            raise e
        retval = self.doit( Obj = dll.PrettyPrint )
        return retval

if __name__ == '__main__':
    gpp = GenericPrettyPrinter()
    gpp.prettyprint()
