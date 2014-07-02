#!/usr/bin/python
# vi: noet sw=4 ts=4

import	os
import	sys
import	superclass
import	string

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	NAME = 'iptables-pp'
	DESCRIPTION = """Display 'iptables -L' output in canonical style."""

	def	__init__( self ):
		super( PrettyPrint, self ).__init__()
		self.reset()
		return

	def	reset( self ):
		super( PrettyPrint, self ).reset()
		self._reset()
		return

	def	_reset( self ):
		self.chain    = None
		self.entries  = []
		self.headers  = None
		self.nHeaders = 0
		self.widths   = None
		return

	def	own_glob( self ):
		return '-'

	def	next_line( self, line ):
		if line.startswith( 'Chain' ):
			self.report()
			self._reset()
			self.chain = line
		elif line.startswith( 'target' ):
			self.headers = line.split()
			self.headers.append( 'modifiers' )
			self.widths = map(len,self.headers)
			self.nHeaders = len( self.headers )
		else:
			tokens = line.split( None, 5 )
			n = len( tokens )
			if n > 0:
				while len(tokens) < 6:
					tokens.append( '' )
				tokens = map( string.strip, tokens )
				for i in xrange( 0, len(tokens) ):
					self.widths[i] = max( self.widths[i], len(tokens[i]) )
				self.entries.append( tokens )
		return

	def	report( self, final = False ):
		if self.chain:
			self.println( self.chain )
			gutter = '  '
			fmts = [
				('%%-%ds' % self.widths[i]) for i in xrange(0, self.nHeaders)
			]
			self.println(
				gutter.join(
					(
						fmts[i] % self.headers[i]
					) for i in xrange(0,len(self.headers))
				)
			)
			for tokens in self.entries:
				self.println(
					gutter.join(
						(fmts[i] % tokens[i]) for i in xrange(0,self.nHeaders)
					)
				)
		return
