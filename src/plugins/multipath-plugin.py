#!/usr/bin/python
# vim: noet sw=4 ts=4

import	os
import	sys
import	string

class	PrettyPrint( object ):

	INDENT_WITH = '        '

	def __init__( self ):
		self.reset()
		return

	def	reset( self ):
		self.depth = 0
		return

	def spew( self, tokens ):
		line = ''
		for x in xrange( 0, self.depth ):
			line = line + MultipathPrettyPrint.INDENT_WITH
		line = line + tokens[0]
		if len(tokens) > 1:
			while True:
				line = line + ' '
				if len(line) >= 36: break
			line = line + ' '.join(tokens[1:])
		print '%s' % line
		return

	def	process( self, f = sys.stdin ):
		self.depth = 0
		for line in f:
			# Column-1 comments are copied verbatim
			if line.startswith( '#' ):
				print line,
				continue
			# All other lines are to be correctly indented
			# Ensure that magic tokens are whitespace-delimited
			tokens = line.strip().replace( '{', ' { ' ).replace( '}', ' } ').split()
			if len(tokens) > 0:
				final = tokens[-1]
				if final == '{':
					self.spew( [' '.join(tokens)] )
					self.depth += 1
				elif final == '}':
					self.depth -= 1
					self.spew( ['%s' % ' '.join(tokens)] )
				elif tokens[0][0] == '#':
					self.spew( ['%s' % line] )
				else:
					tokens = ' '.join( tokens ).split( '=', 1 )
					if len(tokens) == 2:
						self.spew( [
							'%s = %s' % ( tokens[0], tokens[1] )
						] )
					else:
						self.spew( tokens )
		return

	def	finish( self ):
		return
