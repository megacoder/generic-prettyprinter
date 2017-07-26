#!/usr/bin/python
# vim: noet sw=4 ts=4

import	sys

from	superclass	import	MetaPrettyPrinter

class	PrettyPrint( MetaPrettyPrinter ):

	NAME = 'sssd'
	DESCRIPTION = """Display sssd.conf files in canonical style."""

	def __init__( self ):
		super( PrettyPrint, self ).__init__()
		self.pre_begin_file()
		return

	def pre_begin_file( self ):
		self.filename = None
		self.stanzas  = []
		self.stanza   = dict()
		self.name	  = None		# Name of active stanza
		return

	def begin_file( self, name ):
		super( PrettyPrint, self ).begin_file( name )
		self.filename = name
		return

	def	_start_stanza( self, name ):
		if self._in_stanza():
			self._end_stanza()
		self.name = name
		self.stanza = dict()
		return

	def	_add_entry( self, name, value ):
		if name in self.stanza.keys():
			self.error( 'item "{0}" set multiple times'.format( name ) )
		self.stanza[name] = value
		return

	def	_end_stanza( self ):
		if self._in_stanza():
			self.stanzas.append(
				[ self.name, self.stanza ]
			)
		self.name	= None
		self.stanza = None
		return

	def	_in_stanza( self ):
		return True if self.name else False

	def next_line( self, line ):
		if line.startswith( '[' ):
			self._start_stanza( line )
		else:
			tokens = map(
				str.strip,
				# Drop comments, tokenize around '='
				line.split( '#', 1 )[0].split( '=', 1 )
			)
			if len(tokens) == 2:
				self._add_entry( tokens[0], tokens[1] )
		return

	def report( self, final = False ):
		self._end_stanza()
		if not final and len( self.stanzas ):
			for [name,stanza] in sorted( self.stanzas ):
				self.println( "{0}\n".format( name ) )
				if len( stanza ):
					width = max(
						map(
							len,
							stanza
						)
					)
					fmt = ' {{0:{0}}} = {{1}}'.format(
						width
					)
					for key in sorted( stanza ):
						self.println(
							fmt.format(
								key,
								stanza[key]
							)
						)
					self.println()
		return
