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
		return

	def	next_line( self, line ):
		tokens = line.rstrip().split( ':' )
		if len(tokens) > 0:
			field = tokens[0].strip()
			value = tokens[1].strip()
			self.maxfield = max( self.maxfield, len(field) )
			values = value.split()
			# Some entries have no specific units specified
			if not value.endswith( 'kB' ):
				# Null units to make the columns line up
				values.append( '  ' )
			if len(values) >= 2 :
				self.lines.append( (field, values) )
		return

	def	finish( self ):
		maxvalue = 12
		for (field,values) in self.lines:
			maxvalue = max( maxvalue, len(values[0]) )
		ffmt = '%%-%ds' % (self.maxfield+1)
		vfmt = '%%%ds %%s' % maxvalue
		fmt = ffmt + '  ' + vfmt
		for (field, values) in self.lines:
			print fmt % (field + ':', values[0], values[1])
		return
