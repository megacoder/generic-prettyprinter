#!/usr/bin/python

import	os
import	sys
import	superclass

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	NAME = 'rpm-vt-pp'
	DESCRIPTION = """Display 'rpm -Va' output in canonical style."""

	STATES = [
		'Size',
		'Mode',
		'MD5',
		'Devno',
		'Link',
		'UID',
		'GID',
		'MTIME',
		'Capabilities'
	]

	FORMATS = {
		'c': '%config',
		'd': '%doc',
		'g': '%ghost',
		'l': '%license',
		'r': '%readme'
	}

	def	__init__( self ):
		super( PrettyPrint, self ).__init__()
		self.fmt = '%%-%ds  %%-%ds  %%-%ds  %%s' % (
			len( PrettyPrint.STATES ),
			1,
			48
		)
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
		comment = '['
		if state != 'missing':
			for i in xrange( 0, len(PrettyPrint.STATES) ):
				if state[i] != '.':
					comment += ':' + PrettyPrint.STATES[i]
		for c in flags:
			if c in PrettyPrint.FORMATS:
				comment += ':' + PrettyPrint.FORMATS[c]
		comment += ':]'
		self.println( self.fmt % (state, flags, name, comment) )
