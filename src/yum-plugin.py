#!/usr/bin/python

import	os
import	sys
import	superclass

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	NAME        = 'yum.repo'
	DESCRIPTION = """Display /etc/yum.repos.d/*.repo files in style."""

	def	__init__( self ):
		super( PrettyPrint, self ).__init__()
		return

	def	start( self ):
		super( PrettyPrint, self ).start()
		self.pre_begin_file()
		return

	def	pre_begin_file( self ):
		self.feeds    = []
		self._new_repo()
		return

	def	_new_repo( self, name = None ):
		self.feed     = []
		self.name     = name
		self.max_name = 1
		return

	def	ignore( self, fn ):
		return not fn.endswith( '.repo' )

	def	add_repo( self ):
		if self.name is not None:
			self.feed.sort( key = lambda (x,y): x.lower() )
			self.feeds.append( (self.name, self.max_name, self.feed) )
		return

	def	next_line( self, line ):
		line = line.split( '#', 1 )[0]
		if line.startswith( '[' ):
			self.add_repo()
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
	    if not final:
		self.add_repo()
		self.feeds.sort( key = lambda (n,l,f) : n.lower() )
		others = False
		for (name, max_name, entries) in self.feeds:
			if others:
				self.println()
			others = True
			self.println( '[{0}]'.format( name ) )
			print
			fmt = ' {0:>%d} = {1}' % max_name
			for (id,value) in entries:
				self.println( fmt.format( id, value ) )
	    return
