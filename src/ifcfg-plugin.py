#!/usr/bin/python

import  sys
import  superclass

class   PrettyPrint( superclass.MetaPrettyPrinter ):

    NAME = 'ifcfg-pp'
    DESCRIPTION="""Show ifcfg network files in canonical style."""

    def __init__( self ):
        super( PrettyPrint, self ).__init__()
        self.ifcfgs = dict()    # Key is iface name
        self.iface  = None
        return

    def ignore( self, name ):
        """ Ignore directory entries not ending with '.conf' """
        return not name.endswith( '.conf' )

    def moder( self, mode ):
        """ Replace a numeric bonding mode with its alpha form. """
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
            if code in spelling:
                self.footnote(
                    'The mode is actually given as "{0}" in the file.'.format(
                        mode
                    )
                )
                mode = 'mode={0}'.format(
                    spelling[ code ]
                )
        return mode

    def pre_begin_file( self, name = None ):
        self.iface  = dict(
            printed   = False,
            footnotes = list()
        )
        self.prolog = list()
        return

    def next_line( self, line ):
        """ Called with each ifcfg-<*> file line, already rstrip()'ed. """
        if line.startswith( '#' ):
            self.prolog.append( line )
        else:
            # Isolate and strip left- and right-hand portions
            parts = map(
                str.strip,
                line.split( '=', 1 )
            )
            if len(parts) != 2:
                # Treat anything without an equal sign as prolog
                self.prolog.append( line )
            else:
                name  = parts[0]
                value = parts[1]
                # Elide incoming quotes because we will unconditionally
                # quote the value later.
                if value.startswith( '"' ) or value.startswith( "'" ):
                    value = value[1:-1]
                self.iface[name] = value
        return

    def _normalize( self, iface ):
        """ The rules for creating an ifcfg-<*> file are very lax.
            As a result, many defintions omit implied values.  In
            the interest of clarity, try to intuit the companion
            values if a related setting is used. """
        #
        if 'DEVICE' in iface and 'NAME' not in iface:
            self.footnote( 'Intuited NAME from DEVICE' )
            iface['NAME'] = iface['DEVICE']
        #
        if 'NAME' in iface and 'DEVICE' not in iface:
            self.footnote( 'Intuited DEVICE from NAME' )
            iface['DEVICE'] = iface['NAME']
        #
        if 'MASTER' in iface and 'TYPE' not in iface:
            self.footnote( 'Interpreted as bonded interface' )
            iface['TYPE'] = 'Bonding'
        #
        if not 'TYPE' in iface:
            self.footnote( 'Assuming type is "Ethernet"' )
            iface[ 'TYPE' ] = 'Ethernet'
        #
        if 'MTU' not in iface:
            mtu = '1500'
            self.footnote( 'MTU missing; assuming {0}'.format( mtu ) )
            iface['MTU'] = mtr
        # print >>sys.stderr, iface
        return iface

    def post_end_file( self ):
        """ Normalize and save the interface definition. """
        iface = self._normalize( self.iface )
        name = iface['NAME']
        self.ifcfgs[name] = iface
        self.report()
        return

    def _get_vlans_for( self, name ):
        """ Return names of VLAN interfaces based on the interface
            name.  The VLAN naming scheme just adds a ".<n>" to the
            name of the base interface. """
        vname = name + '.'
        vlans = [
            iface['NAME'] for iface in self.ifcfgs if iface['NAME'].startswith(vname)
        ]
        return vlans

    def _show_iface( self, iface ):
        """ Output the ifcfg-<name> entries, one to a line in movie-credit
            format, aligned around the '=' sign. """
        return

    def _report_bridges( self, others = False ):
        bridges = [
            iface for iface in self.ifcfgs if iface['TYPE'] == 'Bridge'
        ]
        for bridge in sorted( bridges ):
            if others:
                self.println()
            else:
                title = 'BRIDGE'
                self.println( title )
                self.println( '-' * len( title ) )
            others = True
            self.println()
            name = bridge[ 'NAME' ]
            bridge_mtu = bridge[ 'MTU' ]
            title = '{0}'.format( name )
            self.println( title )
            self.println( '-' * len( title ) )
            self._get_vlans_for( name )
            members = [
                iface for iface in self.ifcfgs if 'BRIDGE' in iface
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
                self._get_vlans_for( member['NAME' ] )
        return others

    def _report_bonds( self, others = False ):
        # Fixup: Some bonds are explicity declared
        bonds = {}
        for iface in self.ifcfgs:
            if 'TYPE' in iface and iface['TYPE'] == 'Bond':
                bonds[iface['NAME']] = iface
        # Fixup: Some bonds are inferred by being mentioned as a 'MASTER'
        for iface in self.ifcfgs:
            if 'MASTER' in iface :
                bonds[iface['MASTER']] = iface
        #
        for bond in sorted( bonds ):
            if others:
                self.printlin()
            else:
                title = 'BONDING'
                self.println( title )
                self.println( '-' * len(title))
                self.println()
            others = True
            self.println( bond )
            vlans = self._get_vlans_for( bond )
            for vlan in vlans:
                self.println( '  |' )
                self.println( '  +-- {0}'.format( path['NAME'] ) )
            paths = [
                iface for iface in self.ifcfgs if 'MASTER' in iface
                and iface['MASTER'] == bond
            ]
            for path in paths:
                self.println( '  |' )
                self.println( '  +-- {0}'.format( path['NAME'] ) )
        return others

    def _get_ifcfgs_for_type( self, kind, seen = False ):
        """ Return a list of interface names of KIND=kind. If none,
            return None. """
        kinds = [
            iface['NAME'] for iface in self.ifcfgs if iface['TYPE'] == kind and iface['printed'] == seen
        ]
        return kinds if len(kinds) else None

    def _get_bridge_members( self, name ):
        members = [
            iface['NAME'] for iface in self.ifcfgs if 'BRIDGE' in iface and iface['BRIDGE'] == name
        ]
        return members if len(members) > 0 else None

    def _get_bond_members( self, name ):
        """ Find slave interfaces for the named bond. """
        members = [
            iface['NAME'] for iface in self.ifcfgs if 'SLAVE' in iface and iface['SLAVE'] == 'yes' and 'master' in iface and iface['MASTER'] == name
        ]
        return members

    def _get_ipaddr_for( self, name ):
        IP = self.ifcfgs[name]['IPADDR'] if 'IPADDR' in self.ifcfgs[name] else None
        return IP

    def _final_report( self ):
        self.println()
        title = 'S U M M A R Y'
        self.println( title )
        self.println( '=' * len( title ) )
        self.printlin()
        others = False
        # Pass 1: construct bridged interfaces
        bridge_namess = self._names_of_kind( 'Bridge' )
        if bridge_names:
            title = 'B R I D G E S'
            self.println( title )
            self.println( '-' * len(title) )
            self.println()
            for name in sorted( bridges_names ):
                IP = self._get_ipaddr_for( name )
                title = '{0}'.format(
                    name,
                    ' ({{0}})'.format( IP ) if IP else ''
                )
                self.println( title )
                self.println( '-' * len( title ) )
                vlans = self._get_vlans_for( name )
                for vlan in sorted( vlans ):
                    IP = self._get_ipaddr_for( vlan )
                    self.printon( '  |' )
                    self.println( '  +-- {0}{1}'.format(
                        self.ifcfgs['NAME']),
                        ' ({0})'.format( IP ) if IP else ''
                    )
                # Make sure all members of this bridge use a common MTU
                bridge_mtu = self.ifcfgs[name][ 'MTU' ]
                members = self._get_bridge_members( name )
                for member in members:
                    member_mtu = self.ifcfgs[member][ 'MTU' ]
                    if bridge_mtu != member_mtu:
                        msg = ' *** Bridge MTU {0}, not {1} as member.'.format(
                            bridge_mtu,
                            member_mtu
                        )
                    else:
                        msg = ''
                    self.println( '  |' )
                    self.println( '  +-- {0}{1}'.format(member['NAME'], msg ) )
        # Pass 2: Bonds
        bonds = self._get_ifcfgs_for_type( 'Bond' )
        if bonds:
            title = 'B O N D I N G'
            self.println()
            self.println( title )
            self.println( '=' * len(title) )
            self.println()
            for name in bonds:
                IP = self._get_ipaddr_for( name )
                self.println( '  |' )
                self.println( '  +-- {0}'.format(
                        name,
                        ' ({0})'.format( IP ) if IP else ''
                    )
                )
                # Show any VLANs defined for bond; not sure this is
                # even valid, but anyway...
                vlans = self._get_vlans_for( name )
                for vlan in sorted( vlans ):
                    IP = self._get_ipaddr_for( vlan )
                    self.println( '  |' )
                    self.println( '  +-- {0}'.format(
                        self.ifcfgs['NAME'],
                        ' ({0})'.format( IP ) if IP else ''
                    ))
                # Show members of this bond
                slaves = self._get_bond_members( name )
                if slaves:
                    for slave in sorted( slaves ):
                        IP = self._get_ipaddr_for( slave )
                        self.println( '  |' )
                        self.println( '  +-- {0}'.format(
                            slave,
                            ' ({0})'.format( IP ) if IP else ''
                        ))
        return

    def report( self, final = False ):
        if final:
            self._final_report()
        elif 'NAME' in self.iface:
            # Dump any accumulated prolog
            if len(self.prolog) > 0:
                for line in self.prolog:
                    self.println( line )
                self.println()
            # Output iface lines, sorted in order
            max_name =  max(
                map(
                    len,
                    iface
                )
            )
            fmt = '{{0:>{0}}}={{1}}'.format( max_name )
            for key in sorted( iface ):
                self.println(
                    fmt.format( key, self.iface[key] )
                )
        return
