#!/usr/bin/python
# vim: noet sw=4 ts=4

import	os
import	sys
import	superclass

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	NAME = 'modinfo-pp'
	DESCRIPTION = """Display modinfo(8) output in canonical style."""

	def	__init__( self ):
		super( PrettyPrint, self ).__init__()
		return

	def	pre_begin_file( self, fn = None ):
		self.info = dict()
		return

	def	next_line( self, line ):
		tokens = map(
			str.strip,
			line.split( ':', 1 )
		)
		if len(tokens) == 2:
			field			   = tokens[0]
			value			   = tokens[1]
			self.info[ field ] = value
		return

	def	report( self, final = False ):
		if final: return
		width = max(
			14,
			map(
				len,
				self.info.keys()
			)
		)
		fmt = '{{0:<{0}}}: {{1}}'.format( width )
		for key in sorted( self.info.keys() ):
			self.println(
				fmt.format( key, self.info[ key ] )
			)
		return
