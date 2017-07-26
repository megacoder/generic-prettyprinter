#!/usr/bin/python
# vim: et sw=4 ts=4

import  os
import  sys
import  csv
import  superclass
import  align

class   PrettyPrint( superclass.MetaPrettyPrinter ):

    NAME = 'vmstat-pp'
    DESCRIPTION = """Display vmstat(1) output in a canonical style."""

    def __init__( self ):
        super( PrettyPrint, self ).__init__()
        return

    def reset( self ):
        super( PrettyPrint, self ).reset()
        self._prepare()
        return

    def _prepare( self ):
        self.timestamp = None
        self.entries   = align.Align( titles = 1 )
        return

    def begin_file( self, name ):
        super( PrettyPrint, self ).begin_file( name )
        self._prepare()
        return

    def end_file( self, name ):
        super( PrettyPrint, self ).end_file( name )
        return

    def next_line( self, line ):
        if line.startswith( 'Linux OSW' ):
            pass
        elif line.startswith( 'zzz ***' ):
            self.timestamp = line[7:]
        elif line.startswith( 'procs' ):
            pass
        elif line.startswith( ' r ' ):
            self.entries.add( line.split() )
        elif line.startswith( 'SNAP_INTERVAL' ):
            pass
        elif line.startswith( 'CPU_COUNT' ):
            pass
        elif line.startswith( 'OSWBB_ARCHIVE_DEST' ):
            pass
        else:
            self.entries.add( line.split() )
        return

    def _show( self, tokens ):
        line = ''
        sep  = ''
        for i in xrange( 0, len(tokens) ):
            fmt = '%%s%%%ds' % self.widths[i]
            line += fmt % (sep, tokens[i])
            sep = '  '
        self.println( line )
        return

    def report( self, final = False ):
        if not final:
            for _,tokens in self.entries.get_items():
                self.println( ' '.join( tokens ) )
            self._prepare()
        return

if __name__ == '__main__':
	fn = '<selftest>'
	pp = PrettyPrint()
	pp.pre_begin_file()
	pp.begin_file( fn )
	for line in [

        'procs -----------memory---------- ---swap-- -----io---- -system-- ------cpu-----',
         'r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st',
         '1  0  52016 1444604   1192 11392964    0    0    12    84    2   20 20 11 68  1  0',
         '0  0  52016 1443588   1192 11393000    0    0     0    71 1833 2378  8  5 86  1  0',
         '1  0  52016 1444628   1192 11393024    0    0     0     1 1725 2283  7  5 88  0  0',
         '1  0  52016 1445008   1192 11393020    0    0     0     0 1709 2257  7  5 88  0  0',
         '0  0  52016 1443904   1192 11392952    0    0     0     0 1867 2427  9  5 86  0  0',

	]:
		pp.next_line( line )
	pp.end_file( fn )
	pp.post_end_file()
	pp.report( final = True )

