#!/usr/bin/python

import	os
import	sys
import	superclass

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	NAME = 'kdump'
	DESCRIPTION = """Display /etc/kdump.* files in canonical style."""

	def	__init__( self ):
		super( PrettyPrint, self ).__init__()
		return

	def	reset( self ):
		super( PrettyPrint, self ).reset()
		self.tokens = []
		self.max_name = 1
		return

	def	next_line( self, line ):
		octothorpe = line.find( '#' )
		if octothorpe > -1:
			line = line[:octothorpe]
		tokens = line.split()
		if len(tokens) > 0:
			name = tokens[0]
			if len(tokens) == 1:
				value = []
			else:
				value = tokens[1:]
			self.max_name = max( self.max_name, len(name) )
			self.tokens.append( ( name, ' '.join(value) ) )
		return

	def	finish( self ):
		fmt = '%%%ds %%s' % self.max_name
		self.tokens.sort( key = lambda (n,v) : n.lower() )
		for name,value in self.tokens:
			print fmt % (name, value)
		return
