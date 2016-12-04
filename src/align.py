#!/usr/bin/python
# vim: noet sw=4 ts=4

import	sys
import	os
import	re

class	align( object ):

	def	__init__( self, lj = False ):
		self.want_lj = lj
		self.widths  = dict()
		self.numeric = dict()
		self.re      = re.compile(
			# Signed/unsigned integer|floating|scientific
			r'(^[-+]?[0-9]{1,}([.][0-9]{1,})?([Ee][-+]?[0-9]{1,})?)$'
		)
		self.items   = []
		return

	def	add( self, l ):
		L = len( l )
		# Save to list of items in string format
		F = map(
			str,
			l
		)
		self.items.append( F )
		# Grow saved widths if requred
		for i,v in enumerate( F ):
			key = str(i)
			self.widths[key] = max(
				len(v),
				self.widths.get( key, 7 )
			)
			mo = self.re.match( v ) and self.want_lj
			self.numeric[key] = self.numeric.get(key, True) and mo is not None
		return

	def	_justify( self, v ):
		if not self.want_lj or self.re.match( v ):
			return '>'
		return '<'

	def	get_items( self ):
		# Construct the format strings
		for N,items in enumerate( self.items ):
			fields = []
			for i,item in enumerate( items ):
				key = str( i )
				fmt = '{{0:{0}{1}}}'.format(
					self._justify( item ),
					self.widths[key]
				)
				fields.append(
					fmt.format( item )
				)
			yield N,fields
		return

if __name__ == '__main__':
	a = align( lj = True )
	a.add( [ 1,22,333, 'astro' ] )
	a.add( [ 44,5,6, 'rubble' ] )
	a.add( [ 321,'abc',123 ] )
	for i,items in a.get_items():
		print 'Line {0}->|{1}|'.format( i+1, '|'.join( items ) )
