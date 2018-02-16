#!/usr/bin/python

import  sys
import  superclass

class   PrettyPrint( superclass.MetaPrettyPrinter ):

    NAME = 'ifcfg-pp'
    DESCRIPTION='''Show ifcfg network files in canonical style.'''

    def __init__( self ):
        super( PrettyPrint, self ).__init__()
        self.options = dict()
        self.config  = dict()
        return

    def ignore( self, name ):
        ''' Ignore directory entries not ending with '.conf' '''
        return not name.endswith( '.conf' )

    def next_line( self, line ):
        parts = map(
            str.strip,
            line.split( '#', 1 )[ 0 ].split()
        )
        n = len( parts )
        if n == 2:
            option                 = parts[ 0 ]
            value                  = parts[ 1 ]
            self.options[ option ] = value
        elif n == 3:
            setting                = parts[ 0 ]
            service                = parts[ 1 ]
            value                  = parts[ 2 ]
            config                 = self.config.get( service, dict() )
            config[ setting ]      = value
            self.config[ service ] = config
        else:
            pass
        return

    def report_options( self ):
        self.subtitle( 'Settings' )
        option_len = max(
            map(
                len,
                self.options if len(self.options) else [ 'oops' ]
            )
        )
        fmt = '{{0:<{0}.{0}s}}  {{1}}'.format(
            option_len
        )
        self.println()
        for option in sorted( self.options ):
            self.println(
                fmt.format( option, self.options[ option ] )
            )
        return

    def report_services( self ):
        self.subtitle( 'Service Configuration' )
        #
        setting_width = 7
        for service in self.config:
            config = self.config[ service ]
            setting_width = max(
                setting_width,
                max(
                    map(
                        len,
                        config
                    )
                )
            )
        #
        service_width = max(
            map(
                len,
                self.config
            )
        )
        #
        fmt = '{{0:<{0}}} {{1:{1}}} {{2}}'.format(
            setting_width,
            service_width
        )
        #
        for service in sorted( self.config ):
            self.println()
            config = self.config[ service ]
            for setting in sorted( config ):
                self.println(
                    fmt.format(
                        setting,
                        service,
                        config[ setting ]
                    )
                )
        return

    def report( self, final = False ):
        if final: return
        self.title( 'nscd(8) Caching Daemon Setup' )
        self.report_options()
        self.report_services()
        return
