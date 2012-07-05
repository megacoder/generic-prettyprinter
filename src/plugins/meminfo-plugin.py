#!/usr/bin/python

import	os
import	sys

class	PrettyPrint( object ):

	def	__init__( self ):
		self.reset()
		return

	def	reset( self ):
		self.lines = []
		self.maxfield = 12
		self.maxvalue = 12
		return

	def	process( self, f = sys.stdin ):
		for line in f:
			tokens = line.rstrip().split( ':' )
			if len(tokens) == 0: continue
			field = tokens[0].strip()
			value = tokens[1].strip()
			self.maxfield = max( self.maxfield, len(field) )
			if not value.endswith( 'kB' ):
				value = value + '   '
			self.maxvalue = max( self.maxvalue, len(value) )
			self.lines.append( (field, value) )
		return

	def	finish( self ):
		fmt = '%%-%ds %%%ds' % (self.maxfield+1, self.maxvalue)
		for (field, value) in self.lines:
			print fmt % (field + ':', value)
		return
