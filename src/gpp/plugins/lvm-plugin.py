#!/usr/bin/python
# vim: noet sw=4 ts=4

import	os
import	sys
import	string
import	superclass

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	NAME = 'lvm-pp'
	DESCRIPTION = """Display LVM configuration files in a canonical form."""

	INDENT_WITH = '        '

	def __init__( self ):
		super( PrettyPrint, self ).__init__()
		return

	def	reset( self ):
		super( PrettyPrint, self ).reset()
		self.stanza = []
		self.max_name = 15
		return

	def	dump_stanza( self ):
		fmt = '%%%ds = %%s' % self.max_name
		self.stanza.sort()
		for tokens in self.stanza:
			print fmt % ( tokens[0], ' '.join( tokens[1:] ) )
		self.reset()
		return

	def	next_line( self, line ):
		# Column-1 comments are copied verbatim
		if line.lstrip().startswith( '#' ):
			print line
			return
		# All other lines are to be correctly indented
		if line.find( '{' ) > -1:
			l = line.rstrip().replace( '{', ' { ' ).replace( '}', ' } ' )
			tokens = l.split()
			print '\t'.join( tokens )
			# Dump any cruft from a partially-completed stanza
			self.reset()
		elif line.find( '}' ) > -1:
			self.dump_stanza()
			l = line.rstrip().replace( '{', ' { ' ).replace( '}', ' } ' )
			tokens = l.split()
			print '\t'.join( tokens )
		else:
			tokens = line.rstrip().split( '=' )
			if len(tokens) != 2:
				print line,
				return
			self.max_name = max( self.max_name, len(tokens[0]) )
			self.stanza.append( tokens )
		return

	def	finish( self ):
		self.dump_stanza()
		return
