#!/usr/bin/python
# vim: noet sw=4 ts=4

import	sys
import	os
import	stat
import	superclass

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	NAME = 'mount'
	DESCRIPTION = """Display 'mounted.ocfs2 -d|-f' in a canonical form."""

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
		self.is_dsw  = False
		self.first   = True
		self.title   = []
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
			self.is_dsw = (n == 6)
			self.title = tokens
			self.first = False
			self._max_widths( tokens )
		else:
			if self.is_dsw:
				# mounted.ocfs2 -d
				# Device Stack Cluster F UUID Label
				self._max_widths( tokens )
				self.content.append( tokens )
			else:
				# mounted.ocfs2 -f
				# Device Stack Cluster F Nodes
				if n < 5:
					nodes = []
				else:
					nodes = tokens[4:]
					for i in xrange( 0, len(nodes) ):
						nodes[i] = nodes[i].replace( ',', '' )
					nodes.sort()
				tokens = tokens[:4] + [ ', '.join(nodes) ]
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
		self._print_set( self.title )
		bars = self.title
		for i in xrange( 0, len(self.title) ):
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
