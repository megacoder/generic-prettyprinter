#!/usr/bin/python

import  pprint
import  sys
import  superclass

class   PrettyPrint( superclass.MetaPrettyPrinter ):

    NAME = 'udev'
    DESCRIPTION = """Display /etc/udev/rules.d/ files in canonical style."""

    def __init__( self ):
        super( PrettyPrint, self ).__init__()
        return

    def reset( self ):
        super( PrettyPrint, self ).reset()
        return

    def process( self, f = sys.stdin ):
        for line in f:
            octothorpe = line.find( '#' )
            if octothorpe == -1:
                comment = ""
            else:
                comment = line[octothorpe:].rstrip()
                line = line[:octothorpe]
            forbidden = False
            clauses = line.split( ',' )
            for i in xrange(0,len(clauses)):
                clauses[i] = clauses[i].strip()
            for clause in clauses:
                if clause.find( '==' ) > -1:
                    if forbidden:
                        print '#' * 72
                        print '# ERROR'
                        print '# Predicate "%s" follows definition.' % clause
                        print '#' * 72
                elif clause.find( '=' ) > -1:
                    forbidden = True
            print '%s%s' % (', '.join(clauses), comment)
        return
