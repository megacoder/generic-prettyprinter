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
        self.prolog  = []
        self.ifaces  = []
        self.iface   = {}
        self.bonds   = {}
        self.bridges = {}
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
            if iface[ 'TYPE' ] == 'Bridge':
                self.bridges[ iface[ 'DEVICE' ] ] = iface
            elif iface[ 'TYPE' ] == 'Bonding':
                self.bonds[ iface[ 'DEVICE' ] ] = iface
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
        fmt = "%%%ds='%%s'" % max_name
        for key in sorted( keys ):
            self.println( fmt % (key, self.iface[key]) )
        self.println()
        return

    def report( self, final = False ):
        if final:
            title = 'S U M M A R Y'
            self.println()
            self.println( title )
            self.println( '-' * len( title ) )
            self.println()
            empty = True
            # Sort interface list once and for all
            self.ifaces.sort( key = lambda e: e['NAME'] )
            # Pass 1: construct bridged interfaces
            if self.bridges != {}:
                if not empty:
                    self.println()
                empty = False
                for name in sorted( self.bridges.keys() ):
                    self.println()
                    self.println( 'Bridge {0}'.format( name ) )
                    bridge = self.bridges[ name ]
                    if 'MTU' in bridge.keys():
                        MTU = bridge[ 'MTU' ]
                    else:
                        MTU = '1500'
                    name = bridge[ 'DEVICE' ]
                    for iface in self.ifaces:
                        keys = iface.keys()
                        if 'BRIDGE' in keys and iface[ 'BRIDGE' ] == name:
                            if 'MTU' in keys:
                                PMTU = iface[ 'MTU' ]
                            else:
                                PMTU = '1500'
                            if PMTU == MTU:
                                msg = ''
                            else:
                                msg = ' *** MTU={0}, expected {1}.'.format(
                                    PMTU,
                                    MTU
                                )
                            self.println( ' |' )
                            self.println(
                                ' +-- {0}{1}'.format(
                                    iface[ 'DEVICE' ],
                                    msg
                                )
                            )
            # Pass 2: Bonds
            if self.bonds != {}:
                if not empty:
                    self.println( '\n' )
                empty = False
                for name in sorted( self.bonds.keys() ):
                    bond = self.ifaces[ name ]
                    self.println()
                    self.println( name )
                    for iface in self.ifaces:
                        keys = iface.keys()
                        if 'MASTER' in keys and iface[ 'MASTER' ] == bond:
                            if 'SLAVE' in keys and iface[ 'SLAVE' ] == 'yes':
                                msg = ''
                            else:
                                msg = ' *** slave with no MASTER'
                            self.println( ' |' )
                            self.println(
                                ' +-- {0}{1}'.format(
                                    iface[ 'DEVICE' ],
                                    msg
                                )
                            )
            # Pass 3: TBD
            if empty:
                self.println()
                self.println( 'No bonding or bridges found.' )
        elif 'NAME' in self.iface.keys():
            self._show_iface( self.iface )
        return
