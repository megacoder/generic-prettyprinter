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
		self._prepare()
		return

	def	_prepare( self ):
		self.lines = []
		self.max_name = 15
		self.max_kinds = {}
		return

	def	next_line( self, line ):
		tokens = line.rstrip().split( ':', 1 )
		if len(tokens) == 2:
			self.max_name = max( self.max_name, len( tokens[0] ) )
			args = {}
			for arg in tokens[1].split():
				kind = arg.split( '=', 1 )[0]
				try:
					self.max_kinds[kind] = max( self.max_kinds[kind], len(arg) )
				except:
					self.max_kinds[kind] = len(arg)
				args[kind] = arg
			self.lines.append( (tokens[0], args) )
		return

	def	begin_file( self, fn ):
		super( PrettyPrint, self ).begin_file( fn )
		self._prepare()
		return

	def	_report( self ):
		self.lines.sort( key = lambda (n,a): string.lower(n) )
		kinds = []
		kind_fmts = {}
		for kind in self.max_kinds.keys():
			kinds.append( kind )
			kind_fmts[kind] = '%%-%ds' % self.max_kinds[kind]
		kinds.sort()
		for (name, args) in self.lines:
			options = ''
			keys = args.keys()
			for kind in kinds:
				if kind in keys:
					s = kind_fmts[kind] % args[kind]
				else:
					s = kind_fmts[kind] % ""
				options = options + ' ' + s
			fmt = '%%%ds :%%s' % self.max_name
			print fmt % ( name, options )
		self._prepare()
		return

	def	end_file( self, name ):
		self._report()
		super( PrettyPrint, self ).end_file( fn )
		return

	def	finish( self ):
		if len(self.lines) > 0:
			self._report()
		return
