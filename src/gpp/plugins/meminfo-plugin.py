#!/usr/bin/python

import	os
import	sys
import	superclass

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	NAME = 'meminfo'
	DESCRIPTION="""Display /proc/meminfo in canonical style."""

	def	__init__( self ):
		super( PrettyPrint, self ).__init__()
		return

	def	reset( self ):
		super( PrettyPrint, self ).reset()
		self.lines = []
		self.maxfield = 12
		self.maxvalue = 12
		return

	def	next_line( self, line ):
		tokens = line.rstrip().split( ':' )
		if len(tokens) > 0:
			field = tokens[0].strip()
			value = tokens[1].strip()
			self.maxfield = max( self.maxfield, len(field) )
			if not value.endswith( 'kB' ):
				value = value + '   '
			self.maxvalue = max( self.maxvalue, len(value) )
			self.lines.append( (field, value) )
		return

	def	finish( self ):
		fmt = '%%-%ds  %%%ds' % (self.maxfield, self.maxvalue)
		for (field, value) in self.lines:
			print fmt % (field + ':', value)
		return
