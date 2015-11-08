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

    def _do_session( self, handler ):
        handler.pre_begin_file()
        handler.do_open_file()
        handler.post_end_file()
        return

    def session( self, Handler, names = [] ):
        handler = Handler()
        argc = len( sys.argv )
        n = len( names )
        # Allow plugin to figure out where its files are
        if n < 1:
            names = handler.own_glob()
            n = len( names )
        # Here is the session
        handler.start()
        # Iterate through the names
        handler.advise( argc = n )
        for name in names:
            handler.do_name( name )
        handler.finish()
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
        if opts.ofile is not None:
            try:
                print >>sys.stderr, 'Redirecting output to {0}'.format(
                    opts.ofile
                )
                sys.stdout = open( opts.ofile, 'wt' )
            except Exception, e:
                print >>sys.stderr, 'Cannot open "%s" for writing.' % opts.ofile
                return True
        retval = self.session( Handler = dll.PrettyPrint, names = args )
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
        retval = self.session( Handler = dll.PrettyPrint, names = args )
        return retval

if __name__ == '__main__':
    import  __main__
    gpp = GenericPrettyPrinter()
    retval = gpp.main()
    if retval:
        exit(1)
    exit(0)
