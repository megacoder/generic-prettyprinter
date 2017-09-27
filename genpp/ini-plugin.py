#!/usr/bin/python
# vim: noet sw=4 ts=4

import	os
import	sys
import	superclass
import	shlex

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	NAME = 'ini-pp'
	DESCRIPTION = """Display [ini] files in canonical style."""

	def	__init__( self ):
		super( PrettyPrint, self ).__init__()
		return

	def	pre_begin_file( self, fn = None ):
		self.section_name = None
		self.entries      = dict()
		self.sections     = dict()
		return

	def	next_line( self, line ):
		# Ignore funky comment lines
		if len(line) == 0 or line[0] in [ '#', ';' ]: return
		if line.startswith( '[' ):
			if self.section_name and len(self.entries):
				self.sections[ self.section_name ] = self.entries
			self.section_name = line
			self.entries = dict()
		else:
			tokens = map(
				str.strip,
				line.strip().split( '=' )
			)
			if len( tokens ) == 2:
				self.entries[ tokens[0] ] = tokens
		return

	def	post_end_file( self, name = None ):
		if self.section_name and len(self.entries):
			self.sections[ self.section_name ] = self.entries
		super( PrettyPrint, self ).post_end_file( name )
		return

	def	report( self, final = False ):
		if not final:
			others = False
			for key in sorted(
				self.sections,
				key = lambda k : k.lower()
			):
				name = key
				if others:
					self.println()
				self.println( name )
				others = True
				#
				width = max(
					map(
						len,
						self.sections[ key ]
					)
				)
				fmt = '{{0:>{0}}} = {{1}}'.format( width )
				for item in sorted(
					self.sections[key],
					key = lambda k : k.lower()
				):
					details = self.sections[key][item]
					self.println(
						fmt.format(
							details[0],
							' '.join( details[1:] )
						)
					)
		return
