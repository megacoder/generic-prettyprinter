#!/usr/bin/python

import  pprint
import  sys
import  superclass

class   PrettyPrint( superclass.MetaPrettyPrinter ):

    NAME = 'udev'
    DESCRIPTION = """Display /etc/udev/rules.d/ files in canonical style."""

    GLOB = '-'

    def __init__( self ):
        super( PrettyPrint, self ).__init__()
        return

    def next_line( self, line ):
        octothorpe = line.find( '#' )
        if octothorpe == -1:
            comment = ""
        else:
            comment = line[octothorpe:].rstrip()
            line = line[:octothorpe]
        forbidden = False
        clauses = map(
            str.strip,
            line.split( ',' )
        )
        for clause in clauses:
            if clause.find( '==' ) > -1:
                if forbidden:
                    print '#' * 72
                    print '# ERROR'
                    print '# Predicate "%s" follows definition.' % clause
                    print '#' * 72
            elif clause.find( '=' ) > -1:
                forbidden = True
        self.println(
            '{0}{1}'.format(
                ', '.join( clauses ),
                comment
            )
        )
        return
