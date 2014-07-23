#!/usr/bin/python

import	os
import	sys
import	superclass

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	NAME = 'printcap-pp'
	DESCRIPTION="""Display RHEL-4 printcap files in a readable style."""

	def	__init__( self ):
		super( PrettyPrint, self ).__init__()
		return

	def	process( self, f = sys.stdin ):
		for original in f:
			line = original.replace( '#.*', '' ).rstrip()
			try:
				tokens = line.split( ':' )
			except Exception, e:
				print original,
				continue
			first = tokens[0]
			try:
				name, comment = first.split( '|', 1 )
			except Exception, e:
				name = first
				comment = 'N/A'
			print '%s "%s"' % ( name, comment )
			attrs = tokens[1:]
			attrs.sort()
			for attr in attrs:
				if len(attr) > 0:
					try:
						name, value = attr.split( '=', 1 )
						print '%7s = %s' % (name, value)
					except Exception, e:
						print '%7s' % attr
		return

	def	finish( self ):
		return 0

if __name__ == '__main__':
	pcp = PrettyPrint()
	pcp.process()
	pcp.finish()
