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

    def pre_begin_file( self, name = None ):
        super( PrettyPrint, self ).pre_begin_file( name )
        self.widths  = dict()
        self.entries = list()
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
                for i, token in enumerate( parts ):
                    key = str(i)
                    if not key in self.widths:
                        self.widths[i] = len( token )
                    else:
                        self.widths[i] = max(
                            self.widths[i],
                            len( token )
                        )
                # Make sure mount options are in canonical order
                options = parts[ 3 ].split( ',' )
                options.sort()
                parts[ 3 ] = ','.join(
                    options
                )
                self.entries.append( parts )
        except Exception, e:
            print >>sys.stderr, 'Error handling "{0}"'.format( line )
            print >>sys.stderr, e
        return

    def report( self, final = False ):
        if not final:
            # Build formats for each column
            fmt = dict()
            for key in self.widths:
                fmt[ key ] = '{0:<%d}' % self.widths[ key ]
            # Output each line with columns according to formats
            for parts in self.entries:
                clauses = list()
                for i, token in enumerate(parts ):
                    key = str( i )
                    clauses.append(
                        fmt[key].format( token )
                    )
                footnote = None
                if len(parts)>=5 and parts[3]=='nfs' and
                parts[4]=='default":
                    footnote = self.footnote(
                        'NFS default options used; probably slow'
                    )
                self.println(
                    ' '.join( clauses ) +
                    '\t*** See footnote %s'.format( footnote ) if footnote
                    else ''
                )
        return
