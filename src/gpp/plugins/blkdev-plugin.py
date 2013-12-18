#!/usr/bin/python
# vim: noet sw=4 ts=4

import	os
import	sys
import	superclass
import	math

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	NAME = 'blkdev'
	DESCRIPTION="""Display block device numbers in canonical style."""

	def	__init__( self ):
		super( PrettyPrint, self ).__init__()
		return

	def	reset( self ):
		super( PrettyPrint, self ).reset()
		self._prepare()
		return

	def	_prepare( self ):
		self.devices = {}
		self.attributes = {}
		self.widths = {}
		return

	def	begin_file( self, name ):
		super( PrettyPrint, self ).begin_file( name )
		self.attributes = {}
		return

	def	_keep_width( self, s ):
		n = len( s )
		try:
			self.widths[ s ] = max( self.widths[ s ], n )
		except Exception, e:
			self.widths[ s ] = n
		return

	def	next_line( self, line ):
		tokens = line.split( '=', 1 )
		if len(tokens) == 2:
			field = tokens[0].strip()
			value = tokens[1].strip()
			for s in [field, value]:
				self._keep_width( s )
			self.attributes[field] = value
		return

	def	end_file( self, name ):
		if 'DEVNAME' in self.attributes:
			self.devices[ self.attributes['DEVNAME'] ] = self.attributes
		return

	def	report( self, final = False ):
		keys = sorted( self.devices.keys )
		fmts = []
		for key in keys:
			fmts[ key ] = '%%-%ds' % self.widths[ key ]
		others = False
		for device in sorted( self.devices ):
			for key in keys:
				if key in device:
					s = device[ key ],
				else:
					s = ''
				if others:
					print ' ',
				others = True
				print fmts[ key ] % s,
			if others:
				print
		return
