#!/usr/bin/python
# vim: noet sw=4 ts=4

import	os
import	sys
import	string
import	superclass
import	re

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	NAME = 'pam'
	DESCRIPTION="""Display /etc/pam.d in conical style."""

	def __init__( self ):
		super( PrettyPrint, self ).__init__()
		self.rules = dict()
		return

	def	pre_begin_file( self, name = None ):
		self.rules    = dict()
		self.maxlen_g = 0
		self.maxlen_v = 0
		self.maxlen_t = 0
		self.maxlen_a = 0
		return

	def	next_line( self, line ):
		tokens = map(
			str.strip,
			line.split( '#', 1 )[0].split()
		)
		N = len( tokens )
		if N >= 3:
			group  = tokens[0]
			verb   = tokens[1]
			target = tokens[2]
			args   = '' if N == 3 else ' '.join( tokens[3:] )
			if group not in self.rules:
				self.rules[group] = []
			self.rules[group].append( (verb, target, args) )
			self.maxlen_g = max( self.maxlen_g, len( group  ) )
			self.maxlen_v = max( self.maxlen_v, len( verb   ) )
			self.maxlen_t = max( self.maxlen_v, len( target ) )
			self.maxlen_a = max( self.maxlen_a, len( args   ) )
		return

	def	report( self, final = False ):
		fmt = ' '.join([
			'{{0:{0}}}'.format( self.maxlen_g ),
			'{{1:{0}}}'.format( self.maxlen_v ),
			'{{2:{0}}}'.format( self.maxlen_t ),
			'{{3:{0}}}'.format( self.maxlen_a ),
		])
		last_group = None
		for group in sorted( self.rules ):
			for (n,d,a) in self.rules[group]:
				if group != last_group:
					self.println()
					last_group = group
				self.println(
					fmt.format(
						group,
						n,
						d,
						a
					)
				)
		self.rules = dict()
		return
