#!/usr/bin/python
# vim: et sw=4 ts=4

import  os
import  sys
import  optparse

class GenericPrettyPrinter( object ):

    NAME = 'N/A'
    USAGE = '%prog [-o file] [-t type] [file..]'
    DESCRIPTION = """Generic pretty-printer with loadable modules."""

    def __init__( self ):
        return

    def own_glob( self, pattern = None ):
        if not pattern:
            try:
                pattern = self.GLOB
            except Exception, e:
                pattern = '*'
        return glob.glob( pattern )

    def doit( self, Obj, names = [] ):
        o = Obj()
        argc = len(sys.argv)
        n = len(names)
        # Allow plugin to figure out where its files are
        if n < 1:
            names = o.own_glob()
        if names:
            n = len( names )
            if n < 1:
                # Give plugin a chance to handle its no-file method
                o.do_open_file()
            else:
                # Iterate through the names
                o.advise( argc = n )
                for name in names:
                    if name == '-':
                        o.do_open_file()
                    else:
                        o.do_name( name )
        o.finish()
        return False

    def main( self ):
        sys.path.insert( 0, os.path.dirname( __file__ ) )
        # Intuit the kind of prettyprinter we want to be
        kind = 'text'
        if sys.argv[0].endswith( '-pp' ):
            kind = os.path.basename( sys.argv[0] )[:-3]
        p = optparse.OptionParser(
            description = """Generic pretty-printer""",
            usage       = '%prog [-o ofile] [-t type] [file..]',
            prog        = 'gpp'
        )
        p.add_option(
            '-o',
            '--out',
            action  = 'store',
            type    = 'string',
            dest    = 'ofile',
            default =  None,
            help    = 'Output written to file; defaults to stdout.',
            metavar = 'file'
        )
        p.add_option(
            '-t',
            '--type',
            action  ='store',
            type    ='string',
            default = 'text',
            dest    ='kind',
            help    ='kind of pretty-printer desired; defaults to text.',
            metavar ='file'
        )
        opts, args = p.parse_args()
        # Here we go...
        if opts.kind == 'help':
            retval = False
        else:
            dll_name = '%s-plugin' % opts.kind
            # DEBUG print >>sys.stderr, 'Loading module %s' % dll_name
            try:
                dll = __import__(dll_name)
            except Exception, e:
                print >>sys.stderr, 'No prettyprinter for "%s".' % opts.kind
                print >>sys.stderr, e
                return True
            if opts.ofile is not None:
                try:
                    sys.stdout = open( opts.ofile, 'wt' )
                except Exception, e:
                    print >>sys.stderr, 'Cannot open "%s" for writing.' % opts.ofile
                    return True
            retval = self.doit( Obj = dll.PrettyPrint, names = args )
        return retval

    def do_one_module( self, kind = 'help', args = [] ):
        dll_name = '%s-plugin' % kind
        # DEBUG print >>sys.stderr, 'Loading module %s' % dll_name
        try:
            dll = __import__(dll_name)
        except Exception, e:
            print >>sys.stderr, 'No prettyprinter for "%s".' % opts.kind
            print >>sys.stderr, e
            return True
        retval = self.doit( Obj = dll.PrettyPrint, names = args )
        return retval

if __name__ == '__main__':
    import  __main__
    gpp = GenericPrettyPrinter()
    retval = gpp.main()
    if retval:
        exit(1)
    exit(0)
