#!/usr/bin/python
# vim: noet sw=4 ts=4

import	os
import	sys
import	superclass

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	NAME		= 'mc'
	DESCRIPTION = """Display /etc/mail/sendmail.mc files in style."""

	def __init__( self ):
		super( PrettyPrint, self ).__init__()
		self.pre_begin_file()
		self.lines = []
		return

	def next_line( self, line ):
		line = line.split( 'dnl' )[0].strip()
		if len( line ) > 0:
			self.lines.append( line )
		return

	def report( self, final = False ):
		if not final:
			for line in sorted( self.lines ):
				self.println( line )
		return
