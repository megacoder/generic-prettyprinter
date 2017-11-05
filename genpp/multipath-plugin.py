#!/usr/bin/python
# vim: noet sw=4 ts=4

import	os
import	sys
import	string
import	superclass
import	shlex

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	NAME = 'multipath-pp'
	DESCRIPTION="""Display /etc/multipath.conf in conical style."""

	INDENT_WITH = ' ' * 8

	def __init__( self ):
		super( PrettyPrint, self ).__init__()
		return

	def	ignore( self, name ):
		ignore_it = False
		if os.path.isfile( name ) and not name.endswith( '.conf' ):
			ignore_it = True
		return

	def	_new_clause( self, name, parent = None ):
		return dict({
			'_name'   : name,
			'_parent' : parent,
		})

	def	pre_begin_file( self, name = None ):
		self.focus = self._new_clause( '_default' )
		return

	def	next_line( self, line ):
		tokens = [x for x in shlex.shlex( line )]
		if len(tokens) > 0:
			keyword = tokens[0]
			final   = tokens[-1]
			if keyword == '}':
				self.focus = self.focus[ '_parent' ]
			elif final == '{':
				child = self._new_clause(
					name = keyword,
					parent = self.focus
				)
				self.focus = child
			else:
				self.focus[ tokens[ 0 ] ] = tokens
		return

	def	report( self, final = False ):
		if not final:
			self._print_node( self.focus )
		else:
			pass
		return

	def	_print_line( self, v, depth ):
		indent = '        ' * depth
		s = '{0}\t{1}'.format(
			v[ 0 ],
			v[ 1: ] if len(v) else ''
		)
		print '{0}{1}'.format(
			indent,
			s,
		)
		return

	def	_print_node( self, node, depth = 0 ):
		width = max(
			map(
				len,
				node.keys()
			)
		)
		fmt = '{{0:{0}}}\t{{1}}'.format( width )
		for name in sorted( node ):
			v = node[ name ]
			if isinstance( v, dict ):
				print fmt.format(
					[ name, '{' ]
				)
				self._print_node( v, depth = depth + 1 )
				print fmt.format(
					[ '}', '' ]
				)
			else:
				v = node[ name ]
				self._print_line( v, depth )
		return
