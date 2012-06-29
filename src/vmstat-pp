#!/usr/bin/python
# vim: et sw=4 ts=4

me = 'vmstat-pp'

import  os
import  sys
import  csv

class   VMPP( object ):
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
        self.reset()
        return

    def reset( self ):
        self.minors = None
        self.content = dict([(h, {}) for h in set(VMPP.HEADINGS.values())])
        return

    def do_name( self, name ):
        if os.path.isdir( name ):
            self.do_dir( name )
        elif os.path.isfile( name ):
            self.do_file( name )
        else:
            print >>sys.stderr, 'Ignoring "%s".' % name
        return

    def do_dir( self, dn ):
        try:
            names = os.listdir( dn )
        except Exception, e:
            print >>sys.stderr, 'Cannot read directory "%s".' % dn
            raise e
        names.sort()
        for name in names:
            if os.path.isdir( name ) or name.endswith( '.conf' ):
                self.do_name( os.path.join( dn, name ) )
        return

    def do_file( self, fn ):
        try:
            f = open( fn, 'rt' )
        except Exception, e:
            print >>sys.stderr, "Cannot open '%s' for reading." % fn
            raise e
        self.process( f )
        f.close()
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
                        self.content[ VMPP.HEADINGS[h] ][h] = []
                    except Exception, e:
                        print >>sys.stderr, 'Unknown minor header "%s"' % h
                        raise e
            elif values[0] != self.minors[0] and \
            values[0] != VMPP.HEADINGS[ self.minors[0] ]:
                for i, v in enumerate(values):
                    self.content[
                        VMPP.HEADINGS[self.minors[i]]
                    ][
                        self.minors[i]
                    ].append( int(v) )
        return

    def report( self ):
        print self.content
        for i, minor in enumerate( self.minors ):
            major = VMPP.HEADINGS[minor]
            s = []
            values = self.content[major][minor]
            # values.sort()
            print '%s\t%s\t%d\t%d' % (major, minor, min(values), max(values))
        return

if __name__ == '__main__':
    me = os.path.basename( sys.argv[0] )
    vpp = VMPP()
    if len( sys.argv ) == 1:
        vpp.process()
    else:
        for fn in sys.argv[1:]:
            vpp.do_name( fn )
    vpp.report()
    exit(0)
