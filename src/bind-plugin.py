#!/usr/bin/python
# vim: noet sw=4 ts=4

import	os
import	sys
import	string
import	superclass

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	NAME = 'bind-pp'
	DESCRIPTION="""Display /etc/named.conf and friends in conical style."""

	def __init__( self ):
		super( PrettyPrint, self ).__init__()
		return

	def	reset( self ):
		super( PrettyPrint, self ).reset()
		self._prepare()
		return

	def	_prepare( self ):
		self.nodes    = []
		self.node_cnt = 0
		self.focus    = self._new_node()
		return

	def	_new_node(
		self,
		content = [],
		parent  = 0,
		child   = 0
	):
		self.nodes.append(
			{
				'content': content,
				'parent': parent,
				'child': child
			}
		)
		n = self.node_cnt
		self.node_cnt += 1
		return n

	def	_do_token( self, token ):
		if token is ';':
			self.nodes[ self.focus ]['content'] += [ token ]
		elif token is '{':
			self.nodes[ self.focus ]['content'] += [ token ]
			self.nodes[ self.focus ]['child'] = self._new_node(
				parent = self.focus
			)
		elif token is '}':
			self.focus = self.nodes[ self.focus ]['parent']
			self.nodes[ self.focus ]['content'] += [ token ]
		else:
			self.nodes[ self.focus ]['content'] += [ token ]
		return

	def	next_line( self, line ):
		line = line.split( '#', 1 )[0].strip()
		# Ignore blank lines
		if line == "": return
		# Ensure that magic tokens are whitespace-delimited
		line = line.replace( '{', ' { ' )
		line = line.replace( '}', ' } ' )
		line = line.replace( ';', ' ; ' )
		for token in line.split():
			self._do_token( token )
		return

	def	_report( self, focus = None, indent = 0 ):
		if not focus:
			focus = self.focus
		for node in self.nodes[ focus ]:
			for key in sorted( node ):
				print key
		return
		print '%s%s' % (
			' ' * indent,
			'X'.join( self.nodes[ focus ]['content'] )
		)
		if self.nodes[ focus ]['child']:
			self._report( self.nodes[ focus ]['child'], indent = indent + 8 )
		return

	def	report( self, final = False ):
		self._report( 0 )
		return

	def	begin_file( self, name ):
		super( PrettyPrint, self ).begin_file( name )
		self._prepare()
		return

	def	end_file( self, name ):
		self._prepare()
		super( PrettyPrint, self ).end_file( name )
		return
