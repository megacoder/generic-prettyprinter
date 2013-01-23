#!/usr/bin/python
# vim: noet sw=4 ts=4

import	os
import	sys
import	string
import	superclass

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	NAME = 'bind'
	DESCRIPTION="""Display /etc/named.conf and friends in conical style."""

	INDENT_WITH = '        '

	def __init__( self ):
		super( PrettyPrint, self ).__init__()
		return

	def	reset( self ):
		super( PrettyPrint, self ).reset()
		self._prepare()
		return

	def	_prepare( self ):
		self.tokens = []
		return

	def _spew( self, tokens, comment = None ):
		line = PrettyPrint.INDENT_WITH * self.depth
		if len(tokens) > 0:
			noun = tokens[0]
			line += noun
			if len(tokens) > 1:
				line += ' '*(21-len(noun)) + ' '
				line += ' '.join(tokens[1:])
		if comment is None:
			leadin = ''
		else:
			leadin = ' '*(64-len(line)) + comment
		print line + leadin
		return

	def	begin_file( self, name ):
		super( PrettyPrint, self ).begin_file( name )
		self._prepare()
		return

	def	end_file( self, name ):
		self._process()
		self._prepare()
		super( PrettyPrint, self ).end_file( name )
		return

	def	next_line( self, line ):
		line = line.split( '#', 1 )[0].strip()
		# Ignore blank lines
		if line == "": return
		# Ensure that magic tokens are whitespace-delimited
		line = line.replace( '{', ' { ' )
		line = line.replace( '}', ' } ' )
		line = line.replace( ';', ' ; ' )
		tokens = line.split()
		self.tokens += tokens
		return

	def	_process( self ):
		for token in self.tokens:
			print token
		return
