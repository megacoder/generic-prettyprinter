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
		return

	def	pre_begin_file( self ):
		super( PrettyPrint, self ).pre_begin_file()
		self.repos = []
		self._new_repo()
		return

	def	_new_repo( self, name = None ):
		self.repo = {}
		self.repo['#name'] = name
		return

	def	ignore( self, fn ):
		return not fn.endswith( '.repo' )

	def	_add_repo( self ):
		name = self.repo['#name']
		if name is not None:
			self.repos.append( (name, self.repo) )
		return

	def	next_line( self, line ):
		if line.startswith( '[' ):
			self._add_repo()
			self._new_repo( line.strip()[1:-1] )
		else:
			tokens = line.split( '#', 1 )[0].split( '=', 1 )
			if len(tokens) == 2:
				name = tokens[0].strip()
				value = tokens[1].strip()
				self.repo[name] = value
		return

	def	report( self, final = False ):
		if not final:
			self._add_repo()
			for (name,feed) in sorted(
				self.repos,
				key = lambda (n,f): n.lower()
			):
				self.println(
					'[{0}]'.format(
						name
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
					if not key[0] == '#':
						self.println(
							fmt.format(
								key,
								feed[key]
							)
						)
				self.println()
		return
