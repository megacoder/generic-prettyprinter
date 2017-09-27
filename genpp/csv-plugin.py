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
		rows   = list()
		widths = dict()
		for row in csv.reader( self.lines ):
		    for i, width in enumerate( row ):
			if not i in widths:
			    widths[i] = 0
			widths[i] = max( widths[i], len(width) )
		    rows.append( row )
		fmts = dict()
		for i, width in enumerate( widths ):
		    fmts[i] = '%%s%%-%ds' % width
		for row in rows:
			sep = ''
			line = ''
			for i, item in enumerate( row ):
			    line += (fmts[i] % (sep, item))
			self.println( line )
		self.lines = []
		return
