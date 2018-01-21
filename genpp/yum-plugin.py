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
		self.pre_begin_file()
		return

	def	ignore( self, fn ):
		return not fn.endswith( '.repo' )

	def	pre_begin_file( self, name = None ):
		self.repos   = dict()
		self.channel = '[ORPHAN]'
		return

	def	next_line( self, line ):
		if line.startswith( '[' ):
			self.channel = line.strip()
		else:
			tokens = map(
				str.strip,
				line.split( '#', 1 )[0].split( '=', 1 )
			)
			if len(tokens) == 2:
				name  = tokens[0]
				value = tokens[1]
				self.repos[ self.channel ] = self.repos.get(
					self.channel,
					list()
				) + [ (name, value) ]
		return

	def	report( self, final = False ):
		if final: return
		# Find the longest repo attribute amongst all those
		# defined in this file.
		width = max( max(
			map(
				lambda l : map(
					lambda (n,v) : len(n),
					l
				),
				[ self.repos[key] for key in self.repos.keys() ]
			)
		))
		fmt = ' {{0:>{0}}} = {{1}}'.format( width )
		others = False
		for channel in sorted( self.repos, key = lambda k : k.lower() ):
			if others:
				self.println()
			others = True
			self.println( '{0}'.format( channel ) )
			self.println()
			for (n,v) in sorted(
				self.repos[channel],
				key = lambda (n,v) : n.lower()
			):
				self.println(
					fmt.format( n, v )
				)
		return
