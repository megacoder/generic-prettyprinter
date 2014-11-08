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
		self.nTitles = len( self.titles )
		self.widths = map(len,self.titles)
		# print 'self.titles={0}'.format(self.titles)
		# print 'self.nTitles={0}'.format(self.nTitles)
		# print 'self.widths={0}'.format(self.widths)
		return

	def	next_line( self, line ):
		if line.startswith( 'IP' ):
			pass
		else:
			tokens = line.split()
			if len(tokens) == self.nTitles:
				widths = map(len,tokens)
				self.widths = map( max, self.widths, widths )
				# print 'appending={0}'.format(tokens)
				self.entries.append( tokens )
		return

	def	report( self, final = False ):
		if not final:
			if len(self.entries) > 0:
				gutter = '  '
				fmts = [
					('%%-%ds' % self.widths[i]) for i in xrange(0, self.nTitles)
				]
				self.println(
					gutter.join(
						(
							fmts[i] % self.titles[i]
						) for i in xrange(0,len(self.titles))
					)
				)
				for tokens in sorted( self.entries ):
					self.println(
						gutter.join(
							(fmts[i] % tokens[i]) for i in xrange(0,self.nTitles)
						)
					)
		return
