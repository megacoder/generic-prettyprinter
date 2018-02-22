#!/usr/bin/python
# vim: noet sw=4 ts=4

import	sys
import	os

class	Bunch( object ):

	def	__init__( self, **kwds ):
		self.__dict__.update( kwds )
		return

	def	__getattr__( self, name ):
		if name in self.__dict__:
			return self.__dict__[name]
		else:
			raise AttributeError( 'No such attribute: {0}'.format( name ) )

	def	__setattr__( self, name, value ):
		self.__dict__[name] = value

	def	__delattr__( self, name ):
		if name in self.__dict__:
			del self.__dict__[name]
		else:
			raise AttributeError( 'No such attribute: {0}'.format( name ) )
		return

	def	__iter__( self ):
		return iter( self.__dict__ )

	def	__repr__( self ):
		labels = [ l for l in dir(self) if l[0].islower() ]
		values = [ '{0}:{1}'.format( l, self.__dict__[l] ) for l in labels ]
		return '; '.join( values )

if __name__ == '__main__':
	b = Bunch(
		first = 'Tommy',
		last = 'Reynolds'
	)
	print b
	print 'Name: {0}, {1}'.format(
		b.last,
		b.first
	)
	print 'iter={0}'.format(
		[ x for x in b ]
	)
	exit( 0 )
