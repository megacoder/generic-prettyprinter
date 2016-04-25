#!/usr/bin/python
# Print /etc/fstab getting the fields as close to their intended columns as may
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
        return

    def start( self ):
        self.pre_begin_file()
        return

    def pre_begin_file( self, name ):
        super( PrettyPrint, self ).pre_begin_file( name )
        self.widths = {}
        self.entries = []
        return

    def next_line( self, line ):
        parts = map(
            str.strip,
            line.split( '#', 1 )[0].split()
        )
        nParts = len( parts )
        # Discard all but regular or bind-mount, lines
        try:
            if (nParts == 4) or (nParts == 6):
                for i in range( nParts ):
                    key = str( i )
                    if key in self.widths.keys():
                        self.widths[ key ] = max(
                            self.widths[ key ],
                            len( parts[ i ] )
                        )
                    else:
                        self.widths[ key ] = len( parts[ i ] )
                # Make sure mount options are in canonical order
                options = parts[ 3 ].split( ',' )
                options.sort()
                parts[ 3 ] = ','.join(
                    options
                )
                self.entries.append( (nParts, parts) )
        except Exception, e:
            print >>sys.stderr, 'Error handling "{0}"'.format( line )
            print >>sys.stderr, e
        return

    def report( self, final = False ):
        if not final:
            # Build formats for each column
            fmt = {}
            for key in self.widths.keys():
                fmt[ key ] = '{0:<%d}' % self.widths[ key ]
            # Output each line with columns according to formats
            for (nParts, parts) in self.entries:
                clauses = []
                for i in range( nParts ):
                    key = str( i )
                    clauses.append(
                        fmt[ key ].format(
                            parts[ i ]
                        )
                    )
                self.println(
                    ' '.join( clauses )
                )
            # Final passes check for bad combinations
            first = True
            for (nParts,parts) in self.entries:
                if parts[ 3 ] == 'nfs' and parts[ 4 ] == 'defaults':
                    if first:
                        self.println()
                        first = False
                    self.println(
                        'Mount point {0} uses default options.'.format(
                            parts[ 0 ]
                        )
                    )
        return
