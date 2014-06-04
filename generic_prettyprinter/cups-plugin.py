#!/usr/bin/python
# vim: noet sw=4 ts=4

import	os
import	sys
import	string
import	superclass

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	INDENT = 1
	WIDTH  = 15

	NAME = 'cups'
	DESCRIPTION="""Display /etc/cups/cups.conf and friends in conical style."""

	def __init__( self ):
		super( PrettyPrint, self ).__init__()
		return

	def	reset( self ):
		super( PrettyPrint, self ).reset()
		self._prepare()
		return

	def	_prepare( self ):
		self.nodecnt = 0
		self.nodes = []
		self.focus	 = None	# This is not a dup assignment!
		self.focus   = self._new_node()
		return

	def	_new_node( self, content = [], header = None, footer = None ):
		node = {
			'id'       : self.nodecnt,
			'parent'   : self.focus,
			'content'  : [],
			'header'   : header,
			'footer'   : footer
		}
		self.nodes.append( node )
		self.nodecnt += 1
		return node['id']

	def	next_line( self, line ):
		line = line.split( '#', 1 )[0].strip()
		tokens = line.split()
		n = len( tokens )
		if n > 0:
			name = tokens[0]
			if name.startswith( '</' ):
				# Close stanza
				self.nodes[self.focus]['footer'] = tokens
				self.focus = self.nodes[self.focus]['parent']
			elif name.startswith( '<' ):
				# Open stanza
				tokens[-1] = tokens[-1][:-1]	# Remove closing '>'
				header = [ tokens[0] ] + sorted( tokens[1:] )
				header[-1] = header[-1] + '>'
				id = self._new_node( header = header )
				self.nodes[ self.focus ]['content'].append( id )
				self.focus = id
			else:
				# Append tokens to current stanza
				self.nodes[ self.focus ]['content'].append( tokens )
		return

	def	_show_node( self, focus = 0, indent = 0 ):
		# print 'show node %d\n%s' % ( focus, self.nodes[focus] )
		width = PrettyPrint.WIDTH - 1
		for obj in self.nodes[focus]['content']:
			if type(obj) == list:
				width = max( width, len(obj[0]) )
		sorted_content = sorted(self.nodes[focus]['content'])
		# First pass gets plain entries only
		leadin = ' ' * indent
		fmt = '%%-%ds %%s' % width
		for obj in sorted_content:
			if type(obj) == list:
				# This is a list of tokens
				line = fmt % (
					obj[0],
					' '.join( obj[1:] )
				)
				print '%s%s' % ( leadin, line )
		# The second pass gets any children
		for obj in sorted_content:
			if type(obj) == int:
				# This is a node
				header = self.nodes[obj]['header']
				if header:
					fmt = '%%-%ds %%s' % PrettyPrint.WIDTH
					line = fmt % (
						header[0],
						' '.join( header[1:] )
					)
					print '%s%s' % ( leadin, line )
				self._show_node(
					focus = obj,
					indent = indent + PrettyPrint.INDENT
				)
				if self.nodes[obj]['footer']:
					print '%s%s' % ( leadin, ' '.join( self.nodes[ obj ]['footer']) )
		return

	def	begin_file( self, name ):
		super( PrettyPrint, self ).begin_file( name )
		self._prepare()
		return

	def	end_file( self, name ):
		self._show_node()
		self._prepare()
		super( PrettyPrint, self ).end_file( name )
		return
