#!/usr/bin/python

import	os
import	sys
import	superclass

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	NAME = 'resolv-pp'
	DESCRIPTION = """Display /etc/resolv.conf files in canonical style."""

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
		tokens = line.split( '#', 1 )[0].split()
		n = len(tokens)
		if n > 0:
			for i in xrange( 0, n ):
				L = len(tokens[i])
				try:
					self.widths[i] = max( self.widths[i], L )
				except:
					self.widths[i] = L
			self.entries.append( tokens )
		return

	def	report( self, final = False ):
		if len(self.entries) > 0:
			for tokens in sorted( self.entries ):
				line = ''
				sep = ''
				for i in xrange( len(tokens) ):
					fmt = '%%-%ds' % self.widths[i]
					line += sep + (fmt % tokens[i])
					sep = ' '
				self.println( line )
		self._prepare()
		return
