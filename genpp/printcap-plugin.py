#!/usr/bin/python

import	os
import	sys
import	superclass

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	NAME = 'printcap-pp'
	DESCRIPTION="""Display RHEL-4 printcap files in a readable style."""

	GLOB = '-'

	def	__init__( self ):
	    super( PrettyPrint, self ).__init__()
	    return

	def	start( self ):
	    self.lines  = []
	    self.widths = []
	    return

	def begin_file( self, name ):
	    # Avoid printing per-file headers
	    return

	def next_line( self, line ):
	    tokens = [
		s for s in map(
		    str.strip,
		    line.split( '#', 1 )[0].split( ':' )
		) if len(s) != 0
	    ]
	    N = len( tokens )
	    if N > 0:
		names = ' | '.join( [
			s for s in map(
			    str.strip,
			    tokens[0].split('|')
			) if len(s) > 0
		] )
		attrs       = tokens[1:]
		attrs.sort()
		tokens      = [ names ] + attrs
		self.lines.append( tokens )
		widths      = map( len, tokens )
		padding     = [1] * (N - len( self.widths ))
		self.widths = map(
		    max,
		    zip( self.widths + padding, widths )
		) + self.widths[N:]
		# print 'N={0}, widths={1}'.format( N, widths )
		# print '  self.widths={0}'.format( self.widths )
	    return

	def report( self, final = False ):
	    if final:
		fmts = map(
		    '{{0:{0}.{0}}}'.format,
		    self.widths
		)
		for tokens in sorted( self.lines ):
		    N = len( tokens )
		    self.println( ' : '.join(
			fmts[i].format( tokens[i] ) for i in range( N )
		    ) )
	    return

if __name__ == '__main__':
	pcp = PrettyPrint()
	pcp.process()
	pcp.finish()
