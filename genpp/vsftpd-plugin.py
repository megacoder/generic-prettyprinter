#!/usr/bin/python
# vim: noet sw=4 ts=4

import	os
import	sys
import	superclass
import	shlex

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	NAME        = 'vsftpd'
	DESCRIPTION = """Display /etc/vsftpd.conf in style."""

	def	__init__( self ):
		super( PrettyPrint, self ).__init__()
		self.pre_begin_file()
		return

	def	ignore( self, fn ):
		return not fn.endswith( '.conf' )

	def	pre_begin_file( self, name = None ):
		self.pairs = dict()
		return

	def	next_line( self, line ):
		tokens = [ token for token in shlex.shlex( line, posix = True ) ]
		if len(tokens) == 3 and tokens[ 1 ] == '=':
			self.pairs[ tokens[ 0 ] ] = tokens[ 2 ]
		return

	def	report( self, final = False ):
		if final: return
		width = max(
			map(
				len,
				self.pairs
			)
		)
		fmt = ' {{0:>{0}}} = {{1}}'.format( width )
		for key in sorted( self.pairs.keys() ):
			self.println( fmt.format( key, self.pairs[ key ] ) )
		return
