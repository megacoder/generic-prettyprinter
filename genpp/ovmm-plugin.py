#!/usr/bin/python
# vim: noet sw=4 ts=4

import	os
import	sys
import	string
import	superclass
import	re

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	NAME = 'ovmm'
	DESCRIPTION="""Display /etc/sysconfig/ovmm in conical style."""

	def __init__( self ):
		super( PrettyPrint, self ).__init__()
		return

	def	pre_begin_file( self, name = None ):
		self.pairs  = dict()
		return

	def	next_line( self, line ):
		tokens = map(
			str.strip,
			# Drop comments, split assignment
			line.split( '#', 1 )[0].split( '=', 1 )
		)
		if len( tokens ) == 2:
			key       = tokens[0]
			value     = tokens[1]
			footnotes = list()
			if key in self.pairs:
				n = self.footnote(
					'Duplicate item as {0}={1}'.format(
						key,
						self.pairs[key]
					)
				)
				footnotes.append( n )
			# Figure out how to quote the value
			if len(value):
				c = value[0]
				if c in [ '"', "'" ] and c == value[-1]:
					value = value[1:-1]
				value = '{0}{1}{0}'.format(
					'"' if '"' not in value else "'",
					value
				)
			# Convert footnotes to a comma-separated list
			if len(footnotes):
				footnotes = ', '.join( footnotes )
			else:
				footnotes = ''
			# Record the results
			self.pairs[ key ] = dict({
				'key'       : key,
				'value'     : value,
				'footnotes' : footnotes,
			})
		return

	def	report( self, final = False ):
		if not final:
			width = max(
				map(
					len,
					self.pairs
				)
			)
			fmt = '{{0:{0}}} = {{1}}  {{2}}'.format( width )
			for key in sorted(
				self.pairs
			):
				info = self.pairs[ key ]
				self.println(
					fmt.format(
						info['key'],
						info['value'],
						info['footnotes']
					)
				)
		return
