#!/usr/bin/python

import	os
import	sys
import	superclass

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	NAME = 'yum.repo'
	DESCRIPTION = """Display /etc/yum.repos.d/*.repo files in style."""

	def	__init__( self ):
		super( PrettyPrint, self ).__init__()
		return

	def	reset( self ):
		super( PrettyPrint, self ).reset()
		self.prepare_for_new_file()
		return

	def	prepare_for_new_file( self ):
		self.feeds    = []
		self._new_repo()
		return

	def	_new_repo( self, name = None ):
		self.feed     = []
		self.name	  = name
		self.max_name = 1
		return

	def	ignore( self, fn ):
		return not fn.endswith( '.repo' )

	def	next_line( self, line ):
		line = line.split( '#', 1 )[0]
		if line.startswith( '[' ):
			if self.name is not None:
				self.feed.sort( key = lambda (x,y): x.lower() )
				self.feeds.append( (self.name, self.max_name, self.feed) )
			self._new_repo( line.strip()[1:-1] )
		else:
			tokens = line.split( '=', 1 )
			if len(tokens) == 2:
				name = tokens[0].strip()
				value = tokens[1].strip()
				self.max_name = max( self.max_name, len(name) )
				self.feed.append( (name, value) )
		return

	def	report( self, final = False ):
		self.feeds.sort( key = lambda (n,l,f) : n.lower() )
		others = False
		for (name, max_name, entries) in self.feeds:
			if others:
				print
			others = True
			print '[%s]' % name
			print
			fmt = ' %%%ds = %%s' % max_name
			for (id,value) in entries:
				print fmt % ( id, value )
		self.prepare_for_new_file()
		return
