#!/usr/bin/python
# vim: noet sw=4 ts=4

import	os
import	sys
import	string
import	superclass

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	NAME = 'multipath-pp'
	DESCRIPTION="""Display /etc/multipath.conf in conical style."""

	INDENT_WITH = '        '

	def __init__( self ):
		super( PrettyPrint, self ).__init__()
		return

	def	reset( self ):
		super( PrettyPrint, self ).reset()
		self.depth = 0
		self.do_capture = False
		self.captured = []
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
		super( PrettyPrint, self ).begin_file()
		self.depth = 0
		return

	def	_end_block( self ):
		self.captured.sort( key = lambda (t, c) : t[0].lower() )
		for saved, said in self.captured:
			self._spew( saved, said )
		self.captured = []
		return

	def	next_line( self, line ):
		line = line.strip()
		octothorpe = line.find( '#' )
		if octothorpe == -1:
			comment = None
		else:
			comment = line[octothorpe:]
			line = line[:octothorpe]
		# Ensure that magic tokens are whitespace-delimited
		line = line.replace( '{', ' { ' )
		line = line.replace( '}', ' } ' )
		tokens = line.split()
		if len(tokens) == 0:
			self._spew( [], comment )
		else:
			keyword = tokens[0]
			final = tokens[-1]
			if final == '{':
				self._spew( tokens, comment )
				self.depth += 1
				if keyword in [ 'device' ]:
					self.captured = []
					self.do_capture = True
			elif final == '}':
				self._end_block()
				self.do_capture = False
				self.depth -= 1
				self._spew( tokens, comment )
			else:
				equals = line.find( '=' )
				if equals > -1:
					tokens = [ line[:equals], line[equals:] ]
					tokens = [ ' = '.join(tokens) ]
				if self.do_capture:
					self.captured.append( (tokens, comment) )
				else:
					self._spew( tokens, comment )
		return

	def	finish( self ):
		return
