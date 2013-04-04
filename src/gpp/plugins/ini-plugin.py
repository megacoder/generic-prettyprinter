#!/usr/bin/python

import	os
import	sys
import	superclass

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	NAME = 'ini-pp'
	DESCRIPTION = """Display [ini] files in canonical style."""

	def	__init__( self ):
		super( PrettyPrint, self ).__init__()
		return

	def	reset( self ):
		super( PrettyPrint, self ).reset()
		self._prepare()
		return

	def	_prepare( self ):
		self.name     = None
		self.sections = []
		return

	def	begin_file( self, name ):
		super( PrettyPrint, self ).begin_file( name )
		self._prepare()
		return

	def	_in_section( self ):
		return True if self.name else False

	def	_open_section( self, name ):
		if self._in_section():
			self._close_section()
		self.name     = name
		self.max_name = 14
		self.entries  = []
		return

	def	_close_section( self ):
		if self.name:
			self.entries.sort(
				key = lambda (n,v) : n.lower()
			)
			self.sections.append( [self.name, self.max_name, self.entries] )
		self.name    = None
		return

	def	next_line( self, line ):
		octothorpe = line.find( '#' )
		if octothorpe > -1:
			line = line[:octothorpe]
		if line.startswith( '[' ):
			self._close_section()
			self._open_section( line.strip() )
		else:
			line = line.strip()
			if len(line) > 0:
				if self._in_section():
					name,value = line.split( '=', 1 )
					self.max_name = max( self.max_name, len(name) )
					self.entries.append( [name, value] )
		return

	def	report( self, final = False ):
		self.sections.sort(
			key = lambda (n,m,s) : n.lower()
		)
		others = False
		for (name,maxlen,settings) in self.sections:
			if others:
				print
			others = True
			print name
			fmt = '%%-%ds = %%s' % maxlen
			for (n,v) in settings:
				print fmt % (n,v)
		self._prepare()
		return
