#!/usr/bin/python
# vim: noet ai sm ts=4 sw=4

import	os
import	sys
import	superclass
import	shlex

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	NAME = 'csv-pp'
	DESCRIPTION = '''
		Display comma-separated-value files in canonical style.
	'''

	def	__init__( self ):
		super( PrettyPrint, self ).__init__()
		return

	def	pre_begin_file( self, name = None ):
		super( PrettyPrint, self ).pre_begin_file( name )
		self.lines  = []
		self.widths = dict()
		return

	def	next_line( self, line ):
		fields = [
			f for f in shlex.shlex( line, posix = True ) if f != ','
		]
		for i in range( len( fields ) ):
			self.widths[ i ] = max(
				self.widths.get( i, 0 ),
				len( fields[i] )
			)
		self.lines.append( fields )
		return

	def	report( self, final = False ):
		if not final:
			gutter = '  '
			fmts = map(
				'{{0:{0}}}'.format,
				[ self.widths[w] for w in self.widths ]
			)
			for line in self.lines:
				columns = map(
					lambda i : fmts[i].format( line[i] ),
					range( len(line) )
				)
				self.println( gutter.join( columns ) )
			self.lines = []
		return
