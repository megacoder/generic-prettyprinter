#!/usr/bin/python

import  os
import  sys
import  math

class   SysctlPrettyprint( object ):

    VERSION = "1.0.0"

    def __init__( self, out = sys.stdout ):
        self.out = out
        self.lines = []
        self.fmt = "%31s\t%s"
        return

    def load( self, fyle = sys.stdin ):
        self.lines = []
        maxlen = 0
        for line in fyle:
            n = line.find( '#' )
            if n > -1: line = line[:n]
            try:
                key, value = line.split( '=', 1 )
            except Exception, e:
                continue
            k = key.strip()
            maxlen = max( maxlen, len(k) )
            self.lines.append( (k, value.strip()) )
        self.fmt = "%%%ds = %%s" % maxlen
        self.lines.sort( key = lambda (key,value): key.lower() )
        return

    def show( self, out = None, line_number = False ):
        if out is None:
            out = self.out
        n = 0
        for key,value in self.lines:
            if line_number:
                n += 1
                print >>out, "%-4s" % ('%d:' % n),
            print >>out, self.fmt % (key, value)
        return

if __name__ == '__main__':
    from    optparse    import  OptionParser

    p = OptionParser(
        prog=os.path.basename( sys.argv[0] ),
        version="%prog " + SysctlPrettyprint.VERSION,
        usage="usage: %prog [-o ofile] [file...]",
        description="""Display sysctl.conf file in canonical form.""",
        epilog = '''Reads from stdin if no files are given.'''
    )
    p.add_option( "-n", "--number", dest="line_number", action="store_true",
                 default=False, help="show line numbers" )
    p.add_option( "-o", "--out", dest="ofile", help="write output to file",
                 metavar="FILE", default=None )
    (options, args) = p.parse_args()
    if options.ofile is None:
        out = sys.stdout
    else:
        out = open( options.ofile, 'wt' )
    if len(args) == 0:
        spp = SysctlPrettyprint( out=out )
        spp.load()
        spp.show( line_number = options.line_number )
    else:
        for optarg in args:
            try:
                fd = open( optarg )
            except Exception, e:
                print >>sys.stderr, "Cannot open '%s' for reading." % optarg
                continue
            spp = SysctlPrettyprint( out=out )
            spp.load( fd )
            fd.close()
            spp.show()
