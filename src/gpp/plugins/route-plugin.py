#!/usr/bin/python
# vim: noet sw=4 ts=4

import	sys
import	os
import	stat
import	superclass

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	NAME = 'route'
	DESCRIPTION = """Display routing table(s) in a canonical form."""

	def	__init__( self ):
		super( PrettyPrint, self ).__init__()
		return

	def	reset( self ):
		super( PrettyPrint, self ).reset()
		self._prepare()
		return

	def	_prepare( self ):
		self.widths  = {}
		self.content = []
		self.first   = True
		self.title	 = None
		return

	def	begin_file( self, name ):
		super( PrettyPrint, self ).begin_file( name )
		self._prepare()
		return

	def	_max_widths( self, tokens ):
		for i in xrange( 0, len(tokens) ):
			token = tokens[i]
			try:
				self.widths[i] = max( self.widths[i], len(token) )
			except:
				self.widths[i] = len(token)
		return

	def	next_line( self, line ):
		tokens = line.rstrip().split()
		n = len( tokens )
		if n == 0: return
		if self.first:
			if tokens[0] == 'Kernel':
				# route -n
				pass
			elif tokens[0] == 'Iface' or tokens[0] == 'Destination':
				# /proc/net/route
				self.first = False
				self.title = tokens
				self._max_widths( tokens )
			else:
				# ip route show -- there is no title
				self.first = False
				self._max_widths( tokens )
				self.content.append( tokens )
		else:
			self._max_widths( tokens )
			self.content.append( tokens )
		return

	def	_print_set( self, tokens ):
		sep = ''
		for i in xrange( 0, len(tokens) ):
			try:
				L = self.widths[i]
			except:
				L = len(tokens[i])
				self.widths[i] = L
			fmt = '%%s%%-%ds' % self.widths[i]
			print fmt % (sep, tokens[i] ),
			sep = ' '
		print
		return

	def	_report( self ):
		self.content.sort()
		if self.title:
			self._print_set( self.title )
			bars = self.title
			for i in xrange( 0, len(bars) ):
				bars[i] = '-' * self.widths[i]
			self._print_set( bars )
			print
		for tokens in self.content:
			self._print_set( tokens )
		self._prepare()
		return

	def	end_file( self, name ):
		self._report()
		super( PrettyPrint, self ).end_file( name )
		return

	def	finish( self ):
		if not self.first:
			self._report()
		return
