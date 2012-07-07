#!/usr/bin/python

import	os
import	sys
import	superclass

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	NAME = 'modprobe-pp'
	DESCRIPTION = """Display /etc/modprobe.* files in canonical style."""

	def	__init__( self ):
		super( PrettyPrint, self ).__init__()
		return

	def	reset( self ):
		self.tokens = []
		self.max_name = 1
		return

	def	process( self, f = sys.stdin ):
		for line in f:
			line = line.strip()
			if line.startswith( '#' ):
				tokens = [ line ]
			else:
				tokens = line.split()
				if len(tokens) >= 2:
					self.max_name = max( self.max_name, len(tokens[1]) )
					self.tokens.append( (
						tokens[0],
						tokens[1],
						' '.join(tokens[2:])
					 ) )
		return

	def	finish( self ):
		fmt = '%%-s %%-%ds %%s' % self.max_name
		for verb,name,rest in self.tokens:
			print fmt % (verb, name, rest)
		return
