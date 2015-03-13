#!/usr/bin/python
# vim: noet sw=4 ts=4

import	sys

from	superclass	import	MetaPrettyPrinter

class	PrettyPrint( MetaPrettyPrinter ):

	NAME = 'showexport'
	DESCRIPTION = """Display 'showmount -e <name>'  output in canonical style."""

	def __init__( self ):
		super( PrettyPrint, self ).__init__()
		self.pre_begin_file()
		return

	def pre_begin_file( self ):
		self.shares   = dict()
		self.overlaps = dict()
		return

	def next_line( self, line ):
		tokens = map(
			str.strip,
			line.split()
		)
		if len(tokens) >= 2:
			share              = tokens[0]
			clients            = sorted( tokens[1:] )
			self.shares[share] = clients
		return

	def report( self, final = False ):
		if not final:
			width = max(
				map(
					len,
					self.shares.keys()
				)
			)
			fmt = '{0:<%ds}  {1}' % width
			for share in sorted( self.shares.keys() ):
				self.println(
					fmt.format(
						share,
						'  '.join( self.shares[ share ] )
					)
				)
				subdir = share + '/'
				for key in self.shares.keys():
					if key.startswith( subdir ):
						if share in self.overlaps:
							self.overlaps[ share ].append( key )
						else:
							self.overlaps[ share ] = [ key ]
			if len( self.overlaps ) > 0:
				self.println()
				self.println( '*** Found Overlapping Shares ***' )
				self.println()
				for share in sorted( self.overlaps.keys() ):
					self.println( share )
					for key in sorted( self.overlaps[ share ] ):
						self.println( ' |' )
						self.println( ' +- {0}'.format( key ) )
		return
