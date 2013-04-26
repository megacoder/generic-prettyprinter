#!/usr/bin/python
# vim: sw=4 ts=4 noet

import	os
import	sys
import	stat
from	superclass	import	MetaPrettyPrinter

class	PrettyPrint( MetaPrettyPrinter ):

	NAME = 'o2cb-pp'
	DESCRIPTION = """Display Oracle OCFS2 O2CB configuration files in canonical format."""

	KEYWORDS = [
		'O2CB_BOOTCLUSTER',
		'O2CB_ENABLED',
		'O2CB_HEARTBEAT_THRESHOLD',
		'O2CB_IDLE_TIMEOUT_MS',
		'O2CB_KEEPALIVE_DELAY_MS',
		'O2CB_RECONNECT_DELAY_MS',
		'O2CB_STACK',
	]

	def	__init__( self ):
		super( PrettyPrint, self ).__init__()
		return

	def	reset( self ):
		super( PrettyPrint, self ).reset()
		self._setup()
		return

	def	_setup( self ):
		self.settings = {}
		self.max_name = 7
		return

	def	next_file( self, name ):
		super( PrettyPrint, self ).next_file( name )
		self._setup()
		return

	def	end_file( self, name ):
		self.report()
		self._setup()
		super( PrettyPrint, self ).end_file( name )
		return

	def	next_line( self, line ):
		line = line.split( '#', 1 )[0].strip()
		tokens = line.split( '=', 1 )
		if len(tokens) == 2:
			name  = tokens[0].strip()
			value = tokens[1].strip()
			self.max_name = max( self.max_name, len(name) )
			self.settings[name] = value
		return

	def	report( self, final = False ):
		fmt = '%%-%ds = %%s' % self.max_name
		for key in sorted( self.settings.keys() ):
			if not key in PrettyPrint.KEYWORDS:
				self.println(
					'# %S is not known to me; is it new?' % key
				)
			self.println( fmt % (key, self.settings[key]) )
		return
