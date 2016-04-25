#!/usr/bin/python
# vim: et sw=4 ts=4

import  os
import  sys
import  optparse

class GenericPrettyPrinter( object ):

    NAME = 'N/A'
    USAGE = '%prog [-o file] [-t type] [file..]'
    DESCRIPTION = """Generic pretty-printer with loadable modules."""

    GLOB = '*'

    def __init__( self ):
        return

    def own_glob( self, pattern = None ):
        if not pattern:
            pattern = self.GLOB
        return glob.glob( pattern )

    def _session( self, Handler, names = [] ):
        handler = Handler()
        # Allow plugin to figure out where its files are
        if len( names ) == 0:
            names = handler.own_glob()
        # Here is the session
        handler.start()
        handler.advise( names )
        for name in names:
            handler.process( name )
        handler.finish()
        return False

    def process( self, f = sys.stdin ):
        for line in f:
            self.println( line.rstrip() )
        return

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
            '-D',
            '--debug',
            action  = 'store',
            type    = 'string',
            dest    = 'debug_level',
            default =  0,
            help    = 'Increase debug verbosity.'
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
        dll_name = '%s-plugin' % opts.kind
        # DEBUG print >>sys.stderr, 'Loading module %s' % dll_name
        try:
            if opts.debug_level > 0:
                print >>sys.stderr, 'Loading module {0}'.format(
                    dll_name
                )
            dll = __import__(dll_name)
        except Exception, e:
            print >>sys.stderr, 'No prettyprinter for "%s".' % opts.kind
            print >>sys.stderr, e
            return True
        if opts.ofile:
            try:
                sys.stdout = open( opts.ofile, 'wt' )
            except Exception, e:
                print >>sys.stderr, 'Cannot open "%s" for writing.' % opts.ofile
                return True
        retval = self._session( dll.PrettyPrint, args )
        return retval

if __name__ == '__main__':
    import  __main__
    gpp = GenericPrettyPrinter()
    retval = gpp.main()
    if retval:
        exit(1)
    exit(0)
