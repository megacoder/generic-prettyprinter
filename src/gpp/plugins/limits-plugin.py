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
		line = line.split( '#', 1 )[0]
		tokens = line.split()
		n = len(tokens)
		if n == 4:
			for i in xrange( 0, n ):
				try:
					self.widths[i] = max( self.widths[i], len(tokens[i]) )
				except:
					self.widths[i] = len(tokens[i])
			self.entries.append( tokens )
		return

	def	_sort( self, (domain,type,item,value) ):
		key = '%s:%s:%s' % (
			domain,
			item,
			type
		)
		return key

	def	report( self, final = False ):
		if len(self.entries) > 0:
			fmt = '%%%-ds  %%-%ds  %%-%ds  %%%ds' % (
				self.widths[0],
				self.widths[1],
				self.widths[2],
				self.widths[3]
			)
			self.entries.sort( key = self._sort )
			for domain, type, item, value in self.entries:
				print fmt % ( domain, type, item, value )
		self._prepare()
		return
