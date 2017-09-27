#!/usr/bin/python
# vim: noet sw=4 ts=4

import	os
import	sys
import	string
import	superclass
import	re

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	NAME = 'tcpdump'
	DESCRIPTION="""Display tcpdump ASCII out in conical style."""

	def __init__( self ):
		super( PrettyPrint, self ).__init__()
		return

	def	pre_begin_file( self, name = None ):
		self.lines           = list()
		self.nFixedWidths    = 7
		self.nVariableWidths = 1
		self.nFields         = self.nFixedWidths + self.nVariableWidths
		self.nSplittable     = self.nFields - 1
		self.variableWidths  = [ 0 ] * self.nFixedWidths
		return

	def	next_line( self, line ):
		tokens = map(
			str.strip,
			line.split( None, self.nSplittable )
		)
		if len( tokens ) == self.nFields:
			self.variableWidths = [
				max( self.variableWidths[i], len(tokens[i]) ) for i in range(
					self.nFixedWidths
				)
			]
			self.lines.append( tokens )
		return

	def	report( self, final = False ):
		if not final:
			fmts = [
				'{{0:{0}}}'.format( self.variableWidths[i] ) for i in range(
					self.nFixedWidths
				)
			] + (
				[ '{0}' ] * self.nVariableWidths
			)
			for tokens in self.lines:
				fields = [
					fmts[i].format( tokens[i] ) for i in range(
						len( tokens )
					)
				]
				self.println( ' '.join( fields ) )
		return
