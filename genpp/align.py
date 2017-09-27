#!/usr/bin/python
# vim: noet sw=4 ts=4

import	sys
import	os
import	re

class	Align( object ):

	def	_left( self, key, value ):
	   width = self.widths.get( key, 1 )
	   fmt = '{{0:<{0}}}'.format( width )
	   return fmt.format( value )

	def	_right( self, key, value ):
		width = self.widths.get( key, 1 )
		fmt = '{{0:>{0}}}'.format( width )
		return fmt.format( value )

	def	_center( self, key, value, pad = ' ' ):
		width = self.widths.get( key, 1 )
		fmt = '{{0:>{0}}}'.format( width )
		extra = (width - len( value )) / 2
		return fmt.format( value + (pad * extra) )

	def	_auto( self, key, value ):
		if self.numeric.get( key, False ):
			return self._right( key, value )
		if self.want_lj:
			return self._left( key, value )
		return self._right( key, value )

	def	__init__( self, lj = False, titles = 0 ):
		self.align_column = dict()
		self.align_title  = dict()
		self.items        = []
		self.nItems       = 0
		self.numeric      = dict()
		self.titles       = titles
		self.want_lj      = lj
		self.widths       = dict()
		self.align_map = dict(
			a = self._auto,
			c = self._center,
			l = self._left,
			r = self._right
		)
		self.re           = re.compile(
			# Signed/unsigned integer|floating|scientific
			r'(^[-+]?[0-9]{1,}([.][0-9]{1,})?([Ee][-+]?[0-9]{1,})?)$'
		)
		return

	def	set_alignment( self, how = 'a' ):
		i = 0
		for k in range( self.get_columns() ):
			key = str( k )
			self.align_column[ key ] = self.align_map.get(
				how[i],
				self._auto
			)
			i = (i + 1) % len( how )
		return

	def	set_title_alignment( self, how = 'a' ):
		i = 0
		for k in range( self.get_columns() ):
			key = str( k )
			self.align_title[ key ] = self.align_map.get(
				how[ i ],
				self._auto
			)
			i = (i + 1) % len( how )
		return

	def	show_alignment( self, out = sys.stdout ):
		print 'Column Alignment'
		for key in sorted( self.align_column ):
			print >>out, '{0}\t{1}'.format( key, self.align_column[key] )
		return

	def	show_title_alignment( self, out = sys.stdout ):
		print 'Title Alignment'
		for key in sorted( self.align_title ):
			print >>out, '{0}\t{1}'.format( key, self.align_title[key] )
		return

	def	get_columns( self ):
		return len( self.widths.keys() )

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
				self.widths.get( key, 1 )
			)
			# Note numberic columns once titles have been read
			if self.nItems >= self.titles:
				mo = self.re.match( v ) and self.want_lj
				self.numeric[key] = self.numeric.get(key, True) and mo is not None
		# Now, remember the facts
		self.items.append( F )
		self.nItems += 1
		return

	def	get_items( self, titles = 0, sort = False ):
		# Let auto columns inherit the justification of their column data
		for key in self.align_title.keys():
			if self.align_title[key] == self._auto:
				self.align_title[key] = self.align_column.get(
					key,
					self._auto
				)
		# Titles are first
		for H,tokens in enumerate( self.items[:self.titles] ):
			columns = []
			for i,token in enumerate( tokens ):
				key = str( i )
				columns.append(
					self.align_title.get( key, self._auto )( key, token )
				)
			yield H,columns
		if sort == False:
			sort = lambda x : 0
		elif sort == True:
			sort = lambda x : x
		for N,tokens in enumerate(
			sorted( self.items[self.titles:], key = sort )
		):
			columns = []
			for i,token in enumerate( tokens ):
				key = str( i )
				columns.append(
					self.align_column.get( key, self._auto )( key, token )
				)
			yield self.titles+N,columns
		return

if __name__ == '__main__':
	a = Align( lj = True, titles = 1 )
	a.add( [ 'First', 'Second', '3rd', 'Fourth' ] )
	a.add( [ 1.2,22,3.33, 'astro' ] )
	a.add( [ 1,22,333, 'aSTRo' ] )
	a.add( [ -44,5,6, 'rubble' ] )
	a.add( [ 321,'abc','def', 123 ] )
	print 'Plain:'
	a.set_title_alignment( 'rlca' )
	a.set_alignment( 'cccc' )
	for i,items in a.get_items():
		print 'Line {0}->|{1}|'.format( i+1, '|'.join( items ) )
	print 'Sorted'
	a.set_title_alignment( 'llll' )
	a.set_alignment( 'aaaa' )
	for i,items in a.get_items( sort = True):
		print 'Line {0}->|{1}|'.format( i+1, '|'.join( items ) )
	print 'Weird'
	a.set_title_alignment( 'a' )
	a.set_alignment( 'a' )
	import random
	how = lambda x : random.random()
	for i,items in a.get_items( sort = how ):
		print 'Line {0}->|{1}|'.format( i+1, '|'.join( items ) )
