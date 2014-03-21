#!/usr/bin/python
# vi: noet sw=4 ts=4

import	os
import	sys
import	superclass

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	NAME = 'smb-pp'
	DESCRIPTION = """Display smb.conf files in canonical style."""

	def	__init__( self ):
		super( PrettyPrint, self ).__init__()
		self.reset()
		return

	def	reset( self ):
		super( PrettyPrint, self ).reset()
		self.section  = None
		self.maxname  = 14
		self.sections = []
		return

	def	_open_section( self, name ):
		self.section = {
			'name'    :	name,
			'maxname' : 14,
			'entries' : []
		}
		return

	def	_close_section( self ):
		if self.section:
			self.section['entries'].sort(
				key = lambda n,v : n.lower()
			)
			self.sections.append( self.section )
			self.section = None
		return

	def	next_file( self, name ):
		super( PrettyPrint, self ).next_file( name )
		self._prepare()
		return

	def	next_line( self, line ):
		line = line.split( '#', 1 )[0].rstrip()
		line = line.split( ';', 1 )[0].rstrip()
		if line.startswith( '[' ):
			self._close_section()
			self._open_section( line )
		elif self.section:
			line = line.strip()
			if len(line) > 0:
				if line.find( '=' ) > -1:
					name,value = line.split( '=', 1 )
					name       = name.strip()
					value      = value.strip()
				else:
					name  = line
					value = None
				self.max_name = max( self.max_name, len(name) )
				self.entries.append( [name, value] )
		return

	def	report( self, final = False ):
		if self.sections != []:
			others = False
			for section in sorted(
				self.sections,
				key = lambda s : s['name'].lower()
			):
				if others:
					self.println()
				others = True
				self.println( section['name'] )
				fmt = '  %%%ds = %%s' % section['maxname']
				for name,value in sorted(
					section['entries'],
					key = lambda n,v: n.lower()
				):
					self.println( fmt % (name, value) )
		return
