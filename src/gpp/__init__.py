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
        argc = len(sys.argv)
        if argc <= 1:
            o.do_open_file()
        else:
            o.advise( argc = argc )
            for arg in sys.argv[1:]:
                if arg == '-':
                    o.do_open_file()
                else:
                    o.do_name( arg )
        o.finish()
        return 0

    def prettyprint( self, plugdir ):
        # Plugins are in "plugins/" directory under where we live.
        sys.path.insert( 0, plugdir )
        # Intuit the kind of prettyprinter we want to be
        if sys.argv[0].endswith( '-pp' ):
            sys.argv[0] = os.path.basename( sys.argv[0] )[:-3]
        elif len(sys.argv) >= 2:
            sys.argv.pop(0)
            kind = sys.argv[0]
        else:
            print >>sys.stderr, 'usage: %s kind [file..]' % (
                sys.argv[0].split( os.sep )[-1]
            )
            raise ValueError
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
        p.add_option(
            '-t',
            '--type',
            action='store',
            type='string',
            dest='kind',
            help='kind of pretty-printer desired.',
            metavar='file'
        )
        p.set_defaults(
            ofile = None,
            kind = "text"
        )
        opts, args = p.parse_args()
        # Here we go...
        dll_name = '%s-plugin' % opts.kind
        try:
            dll = __import__(dll_name)
        except Exception, e:
            print >>sys.stderr, 'Sorry, no prettyprinter for "%s".' % opts.kind
            return True
        if opts.ofile is not None:
            try:
                sys.stdout = open( opts.ofile, 'wt' )
            except Exception, e:
                print >>sys.stderr, 'Cannot open "%s" for writing.' % opts.ofile
                return True
        sys.argv = [ sys.argv[0] ] + args
        retval = self.doit( Obj = dll.PrettyPrint )
        return retval

if __name__ == '__main__':
    gpp = GenericPrettyPrinter()
    retval = gpp.prettyprint(
        os.path.join( os.path.dirname( gpp.__file__ ), 'plugins' )
    )
    if retval:
        exit(1)
    exit(0)
