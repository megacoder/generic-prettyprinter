#!/usr/bin/python
# vim: sw=4 ts=4 noet

import	os
import	sys
import	stat
from	superclass	import	MetaPrettyPrinter

class	PrettyPrint( MetaPrettyPrinter ):

	NAME = 'ocfs2-pp'
	DESCRIPTION = """Display Oracle OCFS2 configuration files in canonical
	format."""

	def	__init__( self ):
		super( PrettyPrint, self ).__init__()
		return

	def	reset( self ):
		self._new_stanza()
		return

	def	_new_stanza( self ):
		self.content = []
		self.longest = 15
		return

	def	_dump_stanza( self ):
		fmt = ' %%%ds = %%s' % self.longest
		self.content.sort( key = lambda (n,v): n.upper() )
		for (name,value) in self.content:
			print fmt % (name, value)
		self._new_stanza()
		return

	def	_out_header( self, line ):
		self._dump_stanza()
		print line
		return

	def process( self, f = sys.stdin ):
		self._new_stanza()
		for line in f:
			if line[0].isspace() is not True:
				self._out_header( line.rstrip() )
			else:
				parts = line.strip().split( '=', 1 )
				if len(parts) < 2:
					self._out_header( line.rstrip() )
					continue
				name = parts[0].strip()
				value = parts[1].strip()
				self.longest = max( self.longest, len(name) )
				self.content.append( (name,value) )
		self._dump_stanza()
		return
