#!/usr/bin/python
# vim: noet sw=4 ts=4

import	pprint
import	sys
from	superclass	import	MetaPrettyPrinter

class	PrettyPrint( MetaPrettyPrinter ):

	NAME = 'vmcfg'
	DESCRIPTION = """Display vm.cfg files in canonical style."""

	def __init__( self ):
		super( PrettyPrint, self ).__init__()
		return

	def pre_begin_file( self ):
		self.filename = None
		self.stanzas  = []
		self.stanza   = dict()
		self.name	  = None		# Name of acive stanza
		return

	def compile( self, script ):
		if len( script ) > 0:
			try:
				code = compile( script, self.filename, 'exec' )
			except Exception, e:
				self.error( 'File "%s" appears to be corrupt.' % self.filename )
				self.error( e )
				return None
			locals = dict()
			globals = dict()
			try:
				eval( code, globals, locals )
			except Exception, e:
				self.error( 'Could not evaluate code' )
				self.error( ' %s' % e )
				return
		return

	def begin_file( self, name ):
		super( PrettyPrint, self ).begin_file( name )
		self.filename = name
		return

	def	_start_stanza( self, name ):
		self.name = name
		self.stanza = dict()
		return

	def	_add_entry( self, name, value ):
		self.stanza[name] = value
		return

	def	_end_stanza( self ):
		self.stanzas.append(
			[ self.name, self.stanza ]
		)
		self.name	= None
		self.stanza = None
		return

	def	_in_stanza( self ):
		return True if self.name else False

	def next_line( self, line ):
		c = line[0]
		print 'c ::= "%s"' % c
		if not c.isspace():
			# name {
			if self._in_stanza():
				self.error(
					'stanza "{0}" not terminated'.format( self.name )
				)
				self._end_stanza()
			tokens = map(
				str.strip,
				line.split()
			)
			if len( tokens ) == 2 and tokens[1] == '{':
				self.name = tokens[0]
				self.stanza = dict()
				# print 'Beginning section %s' % self.name
		elif c == '}':
			# }
			try:
				if not self._in_stanza():
					self.error( 'misplaced "}"' )
				else:
					# print 'Ending section %s' % self.name
					self.println( self.stanza )
					self._end_stanza()
			except Exception, e:
				self.error( e )
		elif c.isspace():
			if not self._in_stanza():
				self.error( 'orphan name' )
			else:
				tokens = map(
					str.strip,
					line.split( '=', 1 )
				)
				print 'tokens = %s' % tokens
				if len( tokens ) == 2 and len(tokens[0]) > 0:
					try:
						code = eval( tokens[1] )
						self._add_entry( tokens[0], code )
					except Exception, e:
						self.error(
							'syntax error in value "{}"',format(
								tokens[1]
							)
						)
		else:
			self.error( '# {0}'.format( line ) )
		return

	def report( self, final = False ):
		if not final and len( self.stanzas ) > 0:
			for [name,stanza] in sorted(
				self.stanzas
			):
				self.println( "%s\t{" % name )
				width = max(
					map(
						len,
						stanza.keys()
					)
				)
				fmt = '  {0:<%d.%ds} {1} {2}' % (
					width,
					width
				)
				for key in sorted(
					stanza.keys(),
					key = lambda s : s.upper()
				):
					s    = pprint.PrettyPrinter().pformat( stanza[key] )
					name = key
					op   = '='
					for line in s.split( '\n' ):
						self.println(
							fmt.format(
								name,
								op,
								line
							)
						)
						name = ''
						op = ''
				self.println( '}' )
		return
