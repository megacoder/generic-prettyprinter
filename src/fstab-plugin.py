#!/usr/bin/python
# Print /etf/fstab getting the fields as close to their intended columns as may
# be.  Long fields push the remainder of the line over as little as is possible
# so that the columns come nearer to alignment.

import	os
import	sys
import  superclass

class   PrettyPrint( superclass.MetaPrettyPrinter ):

    NAME = 'fstab-pp'
    DESCRIPTION = """Display /etc/fstab files in canonical style."""
    GLOB = None

    def __init__( self ):
        super( PrettyPrint, self ).__init__()
        return

    def start( self ):
        super( PrettyPrint, self ).reset()
        self.pre_begin_file()
        return

    def pre_begin_file( self ):
        super( PrettyPrint, self ).pre_begin_file()
        self.widths = {}
        self.entries = []
        return

    def next_line( self, line ):
        parts = line.split( '#', 1 )[0].strip().split()
        L = len( parts )
        if (L == 4) or (L == 6):
            for i in xrange( 0, L ):
                # Reformat only regular, or bind-mount, lines
                if L == 4 or L == 6:
                    k = len( parts[i] )
                    try:
                        w = self.widths[i]
                    except:
                        w = k
                    self.widths[i] = max( k, w )
            self.entries.append( (L, parts) )
        return

    def report( self, final = False ):
        if not final:
            for (L, parts) in self.entries:
                clauses = []
                for i in xrange( 0, L ):
                    fmt = '{0:<%d}' % self.widths[ i ]
                    clauses.append(
                        fmt.format( parts[ i ] )
                    )
                self.println( ' '.join( clauses ) )
            for (L,parts) in self.entries:
                try:
                    if parts[ 3 ] == 'nfs' and parts[ 4 ] == 'defaults':
                        self.println(
                            'Mount point {0} uses default options.'.format(
                                parts[ 0 ]
                            )
                        )
                except:
                    pass
            self.println()
        return
