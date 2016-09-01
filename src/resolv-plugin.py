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
		self.kinds = dict(
			options    = None,
			sortlist   = None,
			domain     = None,
			search     = None,
			nameserver = None,
		)
		return

	def	pre_begin_file( self, name = None ):
		self.entries = dict()
		return

	def	next_line( self, line ):
		tokens = map(
			str.strip,
			# ';' is an alternate comment indicator, drop comment and
			# tokenize
			line.replace( ';', '#' ).split( '#', 1 )[0].split()
		)
		if len(tokens):
			directive = tokens[0]
			if directive not in self.kinds:
				footnote = self.footnote(
					"Directive '{0}' may be mispelled.".format( directive )
				)
				self.println( '{0}\t### See footnote {1}'.format(
						line,
						footnote
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
					self.entries
				)
			)
			fmt = '{{0:{0}}} {{1}}'.format( widest )
			for kind in self.kinds:
				if kind in self.entries:
					for entry in self.entries[ kind ]:
						self.println(
							fmt.format(
								kind,
								' '.join( entry )
							)
						)
		return
