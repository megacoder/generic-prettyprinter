#!/usr/bin/python

import	os
import	sys
import	superclass

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	NAME = 'limits-pp'
	DESCRIPTION = """Display /etc/security/limits.conf files in canonical style."""

	def	__init__( self ):
		super( PrettyPrint, self ).__init__()
		return

	def	reset( self ):
		super( PrettyPrint, self ).reset()
		self._prepare()
		return

	def	_prepare( self ):
		self.entries = []
		self.widths  = {}
		return

	def	begin_file( self, name ):
		super( PrettyPrint, self ).begin_file( name )
		self._prepare()
		return

	def	next_line( self, line ):
		octothorpe = line.find( '#' )
		if octothorpe > -1:
			line = line[:octothorpe]
		tokens = line.split()
		n = len(tokens)
		if n == 3:
			for i in xrange( 0, n ):
				try:
					self.widths[i] = max( self.widths[i], len(tokens[i]) )
				except:
					self.widths[i] = len(tokens[i])
			tokens[2] = int( tokens[2] )
			self.entries.append( tokens )
		return

	def	report( self, final = False ):
		if len(self.entries) > 0:
			fmt = '%%-ds  %%-%ds  %%%dd' % (
				self.widths[0],
				self.widths[1],
				self.widths[2]
			)
			for user,which,value in sorted( self.entries ):
				print fmt % ( user, which, value )
		self._prepare()
		return
