#!/usr/bin/python

import  pprint
import  sys
import  superclass
import  shlex

class   PrettyPrint( superclass.MetaPrettyPrinter ):

    NAME = 'udev'
    DESCRIPTION = """Display /etc/udev/rules.d/ files in canonical style."""

    GLOB = '*.rules'

    def __init__( self ):
        super( PrettyPrint, self ).__init__()
        self.opers = [
            # Put longest matches first
            [ '==', True ],
            [ '+=', False ],
            [ '=',  False ],
        ]
        self.lines  = dict()
        return

    def next_line( self, line ):
        clauses        = dict()
        needs_more     = False
        was_relational = True
        footnotes      = list()
        tokens         = shlex.split( line, comments = True, posix = True )
        for token in tokens:
            name, value = None, None
            for [ oper, is_relop ] in self.opers:
                if token.find( oper, 1 ) > -1:
                    if is_relop and not was_relational:
                        footnotes += [ self.footnote(
                            'Relational op [{0}] follows action'.format(
                                token
                            )
                        ) ]
                    break
            name, value = token.split( oper, 1 )
            if not name and not value: return
            if not name or len( name ) == 0:
                name = '{ANONYMOUS}'
            if not value or len( value ) == 0:
                value = '{EMPTY}'
            if token.endswith( ',' ):
                value = value[:-1]
                needs_more = True
            if name in clauses:
                footnotes += [ self.footnote(
                    'Duplicate {0} clause'.format( name )
                ) ]
            clause = '{0}=="{1}"'.format( name, value )
            clauses[ name ] = clause
        if len(tokens):
            self.lines[ self.get_lineno() ] = line, clauses, footnotes
        return

    def report( self, final = False ):
        if final:
            self.println()
            title = 'R U L E S'
            self.println( title )
            self.println( '-' * len( title ) )
            self.println()
            for lineno in sorted( self.lines, key = lambda n: int(n) ):
                line, clauses, footnotes = self.lines[ lineno ]
                if footnotes and len(footnotes):
                    for footnote in footnotes:
                        self.println(
                            '# See footnote {0}, which follows'.format(
                                footnote
                            )
                        )
                if 'LABEL' in clauses:
                    indent = ''
                else:
                    indent = '\t'
                self.println(
                    '{0}{1}'.format(
                        indent,
                        line
                    )
                )
                if 'GOTO' in clauses and len(clauses) == 1:
                    self.println()
        return
