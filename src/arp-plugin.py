#!/usr/bin/python
# vim: noet sw=4 ts=4

import	os
import	sys
import	string
import	superclass
import	re
import	align

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	NAME = 'arp'
	DESCRIPTION="""Display arp(1) in canonical style."""

	def __init__( self ):
		super( PrettyPrint, self ).__init__()
		self.pre_begin_file()
		return

	def	pre_begin_file( self ):
		self.items = align.Align( titles = 1 )
		return

	def	next_line( self, line ):
		tokens = map(
			str.strip,
			line.split()
		)
		Ntokens = len( tokens )
		if Ntokens >= 4:
			# If no netmask field, insert an empty one
			if Ntokens == 5:
				tokens = tokens[:4] + [ "" ] + tokens[4:]
			self.items.add( tokens )
		return

	def	report( self, final = False ):
		for _,items = self.items.get_items():
			print ' '.join( items )
		return
