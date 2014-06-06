#!/usr/bin/python

import	os
import	sys
import	superclass

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	NAME = 'slabinfo-pp'
	DESCRIPTION = """Display /proc/slabinfo in conical form."""

	def	__init__( self ):
		super( PrettyPrint, self ).__init__()
		self._prepare()
		return

	def	_prepare( self ):
		self.version = None
		self.headers = None
		self.widths  = {
			1: 23
		}
		self.tokens  = []
		return

	def	max_sizes( self, tokens ):
		i = 1
		for token in tokens:
			try:
				self.widths[i] = max( self.widths[i], len(token) )
			except:
				self.widths[i] = len(token)
			i += 1
		return

	def	next_line( self, line ):
		# print 'line=[%s]' % line
		if line.startswith( 'slabinfo' ):
			# Version line
			# print 'line1=[%s]' % line
			self.version = line
		elif line.startswith( '#' ):
			# Column titles
			tokens = [ '# name' ] + line.split()[2:]
			self.max_sizes( tokens )
			self.headers = tokens
		else:
			tokens = line.split()
			self.max_sizes( tokens )
			self.tokens.append( tokens )
		return

	def	print_aligned( self, tokens ):
		i = 1
		line = ''
		sep = ''
		for token in tokens:
			if i == 1:
				just = '-'
			else:
				just = ''
			fmt = '%%%s%d.%ds' % (
				just,
				self.widths[i],
				self.widths[i]
			)
			line = line + sep + (fmt % token)
			sep = ' '
			i += 1
		self.println( line )
		return

	def	report( self, final = False ):
		if self.version:
			self.println( self.version )
		if self.headers:
			self.print_aligned( self.headers )
		self.tokens.sort( key = lambda t : t[0].lower() )
		for tokens in self.tokens:
			self.print_aligned( tokens )
		self._prepare()
		return
