#!/usr/bin/python
# vim: noet sw=4 ts=4

import	ast
import	os
import	sys
import	sys
import	tokenize
import	StringIO
import	compiler

from	superclass	import	MetaPrettyPrinter

class	PythonPrettyPrint( object ):

	def __init__( self ):
		self.level	= 0
		self.was_op = False
		return

	def validate( self, s ):
		try:
			compiler.compile( s, s, 'exec' )
		except Exception, e:
			raise e
		return

	def run( self, spelling, rule = 'p' ):
		for action in rule:
			# print '[{0}]'.format( action ),
			if action == 'i':
				self.level += 1
			elif action == 'd':
				self.level -= 1
			elif action == 'n':
				yield '\n'
			elif action == 'r':
				yield '{0}'.format( '  ' * self.level )
			elif action == 'p':
				yield '{0}'.format( spelling )
			else:
				print >>self.stdout, 'Internal error: action %s' % action
		return

	def parse( self, s ):
		default_rule = 'rp'
		for toknum,spelling,(srow,scol),(erow,ecol),logicalline in tokenize.generate_tokens( StringIO.StringIO(s).readline):
			rule = default_rule
			default_rule = None
			# What do we have?
			if toknum == tokenize.OP:
				if spelling == '[':
					rule = 'pin'
					default_rule = 'rp'
				elif spelling == ']':
					rule = 'dnp'
				elif spelling == ',' or spelling == ';':
					rule = 'p'
					default_rule = 'nrp'
				else:
					if self.was_op:
						spelling = '{0} '.format( spelling )
					else:
						spelling = ' {0} '.format( spelling )
					rule = 'p'
					default_rule = 'p'
				self.was_op = True
			else:
				self.was_op = False
				default_rule = 'p'
			# Take the actions for this token
			for line in self.run( spelling, rule  ):
				yield line
			if not default_rule:
				default_rule = 'rp'
		yield '\n'
		return

class	PrettyPrint( MetaPrettyPrinter ):

	NAME = 'vmcfg'
	DESCRIPTION = """Display vm.cfg files in canonical style."""

	def __init__( self ):
		super( PrettyPrint, self ).__init__()
		self.pp = PythonPrettyPrint()
		self.pre_begin_file()
		return

	def	pre_begin_file( self, name = None ):
		self.lines = []
		self.width = 7
		return

	def next_line( self, line ):
		tokens = map(
			str.strip,
			line.split( '#', 1 )[0].split( '=', 1 )
		)
		if len(tokens) == 2:
			try:
				name = tokens[0]
				value = tokens[1]
				# print '|%s|%s|' % (name,value)
				self.pp.validate( value )
				# print 'Looks good'
			except Exception, e:
				self.error( 'syntax error: %s' % line )
				return
			self.width = max( self.width, len( name ) )
			self.lines.append(
				[ name, value ]
			)
		return

	def report( self, final = False ):
		if not final:
			fmt = '{0:%ds} = {1}' % self.width
			indent = '\n' + (' ' * (self.width + 3))
			first = True
			for [name, value] in sorted(
				self.lines,
				key = lambda a : a[0].lower()
			):
				first = True
				layout = fmt
				for text in self.pp.parse( value ):
					if first:
						line = fmt.format( name, text )
						first = False
					else:
						line += text
				lines = line.split( '\n' )
				lines = indent.join( lines )
				self.println( lines.rstrip() )
		return
