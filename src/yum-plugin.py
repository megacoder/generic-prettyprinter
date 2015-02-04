#!/usr/bin/python
# vim: noet sw=4 ts=4

import	os
import	sys
import	superclass
import	shlex

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	NAME        = 'yum.repo'
	DESCRIPTION = """Display /etc/yum.repos.d/*.repo files in style."""

	def	__init__( self ):
		super( PrettyPrint, self ).__init__()
		return

	def	pre_begin_file( self ):
		self.feeds = []
		self._new_repo()
		return

	def	_new_repo( self, name = None ):
		self.feed = {}
		self.feed['#name'] = name
		return

	def	ignore( self, fn ):
		return not fn.endswith( '.repo' )

	def	add_repo( self ):
		name = self.feed['#name']
		if name is not None:
			self.feeds.append( (name, self.feed) )
		return

	def	next_line( self, line ):
		if line.startswith( '[' ):
			self.add_repo()
			self._new_repo( line.strip()[1:-1] )
		else:
			tokens = [ x for x in shlex.shlex( line ) ]
			if len(tokens) == 3 and tokens[1] == '=':
				name = tokens[0]
				value = tokens[2]
				self.feed[name] = value
		return

	def	report( self, final = False ):
		if not final:
			self.add_repo()
			first = True
			for (name,feed) in sorted(
				self.feeds,
				key = lambda f: f['#name'].lower()
			):
				if first:
					self.println()
					first = False
				self.println(
					'[{0}]'.format(
						name
					)
				)
				self.println()
				fmt = ' {0:>%d} = {1}' % max(
					map(
						str.len,
						[ key for key in feed ]
					)
				)
				for key in sorted( feed.keys() ):
					self.println(
						fmt,
						key,
						feed[key]
					)
		return
