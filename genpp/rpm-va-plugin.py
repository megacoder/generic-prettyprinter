#!/usr/bin/python
# vim: noet sw=4 ts=4

import	os
import	sys
import	superclass

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	NAME = 'rpm-vt-pp'
	DESCRIPTION = """Display 'rpm -Va' output in canonical style."""

	GLOB = '-'

	STATES = {
		'S': 'Size',
		'M': 'Mode',
		'5': 'MD5',
		'D': 'Devno',
		'L': 'Link',
		'U': 'UID',
		'G': 'GID',
		'T': 'MTIME',
		'P': 'Capabilities'
	}

	FORMATS = {
		'c': '%config',
		'd': '%doc',
		'g': '%ghost',
		'l': '%license',
		'r': '%readme'
	}

	def	__init__( self ):
		super( PrettyPrint, self ).__init__()
		return

	def start( self ):
		self.fmt = '%%-%ds	%%-%ds	%%-%ds	%%s' % (
			len( PrettyPrint.STATES ),
			1,
			48
		)
		self.lines = []
		return

	def	begin_file( self, name ):
		# Avoid printing per-file header
		return

	def	next_line( self, line ):
		tokens = line.split()
		if len(tokens) == 2:
			# Dummy up middle colum if no format characters
			tokens.insert( 1, '' )
		if len(tokens) == 3:
			state = tokens[0]
			flags = tokens[1]
			name  = tokens[2]
			self._process( state, flags, name )
		return

	def	_process( self, state, flags, name ):
		comment = ''
		sep = ''
		if state != 'missing':
			for c in state:
				if c in PrettyPrint.STATES:
					comment += sep + PrettyPrint.STATES[c]
					sep = ' '
		for c in flags:
			if c in PrettyPrint.FORMATS:
				comment += sep + PrettyPrint.FORMATS[c]
				sep = ' '
		self.lines.append( [state, flags, name, comment] )

	def	report( self, final = False ):
		if final:
			self.lines.sort( key = lambda t: t[2] )
			for [state, flags, name, comment] in self.lines:
				self.println( self.fmt % (state, flags, name, comment) )
