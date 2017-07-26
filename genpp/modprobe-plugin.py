#!/usr/bin/python
# vim: noet sw=4 ts=4

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
		super( PrettyPrint, self ).reset()
		self._prepare()
		return

	def	_prepare( self ):
		self.tokens = []
		self.max_name = 1
		return

	def	begin_file( self, name ):
		super( PrettyPrint, self ).begin_file( name )
		self._prepare()
		return

	def	next_line( self, line ):
		octothorpe = line.find( '#' )
		if octothorpe > -1:
			line = line[:octothorpe]
		tokens = line.split()
		if len(tokens) >= 2:
			self.max_name = max( self.max_name, len(tokens[1]) )
			self.tokens.append( (
				tokens[0],
				tokens[1],
				' '.join(tokens[2:])
			 ) )
		return

	def	report( self, final = False ):
		fmt = '%%-9s %%-%ds %%s' % self.max_name
		self.tokens.sort( key = lambda (v,n,o) : (v.lower(),n.lower()) )
		for verb,name,rest in self.tokens:
			self.println( fmt % (verb, name, rest) )
		self.println()
		self._prepare()
		return
