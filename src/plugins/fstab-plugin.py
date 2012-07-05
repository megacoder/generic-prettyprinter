#!/usr/bin/python
# Print /etf/fstab getting the fields as close to their intended columns as may
# be.  Long fields push the remainder of the line over as little as is possible
# so that the columns come nearer to alignment.

import	os
import	sys

class   PrettyPrint( object ):

    def __init__( self ):
        self.reset()
        return

    def reset( self ):
        return

    def pad(self, parts, cols):
        s = ""
        while len(parts) > 0:
            c = cols.pop(0)
            l = len(s)
            n = c - l
            if n < 1 and c > 0: n = 1
            s = s + " " * n + parts.pop(0)
        return s

    def process( self, f = sys.stdin ):
        for line in f:
            line = line.strip()
            if not line.startswith( '#' ):
                parts = line.split()
                l = len(parts)
                # Reformat only regular, or bind-mount, lines
                if l == 4 or l == 6:
                    #
                    opts = parts[3].split(',')
                    opts.sort()
                    parts[3]  = ",".join(opts)
                    #
                    line = self.pad(parts,[
                        0, 24, 47, 55, 77, 79
                    ])
            print line
        return

    def finish( self ):
        return
