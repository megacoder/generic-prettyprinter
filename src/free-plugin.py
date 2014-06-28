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
		self.reset()
		return

	def reset( self ):
		super( PrettyPrint, self ).reset()
		self._prepare()
		return

	def _prepare( self ):
		self.lines = 0
		self.mem   = {}
		self.cache = {}
		self.swap  = {}
		return

	def begin_file( self, name ):
		super( PrettyPrint, self ).begin_file( name )
		self._prepare()
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

	def print_dict( self, d, title = None ):
		if title:
			self.println()
			self.println( title )
			self.println( '=' * len(title) )
		width = max( map( len, self.names ) )
		fmt = '\t%%-%ds %%s' % width
		for key in sorted( d.keys() ):
			self.println( fmt % ( key, d[key] ) )
		return

	def report( self, final = False ):
		try:
			pressure = int(
				(
					(
					float( self.mem['free'] )	+
					float( self.mem['buffers'] )	+
					float( self.mem['cached'] )
					) / float( self.mem['total'] )
				) * 100.0
			)
		except Exception, e:
			self.println( 'Memory pressure calculation failed.' )
			self.println( e )
			pressure = 0
		label = '[MemPress%]'
		self.names.append( label )
		self.mem[ label ] = pressure
		self.print_dict( self.mem,		'Memory'	)
		self.println()
		self.println( '\tMemory pressure = (free+buffers+cached)/total' )
		self.print_dict( self.cache,	'Cache'		)
		self.print_dict( self.swap,		'Swap'		)
		return

	def end_file( self, name ):
		self._prepare()
		super( PrettyPrint, self ).end_file( name )
		return
