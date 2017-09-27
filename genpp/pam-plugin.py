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

	GUTTER = ' '

	def __init__( self ):
		super( PrettyPrint, self ).__init__()
		self.rules = dict()
		return

	def	pre_begin_file( self, name = None ):
		self.rules  = dict()
		self.widths = dict()
		return

	def	_parse( self, s ):
		resid = s
		token = None
		state = 'begin'
		while len(resid):
			c = resid[ 0 ]
			if c.isspace():
				if state == 'append':
					# Do not append whitespace to token
					resid = resid[1:]
					break
				if state == 'bracket':
					# Do append whitespace to token
					token += c
					resid = resid[1:]
					break
				# Fall through to ignore space
			# Not a whitespace character
			if state == 'begin':
				token = c
				state = 'append'
			elif state == 'append':
				token += c
			elif c == '[':
				state = 'bracket'
				token = c
			elif c == ']' and state == 'bracket':
				token += c
				resid = resid[1:]
				break
			resid = resid[1:]
		return token, resid

	def	next_line( self, line ):
		tokens = map(
			str.strip,
			line.split( '#', 1 )[0].split()
		)
		L = len( tokens )
		if L >= 3:
			group  = tokens[0]
			apply  = tokens[1]
			dll    = tokens[2]
			if L == 3:
				args = ''
			else:
				args   = ' '.join( tokens[3:] )
			tokens = [ group, apply, dll, args ]
			key = group[1:] if group.startswith( '-' ) else group
			# Want maximum widths of fields
			for i in range( len( tokens ) ):
				self.widths[i] = max(
					self.widths.get( i, 0 ),
					len( tokens[i] )
				)
			# Append this group of tokens to our list
			if key not in self.rules:
				self.rules[ key ] = []
			self.rules[ key ].append( tokens )
		return

	def	report( self, final = False ):
		if not final:
			fmts = [
				'{{0:<{0}}}'.format(self.widths[i]) for i in self.widths
			]
			for key in sorted(
				self.rules,
				key = lambda s : s.lower()
			):
				self.println()
				for tokens in self.rules[ key ]:
					self.println(
						PrettyPrint.GUTTER.join([
							fmts[i].format( tokens[i] )
								for i in range( len( tokens ) )
						])
					)
		return
