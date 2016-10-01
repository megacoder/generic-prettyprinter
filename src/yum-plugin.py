#!/usr/bin/python
# vim: noet sw=4 ts=4

import	os
import	sys
import	superclass

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	NAME        = 'yum.repo'
	DESCRIPTION = """Display /etc/yum.repos.d/*.repo files in style."""

	def	__init__( self ):
		super( PrettyPrint, self ).__init__()
		self.pre_begin_file( None )
		return

	def	ignore( self, fn ):
		return not fn.endswith( '.repo' )

	def	pre_begin_file( self, name = None ):
		super( PrettyPrint, self ).pre_begin_file( name )
		self.repos = list()
		self._new_repo()
		return

	def	_new_repo( self, name = None ):
		self.repo = dict( _name = name )
		return

	def	_end_repo( self ):
		if '_name' in self.repo and self.repo['_name']:
			self.repos.append( self.repo )
		return

	def	next_line( self, line ):
		if line.startswith( '[' ):
			self._end_repo()
			self._new_repo( line.strip()[1:-1] )
		else:
			tokens = map(
				str.strip,
				line.split( '#', 1 )[0].split( '=', 1 )
			)
			if len(tokens) == 2:
				name  = tokens[0]
				value = tokens[1]
				self.repo[name] = value
		return

	def	post_end_file( self, name = None ):
		self._end_repo()
		self.report()
		return

	def	report( self, final = False ):
		if final: return
		others = False
		for feed in sorted(
			self.repos,
			key = lambda f: f['_name'].lower()
		):
			if others:
				self.println()
			others = True
			self.println(
				'[{0}]'.format(
					feed['_name']
				)
			)
			self.println()
			fmt = ' {0:>%d} = {1}' % max(
				map(
					len,
					[ key for key in feed ]
				)
			)
			for key in sorted( feed ):
				if key[0] != '_':
					self.println(
						fmt.format(
							key,
							feed[key]
						)
					)
		return
