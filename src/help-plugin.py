##/usr/bin/python
# vim: et sw=4 ts=4

import  os
import  sys
import  superclass
import  importlib

class PrettyPrint( superclass.MetaPrettyPrinter ):
    NAME        = 'plugins'
    DESCRIPTION = 'Display list of known plugins.'
    GLOB        = None

    def __init__( self ):
        super( PrettyPrint, self ).__init__()
        return

    # Regardless of what filenames are passed, do none
    def ignore( self, fn ):
        return True
    def pre_begin_file( self, fn = None ):
        pass
    def begin_file( self, fn = None ):
        pass
    def next_line( self, line ):
        pass
    def close_file( self, fn = None ):
        pass
    def post_close_file( self, fn = None ):
        pass

    def report( self, final = False ):
        if not final: return
        plugin_dir = os.path.dirname(
            os.path.realpath( __file__ )
        )
        TAIL = '-plugin.py'
        L_TAIL = len( TAIL )
        names = [
            # Take 'FOO-plugin.py' and record 'FOO'
            f[:-L_TAIL] for f in os.listdir(plugin_dir) if f.endswith(
                TAIL
            )
        ]
        width = max(
            [ 6 ] + map( len, names )
        )
        fmt = '{{0:{0}s}} {{1}}'.format( width )
        for name in sorted( names ):
            try:
                module_name = '{0}-plugin'.format( name )
                module = importlib.import_module( module_name )
            except Exception, e:
                print >>sys.stderr, 'Cannot import module "{0}"'.format( module_name )
                raise e
            pp = module.PrettyPrint()
            self.println(
                fmt.format(
                    name,
                    ' '.join( pp.DESCRIPTION.splitlines() )
                )
            )
        return
