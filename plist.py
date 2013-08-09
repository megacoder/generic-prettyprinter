#!/usr/bin/python

import	os
import	sys

class	Plugger():

	SUFFIX = '-plugin.py'

	def	__init__( self ):
		self._reset()
		return

	def	_reset( self ):
		self.maxname  = 7
		self.names = []
		return

	def	process( self, dn = os.path.join( 'src', 'gpp', 'plugins' )):
		for fn in os.listdir( dn ):
			if fn.endswith( Plugger.SUFFIX ):
				name = fn.split( '-', 1 )[0]
				self.maxname = max( self.maxname, len(name) )
				self.names.append( name )
		return

	def	report( self, final = False ):
		fmt = '%%%ds%s' % ( self.maxname, Plugger.SUFFIX )
		for name in sorted( self.names ):
			print( fmt % name )
		return

if __name__ == '__main__':
	p = Plugger()
	if len(sys.argv) == 1:
		p.process()
	else:
		for dn in sys.argv[1:]:
			p.process( dn )
	p.report()
	exit(0)

