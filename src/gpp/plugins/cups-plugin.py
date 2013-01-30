#!/usr/bin/python
# vim: noet sw=4 ts=4

import	os
import	sys
import	string
import	superclass

class	PrettyPrint( superclass.MetaPrettyPrinter ):

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
		leadin = ' ' * indent
		header = self.nodes[focus]['header']
		if header:
			line = '%-15s %s' % (
				header[0],
				' '.join( header[1:] )
			)
			print '%s%s' % ( leadin, line )
		if focus > 0:
			contleadin = leadin + ' '
		else:
			contleadin = leadin
		width = 14
		for obj in self.nodes[focus]['content']:
			if type(obj) == list:
				width = max( width, len(obj[0]) )
		fmt = '%%-%ds %%s' % width
		for obj in sorted(self.nodes[focus]['content']):
			if type(obj) == int:
				# This is a node
				self._show_node( focus = obj, indent = indent + 8 )
			elif type(obj) == list:
				# This is a list of tokens
				line = fmt % (
					obj[0],
					' '.join( obj[1:] )
				)
				print '%s%s' % ( contleadin, line )
			else:
				# WTF?
				print 'huh? %s' % obj
		if self.nodes[focus]['footer']:
			print '%s%s' % ( leadin, ' '.join( self.nodes[ focus ]['footer']) )
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
