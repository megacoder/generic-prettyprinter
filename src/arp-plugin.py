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
		self.items.set_title_alignment( 'laaaaa' )
		self.items.set_alignment( 'lccccc' )
		for _,items in self.items.get_items():
			print ' '.join( items )
		return

if __name__ == '__main__':
	pp = PrettyPrint()
	pp.pre_begin_file()
	for line in [
		'Address HWtype  HWaddress Flags Mask Iface',
		'192.168.1.155 ether   b8:5a:f7:83:30:f0   C br0',
		'192.168.1.237 (incomplete) br0',
		'192.168.1.37  ether   52:54:00:7d:21:ed   C br0',
		'192.168.1.218 ether   00:22:64:ad:90:ed   C br0',
	]:
		pp.next_line( line )
	pp.report()

