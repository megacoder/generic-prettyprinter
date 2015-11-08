#!/usr/bin/python
# vim: noet sw=4 ts=4

import	sys
import	os

class	align( object ):

	def	__init__( self ):
		self.widths = {}
		self.items  = []
		return

	def	add( self, l ):
		for k,v in enumerate( l ):
			width = len( str( v ) )
			self.widths[ k ] = max(
				self.widths[ k ] if k in self.widths else 0,
				width
			)
		self.items.append( l )
		return

	def	get_items( self ):
		for items in self.items:
			aligned = []
			for n,item in enumerate( items ):
				fmt = '{0:%d}' % self.widths[n]
				aligned.append(
					fmt.format(
						str( item )
					)
				)
			yield aligned
		return

if __name__ == '__main__':
	a = align()
	a.add( [ 1,22,333 ] )
	a.add( [ 44,5,6 ] )
	for items in a.get_items():
		print ' '.join( items )
