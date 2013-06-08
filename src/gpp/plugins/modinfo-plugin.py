#!/usr/bin/python

import	os
import	sys
import	superclass

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	NAME = 'modinfo-pp'
	DESCRIPTION = """Display modinfo(8) output in canonical style."""

	def	__init__( self ):
		super( PrettyPrint, self ).__init__()
		return

	def	reset( self ):
		super( PrettyPrint, self ).reset()
		self._prepare()
		return

	def	_prepare( self ):
		self.others = False
		self.info = {}
		return

	def	begin_file( self, name ):
		super( PrettyPrint, self ).begin_file( name )
		self._prepare()
		return

	def	begin_file( self, fn ):
		super( PrettyPrint, self ).begin_file( fn )
		self._prepare()
		return

	def	report( self, final = False ):
		if self.info != {}:
			if self.others:
				self.println()
			self.others = True
			maxname = 7
			for key in sorted( self.info.keys() ):
				maxname = max( maxname, len( self.info[key] ) )
			fmt = '%%%ds: %%s' % maxname
			for key in sorted( self.info.keys() ):
				self.println( fmt % (key, self.info[key]) )
			self.info = {}
		return

	def	next_line( self, line ):
		tokens = line.split( ':', 1 )
		if len(tokens) == 2:
			field = tokens[0]
			value = tokens[1]
			if field == "filename":
				self.report()
			self.info[field] = value
		return
