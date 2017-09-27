#!/usr/bin/python
# vim: noet sw=4 ts=4

import	os
import	sys
import	superclass

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	NAME = 'kdump'
	DESCRIPTION = """Display /etc/kdump.* files in canonical style."""

	def	__init__( self ):
		super( PrettyPrint, self ).__init__()
		return

	def pre_begin_file( self, name = None ):
	    self.values = dict()
	    return

	def	next_line( self, line ):
		tokens = map(
			str.strip,
			line.split( '#', 1 )[0].split()
		)
		L = len( tokens )
		if L:
			key = tokens[0]
			if L == 1:
				value = []
			elif L > 1:
				value = tokens[1:]
			self.values[ key ] = value
		return

	def	report( self, final = False ):
		if not final:
			width = max(
				map(
					len,
					self.values
				)
			)
			fmt = '{{0:<{0}}} {{1}}'.format( width )
			for key in sorted(
				self.values,
				key = lambda s : s.lower()
			):
				value = ' '.join( self.values[ key ] )
				self.println(
					fmt.format( key, value )
				)
		return
