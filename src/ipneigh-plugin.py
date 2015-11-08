#!/usr/bin/python
# vim: noet sw=4 ts=4

import	os
import	sys
import	string
import	superclass
import	re
from	align	import	*

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	NAME = 'ip-neigh'
	DESCRIPTION="""Display ip-neighbour(1) in canonical style."""

	def __init__( self ):
		super( PrettyPrint, self ).__init__()
		self.pre_begin_file()
		return

	def	pre_begin_file( self ):
		self.items = []
		return

	def	next_line( self, line ):
		line = line.strip()
		if len(line) > 0:
			parts = line.split()
			ip = parts[0].split( '.', 4 )
			self.items.append(
				([ int(x) for x in ip], parts[0], parts[1:-1], parts[-1])
			)
		return

	def	report( self, final = False ):
		if not final:
			if len(self.items) > 0:
				self.items.sort( key = lambda (a,ip,mid,state): a )
				a = align()
				for (tcpip,ip,mid,state) in self.items:
					fields = [ ip ]
					while len( mid ) < 4:
						mid.append( "" )
					fields.append( ' '.join( mid ) )
					fields.append( state )
					a.add( fields )
				for fields in a.get_items():
					print ' '.join( fields )
		return
