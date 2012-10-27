#!/usr/bin/python
# vim: noet sw=4 ts=4

import	os
import	string
import	superclass
import	sys

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
		self.max_kinds = {}
		return

	def	next_line( self, line ):
		tokens = line.rstrip().split( ':', 1 )
		if len(tokens) == 2:
			self.max_name = max( self.max_name, len( tokens[0] ) )
			args = tokens[1].split()
			args.sort()
			for arg in args:
				kind = arg.split( '=', 1 )[0]
				try:
					self.max_kinds[kind] = max( self.max_kinds[kind], len(arg) )
				except:
					self.max_kinds[kind] = len(arg)
			self.lines.append( (tokens[0], args) )
		return

	def	finish( self ):
		self.lines.sort( key = lambda (n,a): string.lower(n) )
		kind_fmts = {}
		for (name, args) in self.lines:
			for arg in args:
				kind = arg.split('=',1)[0]
				kind_fmts[kind] = '%%-%ds' % self.max_kinds[kind]
		for (name, args) in self.lines:
			args.sort()
			options = ''
			for arg in args:
				kind = arg.split( '=', 1 )[0]
				options = options + ' ' + (kind_fmts[kind] % arg)
			fmt = '%%%ds :%%s' % self.max_name
			print fmt % ( name, options )
		return
