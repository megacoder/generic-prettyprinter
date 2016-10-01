#!/usr/bin/python
# vi: noet sw=4 ts=4
# Print free(1) output in canonical form

import	os
import	sys
import	superclass

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	NAME = 'free-pp'
	DESCRIPTION = """Display free(1) output in canonical style."""
	GLOB = None

	def __init__( self ):
		super( PrettyPrint, self ).__init__()
		return

	def pre_begin_file( self, name = None ):
		self.lines = 0
		self.mem   = {}
		self.swap  = {}
		self.names = []
		return

	def next_line( self, line ):
		tokens = map(
			str.strip,
			line.split( '#', 1 )[0].split()
		)
		if len(tokens):
			self.lines += 1
			if self.lines == 1:
				# Take first line as column headers
				self.names = tokens
			elif tokens[0] == 'Mem:':
				self.mem = dict( zip( self.names, tokens[1:] ) )
			elif tokens[0] == 'Swap:':
				self.swap = dict( zip( self.names, tokens[1:] ) )
		return

	def _show_dict( self, d, title = None ):
		if title:
			self.println()
			self.println( title )
			self.println( '=' * len(title) )
			self.println()
		width = max(
			map(
				len,
				self.names
			)
		)
		fmt = '\t{{0:{0}}} {{1:>9}}'.format( width )
		for key in sorted( d ):
			self.println( fmt.format( key, d[ key ] ) )
		return

	def report( self, final = False ):
		if not final:
			self._show_dict( self.mem,		'Memory'	)
			try:
				pressure = int(
					(
						(
							float( self.mem['free'] )		+
							float( self.mem['buff/cache'] )
						) / float( self.mem['total'] )
					) * 100.0 + 0.5
				)
				self.println()
				self.println(
					'\tMemory pressure is {0}%.'.format( pressure )
				)
				self.footnote( '\tMemory pressure = (free+buffers_cache)/total' )
			except Exception, e:
				self.println(
					'Memory pressure calculation failed.'
				)
				self.println( e )
			self._show_dict( self.swap,		'Swap'		)
		return
