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

	def pre_begin_file( self ):
		self.lines = 0
		self.mem   = {}
		self.cache = {}
		self.swap  = {}
		self.names = []
		return

	def next_line( self, line ):
		self.lines += 1
		tokens = line.split( '#', 1 )[0].strip().split()
		if self.lines == 1:
			self.names = tokens
		elif line.startswith( 'Mem:' ):
			self.mem = dict( zip( self.names, tokens[1:] ) )
		elif line.startswith( '-/+ buffers/cache:' ):
			self.cache = dict( zip( self.names[1:], tokens[2:] ) )
		elif line.startswith( 'Swap:' ):
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
		fmt = '\t{0:%d} {1}' % width
		for key in sorted( d ):
			self.println( fmt.format( key, d[ key ] ) )
		return

	def report( self, final = False ):
		if not final:
			footnote = None
			try:
				pressure = int(
					(
						(
							float( self.mem['free'] )		+
							float( self.mem['buffers'] )	+
							float( self.mem['cached'] )
						) / float( self.mem['total'] )
					) * 100.0
				)
			except Exception, e:
				footnote = self.footnote(
					'Memory pressure calculation failed.'
				)
				self.println( e )
				pressure = 0
			label = '[MemPress%]'
			self.names.append( label )
			self.mem[ label ] = pressure
			self._show_dict( self.mem,		'Memory'	)
			self.println()
			self.println( '\tMemory pressure = (free+buffers+cached)/total' )
			self._show_dict( self.cache,	'Cache'		)
			self._show_dict( self.swap,		'Swap'		)
		return
