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
		self.feeds    = []
		self._new_repo()
		return

	def	_new_repo( self, name = None ):
		self.feed     = []
		self.name	  = name
		self.max_name = 1
		return

	def	next_line( self, line ):
		octothorpe = line.find( '#' )
		if octothorpe > -1:
			line = line[:octothorpe]
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

	def	finish( self ):
		self.feeds.sort( key = lambda (n,l,f) : n.lower() )
		for (name, max_name, entries) in self.feeds:
			print '[%s]' % name
			fmt = '%%%ds = %%s' % max_name
			for (id,value) in entries:
				print fmt % ( id, value )
		return
