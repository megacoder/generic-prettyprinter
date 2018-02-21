#!/usr/bin/python
# vim: noet sw=4 ts=4

import	bunch
import	os
import	shlex
import	superclass
import	sys

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	NAME        = 'apache-pp'
	DESCRIPTION = """Print apache-style configuration files."""

	PLAIN = [ 'info', 'deviceuri' ]

	def	__init__( self ):
		super(PrettyPrint, self).__init__()
		self.lines = list()
		return

	def	next_line( self, line ):
		tokens = [
			t for t in shlex.split( line, posix = True, comments = True )
		]
		if len(tokens):
			# print 'tokens={0}'.format( tokens )
			self.lines.append(
				(
					# self.get_filename(),
					# self.get_lineno(),
					'{stdin}',
					0,
					tokens
				)
			)
		return

	def	new_node( self, name = None, tokens = list() ):
		return bunch.Bunch(
			name     = name,
			tokens   = tokens,
			attrs    = list(),
			children = list(),
		)

	def	parse_stored_lines( self ):
		stack = list()
		stack.append( self.new_node() )
		tree = node = stack[ -1 ]
		if False:
			self.dump_node( node, 'Top Of The Stack' )
		for filename, lineno, tokens in self.lines:
			if tokens[ 0 ].startswith( '</' ):
				# Close the current node
				if len(stack) == 1:
					break
				stack.pop()
				node = stack[ -1 ]
			elif tokens[ 0 ].startswith( '<' ):
				# Drop angle brackets fore and aft
				tokens[ 0 ]  = tokens[0][ 1: ]
				tokens[ -1 ] = tokens[-1][ :-1 ]
				# Open a new node
				child = self.new_node(
					name   = tokens[ 0 ],
					tokens = tokens,
				)
				node.children.append( child )
				if False:
					self.dump_node( node, 'New child' )
				stack.append( child )
				node = stack[ -1 ]
			else:
				node.attrs.append( tokens )
		return tree

	def	dump_node( self, node, title = None ):
		if title:
			self.println()
			self.println( title )
			self.println( '-' * len( title ) )
			self.println()
		self.println(
			'Node {0}'.format( node.name if node.name else '{top}' )
		)
		self.println( 'tokens={0}'.format( node.tokens ) )
		self.println( 'attrs={0}'.format( node.attrs ) )
		self.println( 'children={0}'.format( node.children ) )
		return

	def	quote_item( self, item ):
		quote = False
		for p in [ ' ', '*', '|', '(', ')' ]:
			if p in item:
				quote = True
				break
		return '"{0}"'.format( item ) if quote else item

	def	do_print_node( self, node, indent = 0 ):
		if False:
			self.dump_node( node, 'About To Print' )
		gutter = '  '
		if node.name:
			self.println(
				'{0}<{1}>'.format(
					gutter * indent,
					' '.join(
						self.quote_item( t ) for t in node.tokens
					)
				)
			)
			indent += 1
		if len( node.attrs ):
			width = max(
				map(
					lambda a : len( a[ 0 ] ),
					node.attrs
				)
			)
			fmt = '{{0:{0}}}  {{1}}'.format(
				width
			)
			for attrs in sorted( node.attrs ):
				args = ' '.join(
					[
						self.quote_item( a ) for a in attrs
					]
				)
				self.println(
					'{0}{1}'.format(
						gutter * indent,
						fmt.format(
							attrs[0],
							args,
						)
					)
				)
		# Do nodes we contain
		if len( node.children ):
			for child in sorted( node.children ):
				self.do_print_node( child, indent )
		if node.name:
			indent -= 1
			self.println(
				'{0}</{1}>'.format( gutter * indent, node.name )
			)
		return

	def	display_tree( self, tree ):
		self.do_print_node(
			tree
		)
		return

	def	report( self, final = False ):
		if not final: return
		tree = self.parse_stored_lines()
		self.display_tree( tree )
		return

if __name__ == '__main__':
	if sys.stdin.isatty():
		def	another():
			return raw_input( '> ' )
	else:
		def	another():
			return raw_input()
	pp = PrettyPrint()
	while True:
		try:
			line = another()
		except:
			break
		pp.next_line( line.rstrip() )
	pp.report( final = True )
	exit( 0 )
