#!/usr/bin/python
# Print /etf/fstab getting the fields as close to their intended columns as may
# be.  Long fields push the remainder of the line over as little as is possible
# so that the columns come nearer to alignment.

import	os
import	sys
import  superclass

class   PrettyPrint( superclass.MetaPrettyPrinter ):

    NAME = 'export'
    DESCRIPTION = """Display /etc/export files in canonical style."""

    def __init__( self ):
        super( PrettyPrint, self ).__init__()
        self.max_share = 7
        self.max_spec  = 15
        self.content   = []
        return

    def process( self, f = sys.stdin ):
        for line in f:
            line = line.strip()
            if not line.startswith( '#' ):
                tokens = line.rstrip().split()
                # Format is
                #   <name> <host>(<param>[,...]) ...
                # Reformat only regular, or bind-mount, lines
                share = tokens[0]
                self.max_share = max( self.max_share, len(share) )
                roster = []
                for token in tokens[1:]:
                    self.max_spec = max( self.max_spec, len(token) )
                    lparen = token.find( '(' )
                    if lparen > -1:
                        host = token[:lparen]
                        list = token[lparen+1:-1]
                        params = list.split( ',' )
                        params.sort()
                        list = ','.join( params )
                        roster.append( (host, list) )
                roster.sort( key = lambda (h,l): h.lower() )
                self.content.append( (share, roster) )
        return

    def finish( self ):
        self.content.sort()
        for share,specs in self.content:
            print '%-23s\t%s' % (
                share,
                '(' + ('),('.join(specs)) + ')'
            )
        return
