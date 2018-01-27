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

    def begin_file( self, fn ):
        self.nic = dict()
        return

    def next_line( self, line ):
        parts = map(
            str.strip,
            line.split( '#', 1 )[ 0 ].split( '=', 1 )
        )
        if len( parts ) == 2:
            name = parts[ 0 ]
            value = parts[ 1 ]
            if value.startswith( '"' ) or value.startswith( "'" ):
                value          = value[1:-1]
                self.nic[name] = value
            self.max_width = max(
                self.max_width,
                len( name )
            )
        return

    def end_file( self, fn ):
        name                 = self.nic.get( 'DEVICE', 'ANONYMOUS' )
        self.nic[ 'DEVICE' ] = name
        self.nic[ '_used' ]  = False
        self.nics[ name ]    = self.nic
        super( PrettyPrint, self ).post_end_file( name )
        return

    def find_nics( self, type = 'Ethernet', BACKLINK = None, MATCH = None ):
        candidates = [
            self.nics[key] for key in self.nics if 'TYPE' in self.nics[
                key
            ] and self.nics[ key ][ 'TYPE' ] == type and not self.nics[
                key
            ][ '_seen' ]
        ]
        if BACKLINK:
            candidates = [
                candidates[ key ] for key in candidates if BACKLINK in
                candidates[ key ] and candidates[ key ][ BACKLINK ] == MATCH
            ]
        return candidates

    def report( self, final = False ):
        if not final:
            return
        title = 'Network Interface Cards'
        self.println()
        self.println( title )
        self.println( '=' * len( title ) )
        fmr = '{{0:>{0}}} = {{1}}'.format( width )
        for nic in sorted( self.nics, key = lambda n : n['DEVICE'].lower() ):
            self.println()
            for name in sorted( nic.keys() ):
                vaule = nic[ name ]
                if value.isdigit():
                    delim = ''
                else:
                    delim = "'" if value.find( "'" ) == -1 else '"'
                self.println(
                    fmt.format(
                        name,
                        '{0}{1}{0}'.format(
                            delim,
                            vaule
                        )
                    )
                )
        if False:
            title = 'Network Topology'
            self.println()
            self.println( title )
            self.println( '=' * len( title ) )
            network = Node( 'network' )
            for type in [ 'Bridge', 'Bond', 'Ethernet' ]:
                topnodes = self.find_nics( self, type = 'Ethernet', BACKLINK = None, MATCH = None )
        return

    def _final_report( self ):
        self.println()
        title = 'S U M M A R Y'
        self.println( title )
        self.println( '=' * len( title ) )
        # Pass 1: construct bridged interfaces
        indents = []
        bridges = self.find_all(
            self._filter_bridge_unclaimed
        )
        if bridges:
            self.println()
            title = 'Bridges'
            self.println( title )
            self.println( '-' * len( title ) )
            last = len( indents ) - 1
            for i,name in enumerate( sorted( bridges ) ):
                iface = self.dev2ifcfg[ name ]
                self._indent_print( iface['NAME'], indents )
                self.set_seen( iface )
        ethernets = self.find_all(
            self._filter_ethernet_unclaimed
        )
        if ethernets:
            self.println()
            title = 'Ethernet'
            self.println( title )
            self.println( '-' * len(title) )
            indents = []
            for name in ethernets:
                self._indent_print( name, indents )
                self.set_seen( self.dev2ifcfg[name] )
        resid = self.find_all( self._filter_any_unclaimed )
        if resid:
            self.println()
            title = 'Unprocessed NICs'
            self.println( title )
            self.println( '-' * len( title ) )
            for name in sorted( resid ):
                self.println( name )
                self.set_seen( self.dev2ifcfg[name] )
        return

    def _nic_report( self ):
        # Dump any accumulated prolog
        if len(self.prolog) > 0:
            for line in self.prolog:
                self.println( line )
            self.println()
        # Output iface lines, sorted in order
        names = [
            name for name in self.iface if name[0].isupper()
        ]
        max_name =  max(
            map(
                len,
                names
            )
        )
        fmt = '  {{0:>{0}}}={{1}}'.format( max_name )
        for key in sorted( names ):
            value = self.iface[ key ]
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
