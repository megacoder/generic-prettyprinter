#!/usr/bin/python
# vim: sw=4 ts=4 noet

import	os
import	sys
import	superclass

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	NAME = 'resolv-pp'
	DESCRIPTION = """Display /etc/resolv.conf files in canonical style."""

	def	__init__( self ):
		super( PrettyPrint, self ).__init__()
		self.kinds = [
			'options',
			'sortlist',
			'domain',
			'search',
			'nameserver',
		]
		return

	def	pre_begin_file( self, name = None ):
		self.entries = {}
		return

	def	next_line( self, line ):
		code = line.replace( ';', '#' ).split( '#', 1 )[0].strip()
		if len(code) > 0:
			tokens = map(
				str.strip,
				code.split()
			)
			directive = tokens[0]
			if directive not in self.kinds:
				n = self.footnote(
					"Directive '{0}' may be mispelled.".format( directive )
				)
				self.println( '{0}\t### Footnote {1}'.format(
						line,
						n
					)
				)
			if directive not in self.entries:
				self.entries[ directive ] = []
			self.entries[ directive ].append( tokens[ 1: ] )
		return

	def	report( self, final = False ):
		if not final:
			widest = max(
				map(
					len,
					self.entries.keys()
				)
			)
			fmt = '{0:%ds} {1}' % widest
			for kind in self.kinds:
				if kind in self.entries.keys():
					for entry in self.entries[ kind ]:
						self.println(
							fmt.format(
								kind,
								' '.join( entry )
							)
						)
		return
