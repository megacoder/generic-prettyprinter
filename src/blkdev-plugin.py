#!/usr/bin/python
# vim: noet sw=4 ts=4

import	os
import	sys
import	superclass
import	math
import	align

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	NAME = 'blkdev'
	DESCRIPTION="""Display block device numbers in canonical style."""
	GLOB = r'/sys/block/*/uevent'

	def	__init__( self ):
		super( PrettyPrint, self ).__init__()
		self.items = align.Align( lj = True, titles = 1 )
		self.items.add([
			'Type', 'Name', 'Major', 'Minor'
		])
		return

	def	begin_file( self, name ):
		self.attributes = dict()
		return

	def	next_line( self, line ):
		items = map(
			str.strip,
			line.split( '=', 1 )
		)
		if len(items) == 2:
			self.attributes[ items[0] ] = items[1]
		return

	def	end_file( self, name ):
		items = [
			self.attributes.get( 'DEVTYPE', 'N/A' ),
			self.attributes.get( 'DEVNAME', '?' ),
			self.attributes.get( 'MAJOR', '0' ),
			self.attributes.get( 'MINOR', '0' )
		]
		self.items.add( items )
		return

	def	report( self, final = False ):
		if final:
			for _,items in self.items.get_items():
				self.println( ' '.join( items ) )
		return

if __name__ == '__main__':
	fn = '<selftest>'
	pp = PrettyPrint()
	pp.pre_begin_file()
	pp.begin_file( fn )
	for line in [
		'MAJOR=8',
		'MINOR=6',
		'DEVNAME=vda',
		'DEVTYPE=disk',
	]:
		pp.next_line( line )
	pp.end_file( fn )
	pp.post_end_file()
	pp.report( final = True )

