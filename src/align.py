#!/usr/bin/python
# vim: noet sw=4 ts=4

import	sys
import	os
import	re

class	align( object ):

	def	__init__( self, lj = False ):
		self.want_lj = lj
		self.widths  = []
		self.Nwidths = len(self.widths)
		self.numeric = [ False ] * self.Nwidths
		self.re      = re.compile(
			# Signed/unsigned integer|floating|scientific
			r'(^[-+]?[0-9]{1,}([.][0-9]{1,})?([Ee][-+]?[0-9]{1,})?)$'
		)
		self.items   = []
		return

	def	add( self, l ):
		L = len( l )
		# Save to list of items in string format
		F = [
			str(a) for a in l
		]
		self.items.append( F )
		# Get field widths
		widths = [
			len(f) for f in F
		]
		# Grow saved widths if requred
		wider = max( L - self.Nwidths, 0 )
		self.widths += [0] * wider
		# Update widths
		pending = [
			max(
				self.widths[i],
				widths[i]
			) for i in range(L)
		] + self.widths[L:]
		self.widths = pending
		self.Nwidths += wider
		# Detect numeric .vs. string fields
		numeric = map(
			lambda s: self.want_lj and not self.re.match(s),
			F
		)
		self.numeric += [ self.want_lj ] * wider
		pending = [
			self.numeric[i] and numeric[i] for i in range( L )
		] + self.numeric[L:]
		self.numeric = pending
		return

	def	get_items( self ):
		fmts = [
			'{{0:{0}{1}}}'. format(
				'<' if self.numeric[i] else '>',
				self.widths[i]
			) for i in range( len(self.widths) )
		]
		for items in self.items:
			L = len(items)
			fields = [
				fmts[i].format(items[i]) for i in range( L )
			]
			yield fields
		return

if __name__ == '__main__':
	a = align()
	a.add( [ 1,22,333, 'astro' ] )
	a.add( [ 44,5,6, 'rubble' ] )
	for items in a.get_items():
		print ' '.join( items )
