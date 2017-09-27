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
            _seen = False
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
        if 'BONDING_OPTS' in iface and 'TYPE' not in iface:
            iface[ 'TYPE' ] = 'Bond'
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
        self.iface        = self._normalize( self.iface )
        name              = self.iface['NAME']
        self.ifcfgs[name] = self.iface
        super( PrettyPrint, self ).post_end_file()
        return

    def get_seen( self, iface ):
        return iface.get( '_seen', False )

    def set_seen( self, iface, value = True ):
        iface['_seen'] = value
        return

    def _iface_is_vlan( self, iface ):
        return '.' in iface['NAME']

    def _iface_is_alias( self, iface ):
        return ':' in iface['NAME']

    def _filter_bridge_unclaimed( self, iface ):
        accept  = not self.get_seen( iface )
        accept &= (iface['TYPE'] == 'Bridge')
        accept &= not self._iface_is_vlan( iface )
        accept &= not self._iface_is_alias( iface )
        return accept

    def _filter_any_unclaimed( self, iface ):
        accept = not self.get_seen( iface )
        return accept

    def _filter_ethernet_unclaimed( self, iface ):
        accept = not self.get_seen( iface )
        accept &= (iface['TYPE'] == 'Ethernet')
        return accept

    def find_all( self, filter = lambda iface: True ):
        names = [
            name for name in self.ifcfgs if filter( self.ifcfgs[name] )
        ]
        if len(names) == 0:
            names = None
        return names

    def _indent_print( self, s, indents = [] ):
        self.println(
            '{0}{1}'.format(
                ''.join( indents ),
                s
            )
        )
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
                iface = self.ifcfgs[ name ]
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
                self.set_seen( self.ifcfgs[name] )
        resid = self.find_all( self._filter_any_unclaimed )
        if resid:
            self.println()
            title = 'Unprocessed NICs'
            self.println( title )
            self.println( '-' * len( title ) )
            for name in sorted( resid ):
                self.println( name )
                self.set_seen( self.ifcfgs[name] )
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
