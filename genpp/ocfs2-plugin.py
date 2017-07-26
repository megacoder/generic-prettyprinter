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
		super( PrettyPrint, self ).reset()
		self._reset_stanza()
		self.stanzas = []
		return

	def	_reset_stanza( self ):
		self.name     = None
		self.maxfield = 15
		self.content  = []
		return

	def	_new_stanza( self, name ):
		self._reset_stanza()
		self.name   = name
		self.number = -1
		return

	def	_end_stanza( self ):
		if self.name:
			self.content.sort( key = lambda (f,v) : f.lower() )
			self.stanzas.append( (self.name, self.number, self.maxfield, self.content) )
		self._reset_stanza()
		return

	def	_add_def( self, field, value ):
		self.maxfield = max( self.maxfield, len(field) )
		if field.lower() == 'number':
			self.number = value
		self.content.append( (field, value) )
		return

	def	next_file( self, name ):
		super( PrettyPrint, self ).next_file( name )
		return

	def	end_file( self, name ):
		self._end_stanza()
		self.stanzas.sort( key = lambda (t,n,m,c) : '%s\1%s' % (
				t.lower(),
				n
			)
		)
		others = None
		for (title, number, maxfield, content) in self.stanzas:
			if others:
				print
			others = True
			print '%s:' % title
			if len(content) > 0:
				print
			fmt = '%%%ds = %%s' % maxfield
			for (field, value) in content:
				print fmt % (field, value)
		self.content = []
		super( PrettyPrint, self ).end_file( name )
		return

	def	next_line( self, line ):
		line = line.split( '#', 1 )[0].strip()
		if line.endswith( ':' ):
			self._end_stanza()
			self._new_stanza( line[:-1] )
		else:
			tokens = line.split( '=', 1 )
			if len(tokens) == 2:
				self._add_def( tokens[0].strip(), tokens[1].strip() )
		return
