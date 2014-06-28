#!/usr/bin/python
# vi: noet sw=4 ts=4

import	os
import	sys
import	superclass

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	NAME = 'pna-pp'
	DESCRIPTION = """Display /proc/net/arp files in canonical style."""

	def	__init__( self ):
		super( PrettyPrint, self ).__init__()
		self.reset()
		return

	def	reset( self ):
		super( PrettyPrint, self ).reset()
		self._reset()
		return

	def	_reset( self ):
		self.entries = []
		self.titles = [
			'IP address',
			'HW type',
			'Flags',
			'HW address',
			'Mask',
			'Device',
		]
		self.widths = [
			len( x ) for x in self.titles,
		]
		return

	def	next_line( self, line ):
		if line.startswith( 'IP' ):
			pass
		else:
			tokens = line.split()
			if len(tokens) == len( self.titles ):
				for i in xrange( 0, len(self.titles) ):
					self.widths[ i ] = max(
						self.width[ i ],
						len( tokens[ i ] )
					)
				self.entries.append( tokens )
		return

	def	report( self, final = False ):
		if len(self.entries) > 0:
			fmts = [
				'%%-%ds' % d for d in self.widths
			]
			self.println(
				' '.join(
					(fmts[i] % self.titles[i]) for i in xrange(0,len(self.titles))
				)
			)
			for tokens in sorted( self.entries ):
				self.println(
					' '.join(
						(fmts[i] % tokens[i]) for i in xrange(0,len(tokens ))
					)
				)
		return
