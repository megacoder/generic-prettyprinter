#!/usr/bin/env python
#!/usr/bin/python
# vim: et sw=4 ts=4

import  argparse
try:
    import  importlib
except:
    class FunkyBob():
        def __init__( self ):
            pass
        def import_module( self, name ):
            module = __import__( name )
            return module
    importlib = FunkyBob()

import  os
import  sys

try:
    import  version
except:
    class version:
        Version = 'v?.?.?'

import  traceback

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

    def _session( self, Handler, names = [[]] ):
        handler = Handler()
        # Allow plugin to figure out where its files are
        if len( names ) == 0:
            names = handler.own_glob()
        # Here is the session
        handler.start()
        handler.advise( names )
        retval = True
        try:
            for name in names:
                handler.process( name )
            retval = False
        except Exception, e:
            traceback.print_exc()
        handler.finish()
        return retval

    def process( self, f = sys.stdin ):
        for line in f:
            self.println( line.rstrip() )
        return

    def main( self ):
        # print 'Generic prettyprinter (gpp) Version {0}'.format( version.Version )
        sys.path.insert( 0, os.path.dirname( __file__ ) )
        # Intuit the kind of prettyprinter we want to be
        kind = 'text'
        if sys.argv[0].endswith( '-pp' ):
            kind = os.path.basename( sys.argv[0] )[:-3]
        p = argparse.ArgumentParser(
            description     = """A modular pretty printer that is easy to
            extend.""",
            prog            = 'gpp',
#           usage           = '%{prog} [-o ofile] [-t type] [file..]',
#           version         = version.Version,
            formatter_class = argparse.ArgumentDefaultsHelpFormatter,
            epilog = """Every attempt is made to provide a
            correctness-preserving tansformation.  The content may look
            different but correct input should result in correct output.
            The idea is for functionally-equivalent input to produce
            functionally-equivalent output so that two different file
            organizations can be compared, even if the line formatting
            differs or the line order differs."""
        )
        p.add_argument(
            '-D',
            '--debug',
            action  = 'count',
            dest    = 'debug_level',
            default =  0,
            help    = 'Increase debug verbosity.'
        )
        p.add_argument(
            'files',
            metavar = 'FILE',
#           action  = 'append',
#           type    = list,
            nargs   = '*',
#           default = [],
#           dest    = 'files',
#           default = [],
        )
        fake_ofile = '{stdout}'
        p.add_argument(
            '-o',
            '--out',
            action  = 'store',
            type    = str,
            dest    = 'ofile',
            default =  fake_ofile,
            help    = 'output written to file',
            metavar = 'PATH'
        )
        p.add_argument(
            '-t',
            '--type',
            metavar  = 'TYPE',
            action   = 'store',
            type     = str,
            default  = 'text',
            dest     = 'kind',
            help     = 'kind of pretty-printer desired',
            required = True,
        )
        p.add_argument(
            '-v',
            '--version',
            action  = 'version',
            default = version.Version,
            help    = 'program version',
        )
        opts = p.parse_args()
        if opts.ofile == fake_ofile:
            opts.ofile = None
        # Here we go...
        module_name = '{0}-plugin'.format( opts.kind )
        try:
            if opts.debug_level > 0:
                print >>sys.stderr, 'Loading module {0}'.format(
                    module_name
                )
            module = importlib.import_module( module_name )
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
        retval = self._session( module.PrettyPrint, opts.files )
        return retval

if __name__ == '__main__':
    import  __main__
    genpp = GenericPrettyPrinter()
    retval = genpp.main()
    if retval:
        exit(1)
    exit(0)
