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
        self.max_width = 7
        return

    def ignore( self, name ):
        ''' Ignore directory entries not ending with '.conf' '''
        return not name.endswith( '.conf' )

    def pre_begin_file( self, fn ):
        self.nic = dict({ '_used' : False })
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

    def end_file( self, fn ):
        if 'NAME' in self.nic:
            name = self.nic[ 'NAME' ]
        elif 'DEVICE' in self.nic:
            name = self.nic[ 'DEVICE' ]
        else:
            name = 'ANONYMOUS'
        self.nic[ 'NAME' ]  = name
        self.nics[ name ]   = self.nic
        # Leave the 'self.nic' intact so we can display it later in
        # self.report()
        return

    def screen( self, candidates, name, value ):
        candidates = [
            key for key in candidates if
                self.nics[key].get( name, '_dunno' ) == value
        ]
        return candidates

    def set_used( self, key ):
        self.nics[ key ][ '_used' ] = True
        return

    def _final_report( self ):
        self.println()
        title = 'S U M M A R Y'
        self.println( title )
        self.println( '=' * len( title ) )
        # Pass 1: construct bridged interfaces
        bridges = self.screen( self.nics.keys(), '_used', False )
        bridges = self.screen( bridges, 'TYPE', 'Bridge' )
        if len(bridges):
            self.println()
            title = 'Bridges'
            self.println( title )
            self.println( '-' * len( title ) )
            for name in sorted( bridges ):
                if 'DEVICE' in self.nics[ name ]:
                    iface = self.nics[ name ]['DEVICE']
                else:
                    iface = name
                self.println( iface )
                self.set_used( name )
        bonds = self.screen( self.nics.keys(), '_used', False )
        bonds = self.screen( bonds, 'TYPE', 'Bond' )
        if len( bonds ):
            self.println()
            title = 'Bonded'
            self.println( title )
            self.println( '-' * len( title ) )
            for name in sorted( bonds ):
                if 'DEVICE' in self.nics[ name ]:
                    iface = self.nics[ name ][ 'DEVICE' ]
                else:
                    iface = name
                self.println( iface )
                self.set_used( name )
        ethernets = self.screen( self.nics.keys(), '_used', False )
        ethernets = self.screen( ethernets, 'TYPE', 'Ethernet' )
        if len(ethernets):
            self.println()
            title = 'Ethernet'
            self.println( title )
            self.println( '-' * len(title) )
            for name in ethernets:
                if 'DEVICE' in self.nics[ name ]:
                    iface = self.nics[ name ][ 'DEVICE' ]
                else:
                    iface = name
                self.println( iface )
                self.set_used( name )
        unclaimed = self.screen( self.nics.keys(), '_used', False )
        if len(unclaimed):
            self.println()
            title = 'Unprocessed NICs'
            self.println( title )
            self.println( '-' * len( title ) )
            for name in sorted( unclaimed ):
                self.println( name )
                self.set_used( name )
        return

    def _nic_report( self ):
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
            self.println(
                fmt.format(
                    key,
                    '{0}{1}{0}'.format( delim, value )
                )
            )
        return

    def report( self, final = False ):
        if final:
            self._final_report()
        else:
            self._nic_report()
        return
