#!/usr/bin/python
# vim: ts=4 sw=4 noet
# Print /etc/sysconfig/oracleasm in a canonical style.

import	os
import	sys
import	superclass
import	shlex

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	NAME = 'asm'
	DESCRIPTION = """Display /etc/sysconfig/oracleasm files in canonical style."""
	NAMES = dict(
		ORACLEASM_ENABLED                = None,
		ORACLEASM_GID                    = None,
		ORACLEASM_SCANBOOT               = None,
		ORACLEASM_SCANEXCLUDE            = None,
		ORACLEASM_SCANORDER              = None,
		ORACLEASM_UID                    = None,
		ORACLEASM_USE_LOGICAL_BLOCK_SIZE = None,
	)

	def __init__( self ):
		super( PrettyPrint, self ).__init__()
		return

	def	pre_begin_file( self, fn ):
		self.used = {}
		return

	def next_line( self, line ):
		tokens = [ x for x in shlex.shlex( line ) ]
		n = len( tokens )
		if n == 2:
			tokens.append( ' # default' )
			n += 1
		if n == 3 and tokens[1] == '=':
			name			= tokens[0]
			value			= tokens[2]
			self.used[name] = value
		return

	def report( self, final = False ):
		if not final:
			for key in sorted( self.used ):
				if not key in PrettyPrint.NAMES:
					footnote = self.footnote(
						'Warning: "{0}" may not be spelled correctly.'.format(
							key
						)
					)
				else:
					footnote = None
				self.println( '{0}={1}{2}'.format(
						key,
						self.used[key],
						'\t*** See footnote {0}'.format(footnote) if footnote else ''
					)
				)
		return

