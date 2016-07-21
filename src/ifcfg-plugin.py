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

    def moder( self, mode ):
        if mode.startswith( 'mode=' ):
            spelling = {
                '0': 'balance-rr',
                '1': 'active-backup',
                '2': 'balance-xor',
                '3': 'broadcast',
                '4': '802.3ad',
                '5': 'balance-tlb',
                '6': 'balance-alb',
            }
            code = mode[ len('mode=') ]
            if code in spelling.keys():
                self.footnote(
                    'The mode is actually given as "{0}" in the file.'.format(
                        mode
                    )
                )
                mode = 'mode={0}'.format(
                    spelling[ code ]
                )
        return mode

    def _normalize( self, iface ):
        keys = iface.keys()
        if 'DEVICE' in keys or 'NAME' in keys:
            if 'MASTER' in keys and not 'TYPE' in keys:
                iface[ 'TYPE' ] = 'Bonding'
            if not 'TYPE' in keys:
                iface[ 'TYPE' ] = 'Ethernet'
            if 'DEVICE' in keys and not 'NAME' in keys:
                iface[ 'NAME' ] = iface[ 'DEVICE' ]
            if 'NAME' in keys and not 'DEVICE' in keys:
                iface[ 'DEVICE' ] = iface[ 'NAME' ]
            if not 'MTU' in keys:
                iface[ 'MTU' ] = '1500'
                self.footnote(
                    '{0} did not supply an MTU, 1500 assumed.'.format(
                        iface['NAME']
                    )
                )
            # Sort parameters if needed
            if 'BONDING_OPTS' in keys:
                tokens = iface['BONDING_OPTS'].split()
                tokens.sort()
                tokens = [
                    self.moder(s) for s in tokens
                ]
                iface['BONDING_OPTS'] = ' '.join( tokens )
        # print >>sys.stderr, iface
        return iface

    def pre_begin_file( self, fn = None ):
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
        keys = iface.keys()
        if 'NAME' in keys:
            self.ifaces.append( iface )
            if iface[ 'TYPE' ] == 'Bridge':
                self.bridges[ iface[ 'DEVICE' ] ] = iface
            elif iface[ 'TYPE' ] == 'Bonding':
                self.bonds[ iface[ 'DEVICE' ] ] = iface
            if 'MASTER' in keys:
                self.bonds[ iface[ 'MASTER' ] ] = 0
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

    def _report_bridges( self, others = False ):
        bridges = [
            iface for iface in self.ifaces if iface['TYPE'] == 'Bridge'
        ]
        if len( bridges ) > 0:
            if others:
                self.println()
            others = True
            title = 'BRIDGE'
            self.println( title )
            self.println( '-' * len( title ) )
            for bridge in bridges:
                self.println()
                name = bridge[ 'NAME' ]
                bridge_mtu = bridge[ 'MTU' ]
                title = '{0}'.format( name )
                self.println( title )
                self.println( '-' * len( title ) )
                members = [
                    iface for iface in self.ifaces if 'BRIDGE' in iface.keys()
                    and iface['BRIDGE'] == name
                ]
                for member in members:
                    member_mtu = member[ 'MTU' ]
                    if bridge_mtu != member_mtu:
                        msg = ' *** Bridge MTU {0}, not {1} as member.'.format(
                            bridge_mtu,
                            member_mtu
                        )
                    else:
                        msg = ''
                    self.println( '  |' )
                    self.println( '  +-- {0}{1}'.format(member['NAME'], msg ))
        return others

    def _report_bonds( self, others = False ):
        if others:
            self.println( '\n' )
        # Some bonds are explicity declared
        bonds = {}
        for iface in self.ifaces:
            if 'TYPE' in iface.keys() and iface['TYPE'] == 'Bond':
                bonds[iface['NAME']] = iface
        # Some bonds are inferred by being mentioned as a 'MASTER'
        for iface in self.ifaces:
            if 'MASTER' in iface.keys():
                bonds[iface['MASTER']] = iface
        keys = bonds.keys()
        if len(keys) > 0:
            if others:
                self.println()
            others = True
            title = 'BONDING'
            self.println( title )
            self.println( '-' * len(title))
            for bond in sorted( bonds ):
                self.println()
                self.println( bond )
                paths = [
                    iface for iface in self.ifaces if 'MASTER' in iface.keys()
                    and iface['MASTER'] == bond
                ]
                for path in paths:
                    self.println( '  |' )
                    self.println( '  +-- {0}'.format( path['NAME'] ) )
        return others

    def report( self, final = False ):
        if final:
            title = 'S U M M A R Y'
            self.println()
            self.println( title )
            self.println( '-' * len( title ) )
            others = False
            # Sort interface list once and for all
            self.ifaces.sort( key = lambda e: e['NAME'] )
            # Pass 1: construct bridged interfaces
            others = self._report_bridges( others )
            # Pass 2: Bonds
            others = self._report_bonds( others )
            # Pass 3: TBD
            if not others:
                self.println()
                self.println( 'No bonding or bridges found.' )
        elif 'NAME' in self.iface.keys():
            self._show_iface( self.iface )
        return
