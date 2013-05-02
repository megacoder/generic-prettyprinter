#!/usr/bin/python
# vim: sw=4 ts=4 noet

import	os
import	sys
import	stat
from	superclass	import	MetaPrettyPrinter

class	PrettyPrint( MetaPrettyPrinter ):

	NAME = 'nsswitch-pp'
	DESCRIPTION = """Display /etc/nsswitch.conf configuration files in canonical format."""

	def	__init__( self ):
		super( PrettyPrint, self ).__init__()
		return

	def	reset( self ):
		super( PrettyPrint, self ).reset()
		self._setup()
		return

	def	_setup( self ):
		self.settings = []
		self.max_name = 7
		return

	def	next_file( self, name ):
		super( PrettyPrint, self ).next_file( name )
		self._setup()
		return

	def	end_file( self, name ):
		self.report()
		self._setup()
		super( PrettyPrint, self ).end_file( name )
		return

	def	next_line( self, line ):
		tokens = line.split( '#', 1 )[0].strip().split()
		if len(tokens) == 2:
			name  = tokens[0].strip()
			value = ' '.join( tokens[1].strip().split() )
			self.max_name = max( self.max_name, len(name) )
			self.settings.append( [name, value] )
		return

	def	report( self, final = False ):
		fmt = '%%-%ds %%s' % self.max_name
		for name,value in sorted( self.settings ):
			self.println( fmt % (name, value) )
		return
