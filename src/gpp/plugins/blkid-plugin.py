#!/usr/bin/python
# vim: noet sw=4 ts=4

import	os
import	sys
import	string
import	superclass

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	NAME = 'blkid-pp'
	DESCRIPTION="""List output of blkid(8) in a canonical form."""

	INDENT_WITH = '        '

	def __init__( self ):
		super( PrettyPrint, self ).__init__()
		return

	def	reset( self ):
		super( PrettyPrint, self ).reset()
		self.lines = []
		self.max_name = 15
		return

	def	next_line( self, line ):
		tokens = line.rstrip().split( ':', 1 )
		if len(tokens) == 2:
			self.max_name = max( self.max_name, len( tokens[0] ) )
			self.lines.append( (tokens[0], tokens[1].split()) )
		return

	def	finish( self ):
		self.lines.sort( key = lambda (n,a): string.lower(n) )
		fmt = '%%%ds : %%s' % self.max_name
		for (name, args) in self.lines:
			args.sort()
			print fmt % ( name, ' '.join(args) )
		return
