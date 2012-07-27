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
        self.max_clause = 14
        return

    def process( self, f = sys.stdin ):
        for line in f:
            octothorpe = line.find( '#' )
            if octothorpe == -1:
                comment = None
            else:
                comment = line[octothorpe+1:].rstrip()
                line = line[:octothorpe]
            forbidden = False
            clauses = line.rstrip().split( ',' )
            for clause in clauses:
                self.max_clause = max( self.max_clause, len(clause) )
                if clause.find( '==' ) > -1:
                    if forbidden:
                        print >>sys.stderr, 'Predicate "%s" follows definition.' % clause
                elif clause.find( '=' ) > -1:
                    forbidden = True
            fmt = '%%-%d.%ds' % (self.max_clause, self.max_clause)
            for i in xrange(0,len(clauses)):
                clause[i] = fmt % clause[i]
            print ', '.join(clauses)
        return
