#!/usr/bin/python
# vim: et sw=4 ts=4

import  os
import  sys
import  csv
import  superclass

class   PrettyPrint( superclass.MetaPrettyPrinter ):

    NAME = 'vmstat-pp'
    DESCRIPTION = """Display vmstat(1) output in a canonical style."""

    HEADINGS = {
        'r'      : 'procs',
        'b'      : 'procs',
        'swpd'   : 'memory',
        'free'   : 'memory',
        'inact'  : 'memory',
        'active' : 'memory',
        'buff'   : 'memory',
        'cache'  : 'memory',
        'si'     : 'swap',
        'so'     : 'swap',
        'bi'     : 'io',
        'bo'     : 'io',
        'in'     : 'system',
        'cs'     : 'system',
        'us'     : 'cpu',
        'sy'     : 'cpu',
        'id'     : 'cpu',
        'wa'     : 'cpu',
        'st'     : 'cpu'
    }

    def __init__( self ):
        super( PrettyPrint, self ).__init__()
        return

    def reset( self ):
        super( PrettyPrint, self ).reset()
        self.minors = None
        self.content = dict([(h, {}) for h in set(PrettyPrint.HEADINGS.values())])
        return

    def process( self, f = sys.stdin ):
        reader = csv.reader( f, delimiter = ' ', skipinitialspace = True )
        lineno = 0
        for values in reader:
            lineno += 1
            if lineno == 1:
                # This is the main headers, we want to skip them
                pass
            elif lineno == 2:
                # This is the subheaders; flag those we have
                self.minors = values
                for h in values:
                    try:
                        self.content[ PrettyPrint.HEADINGS[h] ][h] = []
                    except Exception, e:
                        print >>sys.stderr, 'Unknown minor header "%s"' % h
                        raise e
            elif values[0] != self.minors[0] and \
            values[0] != PrettyPrint.HEADINGS[ self.minors[0] ]:
                for i, v in enumerate(values):
                    self.content[
                        PrettyPrint.HEADINGS[self.minors[i]]
                    ][
                        self.minors[i]
                    ].append( int(v) )
        return

    def finish( self ):
        for i, minor in enumerate( self.minors ):
            major = PrettyPrint.HEADINGS[minor]
            s = []
            values = self.content[major][minor]
            # values.sort()
            print '%s\t%s\t%d\t%d' % (major, minor, min(values), max(values))
        return
