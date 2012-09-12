#!/usr/bin/python
# vim: noet sw=4 ts=4

import	sys
import	os
import	superclass

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	NAME	= 'snmpd-pp'
	DESCRIPTION = """Print snmpd-style configuration files."""

	PLAIN = [ ] # List of names for lesser prettyprinting
	CUTOFF = 2	# Glob tokens[CUTOFF:] together, not padded

	def	__init__( self ):
		super(PrettyPrint, self).__init__()
		self.reset()
		return

	def	reset( self ):
		super(PrettyPrint, self).reset()
		self._init_all()
		return

	def	_init_all( self ):
		self.entries = []
		return

	def	next_line( self, line ):
		line = line.split( '#', 1 )[0].strip()	# Drop comments!
		tokens = line.split()
		if len(tokens) > 0:
			self.entries.append( tokens )
		return

	def	_dump( self ):
		self.entries.sort()
		widths = { 0:15, 1:15 }
		for tokens in self.entries:
			name = tokens[0].lower()
			if name not in PrettyPrint.PLAIN:
				for tokens in self.entries:
					n = min( PrettyPrint.CUTOFF, len(tokens) )
					for i in xrange( 0, n ):
						n = len(tokens[i])
						try:
							widths[i] = max( widths[i], n )
						except Exception, e:
							widths[i] = n
		for tokens in self.entries:
			name = tokens[0]
			fmt = '%%-%ds' % widths[0]
			print fmt % tokens[0],
			if name in PrettyPrint.PLAIN:
				print ' '.join(tokens[1:]),
			else:
				n = len(tokens)
				cutoff = min( PrettyPrint.CUTOFF, n )
				for i in xrange( 1, cutoff ):
					fmt = '%%-%ds' % widths[i]
					print fmt % tokens[i],
				if cutoff < n:
					print ' '.join(tokens[cutoff:]),
			print
		return

	def	end_file( self, fname ):
		self._dump()
		self._init_all()
