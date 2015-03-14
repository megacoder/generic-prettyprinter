#!/usr/bin/python

import  sys
import  superclass

class   PrettyPrint( superclass.MetaPrettyPrinter ):

    NAME = 'ifcfg-pp'
    DESCRIPTION="""Show ifcfg network files in canonical style."""

    def __init__( self ):
        super( PrettyPrint, self ).__init__()
        return

    def reset( self ):
        super( PrettyPrint, self ).reset()
        self.prolog = []
        self.ifaces = []
        self.iface  = {}
        return

    def ignore( self, name ):
        return False if name.endswith( '.conf' ) else True

    def _normalize( self, iface ):
        keys = iface.keys()
        if 'DEVICE' in keys or 'NAME' in keys:
            if not 'TYPE' in keys:
                iface[ 'TYPE' ] = 'Ethernet'
            if 'DEVICE' in keys and not 'NAME' in keys:
                iface[ 'NAME' ] = iface[ 'DEVICE' ]
            if 'NAME' in keys and not 'DEVICE' in keys:
                iface[ 'DEVICE' ] = iface[ 'NAME' ]
        # print >>sys.stderr, iface
        return iface

    def pre_begin_file( self ):
        self.iface  = {}
        self.prolog = []
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
                if value.startswith( '"' ) or value.startswith( "'" ):
                    value = value[1:-1]
                self.iface[name] = value
        return

    def post_end_file( self ):
        iface = self._normalize( self.iface )
        if 'NAME' in iface.keys():
            self.ifaces.append( iface )
        self.report()
        return

    def _show_iface( self, iface ):
        keys = self.iface.keys()
        herald = '# %s' % iface['NAME']
        for line in self.prolog:
            self.println( line )
        max_name =  max(
            map(
                len,
                keys
            )
        )
        fmt = "%%%ds = '%%s'" % max_name
        for key in sorted( keys ):
            self.println( fmt % (key, self.iface[key]) )
        self.println()
        return

    def report( self, final = False ):
        if final:
            self.ifaces.sort( key = lambda e: e['NAME'] )
            Nifaces = len( self.ifaces )
            empty = True
            title = 'S U M M A R Y'
            self.println( title )
            self.println( '-' * len( title ) )
            self.println()
            # Pass 1: construct bridged interfaces
            for i in range( Nifaces ):
                iface = self.ifaces[ i ]
                keys = iface.keys()
                if 'TYPE' in keys:
                    kind = iface[ 'TYPE' ]
                else:
                    kind = None
                if kind == 'Bridge':
                    empty = False
                    bname = iface[ 'NAME' ]
                    self.println(
                        'Bridge %s' % bname
                    )
                    for sno in range( Nifaces ):
                        slave = self.ifaces[ sno ]
                        try:
                            master = slave[ 'BRIDGE' ]
                        except:
                            master = None
                        if master and master == bname:
                            self.println( '  |' )
                            self.println(
                                '  +-- %s' % slave['NAME']
                            )
                    self.println()
            # Pass 2: construct bonded interfaces
            bonds = {}
            for iface in self.ifaces:
                try:
                    if iface[ 'SLAVE' ]:
                        bonds[ iface[ 'MASTER' ] ] = 0
                except:
                    pass
            for bond in sorted( bonds.keys() ):
                empty = False
                self.println( 'Bond %s' % bond )
                for i in range( Nifaces ):
                    iface = self.ifaces[ i ]
                    try:
                        if iface[ 'MASTER' ] == bond:
                            self.println( '  |' )
                            self.println(
                                '  +-- %s' % iface[ 'NAME' ]
                            )
                    except:
                        pass
                self.println()
            # Pass 3: TBD
            if empty:
                self.println()
                self.println( 'No bonding or bridges found.' )
        elif 'NAME' in self.iface.keys():
            self._show_iface( self.iface )
        return
