#!/usr/bin/python
# vim: noet sw=4 ts=4

import	os
import	sys
import	string
import	superclass
import	re
import	align

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	NAME = 'ip-neigh'
	DESCRIPTION="""Display ip-neighbour(1) in canonical style."""

	def __init__( self ):
		super( PrettyPrint, self ).__init__()
		self.pre_begin_file()
		return

	def	pre_begin_file( self ):
		self.items = align.Align()
		return

	def	next_line( self, line ):
		tokens = map(
			str.strip,
			line.split()
		)
		N = len( tokens )
		if N > 0:
			proper = 6
			if N < proper:
				tokens = tokens[:-1] + ([ ' ' ] * (proper - N) ) + tokens[-1:]
			self.items.add( tokens )
		return

	def	report( self, final = False ):
		if not final:
			for _,tokens in self.items.get_items(
				sort = lambda t : map( int, t[0].split('.') )
			):
				print ' '.join( tokens )
		return

if __name__ == '__main__':
	pp = PrettyPrint()
	pp.pre_begin_file()
	pp.next_line( '192.168.1.166 dev br0 lladdr cc:6d:a0:2b:6d:d1 REACHABLE'
			  );
	pp.next_line( '192.168.1.254 dev br0  FAILED' )
	pp.next_line( ' 192.168.1.155 dev br0 lladdr b8:5a:f7:83:30:f0 STALE' )
	pp.report()
