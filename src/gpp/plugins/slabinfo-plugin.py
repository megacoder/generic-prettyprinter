#!/usr/bin/python

import	os
import	sys
import	superclass

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	NAME = 'slabinfo-pp'
	DESCRIPTION = """Display /proc/slabinfo in conical form."""

	def	__init__( self ):
		super( PrettyPrint, self ).__init__()
		return

	def	reset( self ):
		self.fmt = ''
		self.tokens = []
		self.maxname = 23
		return

	def	process( self, f ):
		lineno = 0
		for line in f:
			lineno += 1
			if lineno == 1:
				print line.strip()
			elif lineno == 2:
				if line[0] != '#':
					printf >>sys.stderr, 'Format error.'
					raise IOError
				tokens = line.rstrip().split()
				if len(tokens) < 2:
					printf >>sys.stderr, 'Title format error.'
					raise IOError
				tokens = [ '# Name' ] + tokens[2:]
				self.fmts = []
				for token in tokens:
					l = len(token)
					self.fmts.append( '%%%d.%ds ' % (l, l) )
				self.tokens.append( tokens )
			else:
				tokens = line.rstrip().split()
				if len(tokens) > 0:
					self.maxname = max( self.maxname, len(tokens[0]) )
				self.tokens.append( tokens )
		return

	def	finish( self ):
		self.fmts[0] = '%%%d.%ds' % (self.maxname, self.maxname)
		for tokens in self.tokens:
			for fmt in self.fmts:
				try:
					token = tokens.pop(0)
				except Exception, e:
					token = 'N/A'
				print fmt % token,
			print
		return
