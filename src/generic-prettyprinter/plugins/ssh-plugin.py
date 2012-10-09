#!/usr/bin/python
# vim: noet sw=4 ts=4

import	os
import	sys
import	string
import	superclass

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	NAME = 'ssh'
	DESCRIPTION="""Display /etc/ssh/sshd?_config in conical style."""

	def __init__( self ):
		super( PrettyPrint, self ).__init__()
		return

	def	reset( self ):
		super( PrettyPrint, self ).reset()
		self.prepare()
		return

	def	prepare( self ):
		self.maxname = 0
		self.terms = []
		return

	def	begin_file( self, name ):
		super( PrettyPrint, self ).begin_file( name )
		self.prepare()
		return

	def	end_file( self, name ):
		self._show_content()
		super( PrettyPrint, self ).end_file( name )
		return

	def	next_line( self, line ):
		octothorpe = line.find( '#' )
		if octothorpe > -1:
			line = line[:octothorpe]
		tokens = line.strip().split()
		if len(tokens) == 2:
			name = tokens[0]
			self.maxname = max( self.maxname, len(name) )
			value = tokens[1]
			self.terms.append( tokens )
		return

	def	_show_content( self ):
		if len(self.terms) > 0:
			self.terms.sort( key = lambda (n,v): n.lower() )
			tfmt = '%%-%ds %%s' % self.maxname
			for (name,value) in self.terms:
				print tfmt % (name, value)
		return
