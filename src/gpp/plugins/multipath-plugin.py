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
		self.depth = 0
		self.do_capture = False
		self.captured = []
		return

	def spew( self, tokens, comment = None ):
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

	def	process( self, f = sys.stdin ):
		self.depth = 0
		for line in f:
			line = line.strip()
			# Column-1 comments are copied verbatim
			octothorpe = line.find( '#' )
			if octothorpe == 0:
				print line
				continue
			if octothorpe == -1:
				comment = None
			else:
				comment = line[octothorpe:]
				line = line[:octothorpe]
			# All other lines are to be correctly indented
			# Ensure that magic tokens are whitespace-delimited
			line = line.replace( '{', ' { ' )
			line = line.replace( '}', ' } ' )
			tokens = line.split()
			if len(tokens) == 0:
				self.spew( [], comment )
			else:
				keyword = tokens[0]
				final = tokens[-1]
				if final == '{':
					self.spew( tokens, comment )
					self.depth += 1
					if keyword in [ 'device' ]:
						self.captured = []
						self.do_capture = True
				elif final == '}':
					self.captured.sort( key = lambda (t, c) : t[0].lower() )
					for saved, said in self.captured:
						self.spew( saved, said )
					self.do_capture = False
					self.captured = []
					self.depth -= 1
					self.spew( tokens, comment )
				else:
					equals = line.find( '=' )
					if equals > -1:
						tokens = [ line[:equals], line[equals:] ]
						tokens = [ ' = '.join(tokens) ]
					if self.do_capture:
						self.captured.append( (tokens, comment) )
					else:
						self.spew( tokens, comment )
		return

	def	finish( self ):
		return
