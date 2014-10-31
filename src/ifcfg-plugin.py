#!/usr/bin/python

import  sys
import  superclass

class   PrettyPrint( superclass.MetaPrettyPrinter ):

    NAME = 'ifcfg-pp'
    DESCRIPTION="""Show ifcfg network files in canonical style."""

    EMPTY = {
        'NAME': None,
        'TYPE': 'Ethernet',
        ' SKP': False,
    }

    def __init__( self ):
        super( PrettyPrint, self ).__init__()
        return

    def reset( self ):
        super( PrettyPrint, self ).reset()
        self.prolog   = []
        self.ifaces   = []
        self.iface    = PrettyPrint.EMPTY
        return

    def pre_begin_file( self ):
        if self.iface != PrettyPrint.EMPTY:
            if not 'NAME' in self.iface.keys():
                self.iface[ 'NAME' ] = self.iface[ 'DEVICE' ]
            self.ifaces.append( self.iface )
        self.iface = PrettyPrint.EMPTY
        return

    def next_line( self, line ):
        if line.startswith( '#' ):
            self.prolog.append( line )
        else:
            parts = line.rstrip().split( '=', 1 )
            if len(parts) != 2:
                self.prolog.append( line )
            else:
                name  = parts[0]
                value = parts[1]
                if not value.startswith('"') and not value.startswith("'"):
                    value = '"' + value + '"'
                self.iface[name] = value
        return

    def post_end_file( self ):
        if self.iface != PrettyPrint.EMPTY:
            self.ifaces.append( self.iface )
        return

    def _show_iface( self, iface ):
        herald = '# %s' % iface['NAME']
        for line in self.prolog:
            print line
        max_name = max( self.iface.keys() )
        print >>sys.stderr, 'max_name={0}'.format( max_name )
        fmt = '%%%ds=%%s' % self.max_name
        for name,value in sorted( self.iface.keys() ):
            print fmt % (name, value)
        return

    def report( self, final = False ):
        print >>sys.stderr, 'final={0}'.format( final )
        if final:
            self.ifaces.sort( key = lambda e: e['NAME'] )
            for i in range( len( self.ifaces ) ):
                if self.ifaces[i]['TYPE'] == 'Bridge':
                    self._show_iface( iface )
                    self.ifaces[i][' SKP'] = True
        return
