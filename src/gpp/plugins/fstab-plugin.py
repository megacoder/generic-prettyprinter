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

    def __init__( self ):
        super( PrettyPrint, self ).__init__()
        self.reset()
        return

    def reset( self ):
        super( PrettyPrint, self ).reset()
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

    def dump( self ):
        for (L, parts) in self.entries:
            sep = ''
            for i in xrange( 0, L ):
                fmt = '%%s%%-%ds' % self.widths[i]
                print fmt % (sep, parts[i]),
                sep = ' '
            print
        return

    def begin_file( self, name ):
        super( PrettyPrint, self ).begin_file( name )
        self.reset()
        return

    def end_file( self, name ):
        self.dump()
        super( PrettyPrint, self ).end_file( name )
        return
