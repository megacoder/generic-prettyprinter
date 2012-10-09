#!/usr/bin/python
# vim: noet sw=4 ts=4

import	os
import	sys
import	string
import	superclass

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	NAME = 'tcpwrapper'
	DESCRIPTION="""Display /etc/hosts.* in conical style."""

	def __init__( self ):
		super( PrettyPrint, self ).__init__()
		return

	def	reset( self ):
		super( PrettyPrint, self ).reset()
		self._setup()
		return

	def	_setup( self ):
		self.widths  = {}
		self.content = []
		return

	def	next_file( self, name ):
		super( PrettyPrint, self ).next_file( name )
		self._setup()
		return

	def	end_file( self, name ):
		self._show()
		self._setup()
		return

	def	_show( self ):
		for (n,tokens) in self.content:
			prefix = ''
			for i in xrange( 0, n ):
				fmt = '%%s%%-d%s' % self.widths[i]
				print fmt % (prefix, tokens[i]),
				prefix = ' : '
			print
		return

	def	next_line( self, line ):
		line = line.strip()
		octothorpe = line.find( '#' )
		if octothorpe > -1:
			line = line[:octothorpe]
		line = line.strip()
		tokens = line.split( ':' )
		n = len(tokens)
		if n > 0:
			for i in xrange( 0, n ):
				try:
					self.widths[i] = max(self.widths[i], len(tokens[i]))
				except Exception, e:
					self.widths[i] = len(tokens[i])
			self.content.append( (n, tokens) )
		return

	def	finish( self ):
		self._show()
		return
