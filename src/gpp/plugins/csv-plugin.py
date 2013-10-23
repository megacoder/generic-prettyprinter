#!/usr/bin/python

import	os
import	sys
import	superclass
import	csv

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	NAME = 'csv-pp'
	DESCRIPTION = """Display comma-separated-value files in canonical style."""

	def	__init__( self ):
		super( PrettyPrint, self ).__init__()
		return

	def	reset( self ):
		super( PrettyPrint, self ).reset()
		self.lines = []
		return

	def	begin_file( self, name ):
		super( PrettyPrint, self ).begin_file( name )
		self.lines = []
		return

	def	next_line( self, line ):
		self.lines.append( line )
		return

	def	report( self, final = False ):
		rows = []
		for row in csv.reader( self.lines ):
			for i in xrange( 0, len(row) ):
				try:
					self.widths[i] = max( self.widths[i], len(row[i]) )
				except:
					self.widths[i] = len(row[i])
			rows.append( row )
		fmts = {}
		for i in self.widths.keys():
			fmts[i] = '%%s%%-%ds' % self.widths[i]
		for row in rows:
			sep = ''
			line = ''
			for i in xrange( 0, len(row) ):
				line += (fmts[i] % (sep, row[i]))
				sep = ' '
			self.println( line )
		self.lines = []
		return
