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
            used   = False
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
        # footnotes = []
        if 'DEVICE' in iface and 'NAME' not in iface:
            # footnotes.append( 'Intuited NAME from DEVICE' )
            self.footnote( 'Intuited NAME from DEVICE' )
            iface['NAME'] = iface['DEVICE']
        if 'NAME' not in iface:
            # footnotes.append( 'No name for ifcfg {0}'.format( iface ) )
            self.footnote( 'No name for ifcfg {0}'.format( iface ) )
            iface['NAME'] = '***'
        #
        if 'NAME' in iface and 'DEVICE' not in iface:
            # footnotes.append( 'Intuited DEVICE from NAME' )
            self.footnote( 'Intuited DEVICE from NAME' )
            iface['DEVICE'] = iface['NAME']
        #
        if 'MASTER' in iface and 'TYPE' not in iface:
            # footnotes.append( 'Interpreted as bonded interface' )
            self.footnote( 'Assuming this is a bonded interface' )
            iface['TYPE'] = 'Bonding'
        #
        if not 'TYPE' in iface:
            # footnotes.append( 'Assuming type is "Ethernet"' )
            self.footnote( 'Assuming type is "Ethernet"' )
            iface[ 'TYPE' ] = 'Ethernet'
        #
        if 'MTU' not in iface:
            mtu = '1500'
            # footnotes.append( 'MTU missing; assuming {0}'.format( mtu ) )
            self.footnote( 'MTU missing; assuming {0}'.format( mtu ) )
            iface['MTU'] = mtu
        # print >>sys.stderr, iface
        return iface

    def post_end_file( self ):
        """ Normalize and save the interface definition. """
        iface = self._normalize( self.iface )
        name = iface['NAME']
        self.ifcfgs[name] = iface
        return

    def _get_vlans_for( self, name ):
        """ Return names of VLAN interfaces based on the interface
            name.  The VLAN naming scheme just adds a ".<n>" to the
            name of the base interface. """
        vname = name + '.'
        vlans = [
            name for name in self.ifcfgs if name.startswith( vname )
        ]
        return vlans

    def _get_bridge_members( self, name ):
        """ Get names of interfaces which mention the desired bridge name.
            If there are none, returns the empty set. """
        candidates = self._get_names_for_type( 'Bond' )
        #for iface in self.ifcfgs:
        #    if self.ifcfgs[iface]['TYPE'] == 'Bond' and self.ifcfgs[iface]['BRIDGE'] == name:
        #        members.append( iface )
        members = [
            member for member in self.ifcfgs if self.ifcfgs[member]['TYPE']
            == 'Bond' and self.ifcfgs[member]['BRIDGE'] == name
        ]
        return members

    def _get_bond_members( self, name ):
        """ Find slave interfaces for the named bond. """
        members = [
            iface['NAME'] for iface in self.ifcfgs if 'SLAVE' in iface and iface['SLAVE'] == 'yes' and 'master' in iface and iface['MASTER'] == name
        ]
        return members

    def _get_ipaddr_for( self, name ):
        IP = self.ifcfgs[name]['IPADDR'] if 'IPADDR' in self.ifcfgs[name] else None
        return IP

    def _iprint( self, lines, indent = 0 ):
        leadin = '  ' * indent
        for line in lines.splitlines():
            self.println( '{0}{1}'.format( leadin, line ) )
        return

    def _indented_print( self, indent, msg ):
        padding = '  ' * indent
        for line in msg.splitlines():
            self.println( '{0}{1}'.format( padding, line ) )
        return

    def _network_tree( self, node, components = None, indent = 0 ):
        for name in self._get_names_for_type( theType ):
            IP = self._get_ipaddr_for( name )
            title = '{0}{1}'.format(
                name,
                ' ({0})'.format( IP ) if IP else ''
            )
            self._indented_print( indent, title )
            self._indented_print( indent, '-' * len(title) )
            vlans = self._get_vlans_for( name )
            for vlan in vlans:
                IP = self._get_ipaddr_for( vlan )
                title = '{0}{1}'.format(
                    name,
                    ' ({0})'.format( IP ) if IP else ''
                )
                self._indented_print(
                    indent,
                    ' |\n +--- {0}{1}'.format(
                        vlan,
                        ' ({0})'.format( IP ) if IP else ''
                    )
                )
            pass
            # Process possible children, in order provided
            for child in children:
                if child == 'Bond':
                    pass
                elif child == 'Ethernet':
                    pass
                else:
                    self.println( 'Dunno about "{0}".'.format( child ) )
        return

    def _used( self, node, value = True ):
        node['used'] == value
        return

    def _tree( self, n, indent = 0 ):
        for vlan in self.vlans( n ):
            self.iprint( ' |\n +--- {0}'.format( vlan ), indent )
            for (t,v) in self.ifcfgs[n]['roster']:
                members = self._find_all( t, v, n )
                for member in members:
                    self._iprint( ' |\n +--- {0}'.format( mamber ), indent )
                    self._tree( member, indent + 1 )
        return


    def _NIC_tree( self ):
        for TYPE in [
            'Bridge',
            'Bond',
            'Ethernet'
        ]:
            members = self._find_all( TYPE, None, None )
            for n in sorted( members ):
                self.println()
                self._iprint( fmt_nic( n ) )
                self._tree( n )
        return

    def _find_all( self, wanted, v = None, n = None ):
        # Gather all unused nodes of this type
        candidates = [
            c for c in self.ifcfgs if (
                self.ifcfgs[c]['TYPE'] == wanted and not self.ifcfgs[c]['used']
            )
        ]
        if not v:
            return candidates
        # Filter candidates by checking value of the named attribute
        members = [
            c for c in candidates if v in self.ifcfgs[c] and
            self.ifcfgs[c][v] == n
        ]
        return members

    def _node_names_of_type( self, wanted ):
        names = [
            n['NAME'] for n in self.ifcfgs if n['TYPE'] == wanted
        ]
        return names

    def _get_names_for_type( self, wanted, used = False ):
        names = [
            name for name in self.ifcfgs if (
                (self.ifcfgs[name]['TYPE'] == wanted) and
                (self.ifcfgs[name]['used'] == used)
            )
        ]
        return names if len(names) else None

    def _final_report( self ):
        self.println()
        title = 'S U M M A R Y'
        self.println( title )
        self.println( '=' * len( title ) )
        found_any = False
        # Pass 1: construct bridged interfaces
        bridges = self._node_names_of_type( 'Bridge' )
        if bridges:
            self._network_tree( node, [ 'Bond', 'Ethernet' ] )
            pass
        for key in sorted( self_get_nodes( 'Bridge' ) ):
            pass
        self._network_tree( 'Bridge', [ 'Bond', 'Ethernet' ] )
        if True:
            return
        # Pass 2: Bonds
        bonds = self._get_names_for_type( 'Bond' )
        if bonds:
            found_any = True
            title = 'B O N D I N G'
            self.println()
            self.println( title )
            self.println( '=' * len(title) )
            for name in bonds:
                self.println()
                IP = self._get_ipaddr_for( name )
                title = '{0}{1}'.format(
                    name,
                    ' ({0})'.format( IP ) if IP else ''
                )
                self.println( title )
                self.println( '-' * len(title) )
                # Show any VLANs defined for bond; not sure this is
                # even valid, but anyway...
                vlans = self._get_vlans_for( name )
                for vlan in sorted( vlans ):
                    IP = self._get_ipaddr_for( vlan )
                    self.println( ' |' )
                    self.println( ' +-- {0}'.format(
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
        if not found_any:
            self.println()
            self.println( 'No bridge or bonded interfaces found.' )
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
                    self.iface
                )
            )
            fmt = '{{0:>{0}}}={{1}}'.format( max_name )
            for key in sorted( self.iface ):
                if key.isupper():
                    self.println(
                        fmt.format( key, self.iface[key] )
                    )
        return
