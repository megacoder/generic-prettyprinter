#!/usr/bin/python
# vim: noet sw=4 ts=4

import	os
import	sys
import	string
import	superclass

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	NAME = 'lvm'
	DESCRIPTION = """Display LVM configuration files in a canonical form."""

	def __init__( self ):
		super( PrettyPrint, self ).__init__()
		return

	def	reset( self ):
		super( PrettyPrint, self ).reset()
		self.begins_with = None
		self.ends_with   = None
		self.max_name    = 15
		self.stanza      = []
		self.stanzas     = []
		return

	def	dump_stanza( self, beginning, content, ending ):
		fmt = '%%%ds = %%s' % self.max_name
		content.sort()
		print '\t'.join(beginning)
		for tokens in content:
			print fmt % ( tokens[0], ' '.join( tokens[1:] ) )
		print '\t'.join(ending)
		return

	def	finish_stanza( self, beginning, content, ending ):
		self.stanzas.append( (beginning, content, ending) )
		return

	def	next_line( self, line ):
		line = line.strip()
		if line.startswith( '#' ):
			print line
			return
		# All other lines are to be correctly indented
		if line.find( '{' ) > -1:
			self.begins_with = line.rstrip().replace( '{', ' { ' ).replace( '}', ' } ' ).split()
			self.stanza = []
		elif line.find( '}' ) > -1:
			self.ends_with = line.rstrip().replace( '{', ' { ' ).replace( '}', ' } ' ).split()
			self.finish_stanza( self.begins_with, self.stanza, self.ends_with )
		else:
			tokens = line.rstrip().split( '=', 1 )
			if len(tokens) == 2:
				self.max_name = max( self.max_name, len(tokens[0]) )
				self.stanza.append( tokens )
		return

	def	finish( self ):
		if len(self.stanzas) > 0:
			self.stanzas.sort()
			for (beginning,content,ending) in self.stanzas:
				self.dump_stanza( beginning, content, ending )
		return
