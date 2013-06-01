#!/usr/bin/python

import	os
import	sys
import	superclass

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	NAME = 'smp-pp'
	DESCRIPTION = """Display smb.conf files in canonical style."""

	def	__init__( self ):
		super( PrettyPrint, self ).__init__()
		return

	def	reset( self ):
		super( PrettyPrint, self ).reset()
		self._prepare()
		return

	def	_prepare( self ):
		self.name     = None
		self.entries  = []
		self.max_name = None
		self.sections = []
		return

	def	begin_file( self, name ):
		super( PrettyPrint, self ).begin_file( name )
		self._prepare()
		return

	def	end_file( self, name ):
		self._close_section()
		self.report()
		super( PrettyPrint, self ).end_file( name )
		return

	def	_in_section( self ):
		return True if self.name else False

	def	_open_section( self, name ):
		self._close_section()
		self.name     = name
		self.max_name = max( 14, len(name) )
		self.entries  = []
		return

	def	_close_section( self ):
		if self._in_section():
			self.entries.sort(
				key = lambda (n,v) : n.lower()
			)
			self.sections.append( [self.name, self.max_name, self.entries] )
		self.name     = None
		self.max_name = None
		self.entries  = None
		return

	def	next_line( self, line ):
		line = line.split( '#', 1 )[0].split( ';', 1 )[0]
		if line.startswith( '[' ):
			self._close_section()
			self._open_section( line )
		else:
			line = line.strip()
			if len(line) > 0 and self._in_section():
				name,value = line.split( '=', 1 )
				name = name.strip()
				value = value.strip()
				self.max_name = max( self.max_name, len(name) )
				self.entries.append( [name, value] )
		return

	def	report( self, final = False ):
		others = False
		for (name,maxlen,settings) in sorted( self.sections, key =
			lambda (n,m,s) : n.lower() ):
			if others:
				self.println()
			others = True
			self.println( name )
			fmt = '%%-%ds = %%s' % maxlen
			for (n,v) in settings:
				self.println( fmt % (n,v) )
		self._prepare()
		return
