#!/usr/bin/python
# vim: noet sw=4 ts=4

import	sys
import	os
import	re

class	Align( object ):

	def	__init__( self, lj = False, titles = 0 ):
		self.titles  = titles
		self.want_lj = lj
		self.widths  = dict()
		self.numeric = dict()
		self.re      = re.compile(
			# Signed/unsigned integer|floating|scientific
			r'(^[-+]?[0-9]{1,}([.][0-9]{1,})?([Ee][-+]?[0-9]{1,})?)$'
		)
		self.items   = []
		self.nItems  = 0
		return

	def	get_widths( self ):
		return self.widths

	def	add( self, l ):
		L = len( l )
		# Save to list of items in string format
		F = map(
			str,
			l
		)
		# Grow saved widths if requred
		for i,v in enumerate( F ):
			key = str(i)
			self.widths[key] = max(
				len(v),
				self.widths.get( key, 7 )
			)
			# Note numberic columns once titles have been read
			if self.nItems >= self.titles:
				mo = self.re.match( v ) and self.want_lj
				self.numeric[key] = self.numeric.get(key, True) and mo is not None
		# Now, remember the facts
		self.items.append( F )
		self.nItems += 1
		return

	def	get_items( self, titles = 0, sorted = None ):
		for N,items in enumerate( self.items ):
			fields = []
			for i,item in enumerate( items ):
				key = str( i )
				max_width = self.widths[ key ]
				justification = '>'
				if self.numeric[ key ]:
					justification = '>'
				else:
					if self.want_lj:
						justification = '<'
				# Add formatted item
				fmt = r'{{0:{0}{1}}}'.format( justification, max_width )
				fields.append( fmt.format( item ) )
			yield N,fields
		return

if __name__ == '__main__':
	a = Align( lj = True, titles = 1 )
	a.add( [ 'First', 'Second', 'Third', 'Fourth' ] )
	a.add( [ 1.2,22,3.33, 'astro' ] )
	a.add( [ 1,22,333, 'astro' ] )
	a.add( [ -44,5,6, 'rubble' ] )
	a.add( [ 321,'abc','def', 123 ] )
	for i,items in a.get_items():
		print 'Line {0}->|{1}|'.format( i+1, '|'.join( items ) )
