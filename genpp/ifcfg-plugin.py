#!/usr/bin/python

import  sys
import  superclass

class   PrettyPrint( superclass.MetaPrettyPrinter ):

    NAME = 'ifcfg-pp'
    DESCRIPTION='''Show ifcfg network files in canonical style.'''

    def __init__( self ):
        super( PrettyPrint, self ).__init__()
        self.device    = None
        self.nics      = dict()
        return

    def ignore( self, name ):
        ''' Ignore directory entries not ending with '.conf' '''
        return not name.endswith( '.conf' )

    def pre_begin_file( self, fn ):
        self.nic = dict({
            '_used'  : False,
            '_id'    : None,
            'NAME'   : None,
            'DEVICE' : None,
        })
        return

    def next_line( self, line ):
        parts = map(
            str.strip,
            line.split( '#', 1 )[ 0 ].split( '=', 1 )
        )
        if len( parts ) == 2:
            name  = parts[ 0 ]
            value = parts[ 1 ]
            if value.startswith( '"' ) or value.startswith( "'" ):
                value          = value[1:-1]
            self.nic[name] = value
        return

    def get_nic_id( self, nic ):
        id = nic.get( '_id', None )
        if not id: id = nic.get( 'NAME', None )
        if not id: id = nic.get( 'DEVICE', None )
        if not id: id = 'TBD'
        return id

    def end_file( self, fn ):
        id = self.get_nic_id( self.nic )
        self.nic[ '_id' ] = id
        self.nics[ id ]   = self.nic
        # Leave the 'self.nic' intact so we can display it later in
        # self.report()
        return

    def screen( self, candidates, name, value, same = True ):
        if not candidates:
            candidates = self.nics.keys()
        if same:
            candidates = [
                id for id in candidates if
                    self.nics[id].get( name, '_dunno' ) == value
            ]
        else:
            candidates = [
                id for id in candidates if
                    self.nics[id].get( name, '_dunno' ) != value
            ]
        return candidates

    def set_used( self, id ):
        self.nics[ id ][ '_used' ] = True
        return

    def indent_print( self, s, depth = 0 ):
        self.println(
            '{0}{1}'.format(
                '    ' * depth,
                s,
            )
        )
        return

    def vlans_for( self, id ):
        leadin = '{0}.'.format( id )
        candidates = list()
        for candidate in self.screen( None, '_used', False ):
            device = self.nics[ candidate ][ 'DEVICE' ]
            if device.startswith( leadin ):
                candidates.append( device )
        return candidates

    def _print_a_nic( self, nic, depth = 0 ):
        # Output iface lines, sorted in order
        keys = [
            key for key in self.nic if key[0].isupper()
        ]
        width =  max(
            map(
                len,
                keys
            )
        )
        fmt = '{{0:>{0}}}={{1}}'.format( width )
        for key in sorted( keys ):
            value = self.nic[ key ]
            # delim = "'" if '"' in value else '"'
            delim = '"'
            self.indent_print(
                fmt.format(
                    key,
                    '{0}{1}{0}'.format( delim, value )
                ),
                depth
            )
        return

    def _print_a_bridge( self, bridge, depth = 0 ):
        self.indent_print( bridge, depth )
        for vlan in self.vlans_for( bridge ):
            self.indent_print( vlan, depth + 1 )
            self.set_used( vlan )
        candidates = self.screen( None, '_used', False )
        candidates = self.screen( candidates, 'BRIDGE', bridge )
        ethernets  = self.screen( candidates, 'Type', 'Ethernet' )
        for ethernet in sorted( ethernets ):
            self.indent_print( ethernet, depth + 1 )
            self.set_used( ethernet )
            del candidates[ ethernet ]
        if len(candidates):
            print >>sys.stderr, 'unused bridge components={0}'.format(
                candidates
            )
        return

    def _print_a_bond( self, bond, depth = 0 ):
        self.indent_print( bond, depth )
        for vlan in self.vlans_for( bond ):
            self.indent_print( vlan, depth + 1 )
            self.set_used( vlan )
        candidates = self.screen( None, '_used', False )
        candidates = self.screen( candidates, 'SLAVE', 'yes' )
        candidates = self.screen( candidates, 'MASTER', bond )
        for slave in sorted( candidates ):
            self.indent_print( slave, depth + 1 )
            for vlan in self.vlans_for( slave ):
                self.indent_print( vlan, depth + 2 )
                self.set_used( vlan )
            self.set_used( slave )
        return

    def _final_report( self ):
        self.println()
        title = 'S U M M A R Y'
        self.println( title )
        self.println( '=' * len( title ) )
        # Step 0: The network (tm)
        self.println()
        depth = 0
        self.indent_print( 'network', depth )
        # Step 1: construct bridged interfaces
        bridges = self.screen( None, '_used', False )
        bridges = self.screen( bridges, 'TYPE', 'Bridge' )
        if len(bridges):
            for bridge in sorted( bridges ):
                self.set_used( bridge )
                self._print_a_bridge( bridge, depth + 1 )
        # Step 2: Bonded interfaces
        bonds = self.screen( None, '_used', False )
        bonds = self.screen( bonds, 'TYPE', 'Bond' )
        if len( bonds ):
            for bond in sorted( bonds ):
                self.set_used( bond )
                self._print_a_bond( bond, depth + 1 )
        # Step 3: Plain Ethernets (Infiniband?)
        ethernets = self.screen( None, '_used', False )
        ethernets = self.screen( ethernets, 'TYPE', 'Ethernet' )
        if len(ethernets):
            for nic in ethernets:
                self.set_used( nic )
                if nic != 'lo':
                    self.indent_print(
                        nic,
                        depth + 1
                    )
                    for vlan in self.vlans_for( nic ):
                        self.indent_print( vlan, depth + 2 )
                        self.set_used( vlan )
        # Step 4: Show any left-overs
        unclaimed = self.screen( None, '_used', False )
        unclaimed = self.screen( unclaimed, 'DEVICE', 'lo', False )
        if len(unclaimed):
            for name in sorted( unclaimed ):
                self.set_used( name )
                self.indent_print( name, depth + 1 )
        return

    def report( self, final = False ):
        if final:
            self._final_report()
        else:
            id = self.nic.get( 'NAME', None )
            if not id:
                id = self.nic.get( 'DEVICE', 'DUNNO' )
            self._print_a_nic( id )
        return
