#!/usr/bin/python
# vim: sw=4 ts=4 noet

import	os
import	sys
import	stat
from	superclass	import	MetaPrettyPrinter

class	PrettyPrint( MetaPrettyPrinter ):

	NAME = 'o2cb-pp'
	DESCRIPTION = """Display Oracle OCFS2 O2CB configuration files in canonical format."""

	KEYWORDS = dict(
		O2CB_BOOTCLUSTER         = None,
		O2CB_ENABLED             = None,
		O2CB_HEARTBEAT_THRESHOLD = None,
		O2CB_IDLE_TIMEOUT_MS     = None,
		O2CB_KEEPALIVE_DELAY_MS  = None,
		O2CB_RECONNECT_DELAY_MS  = None,
		O2CB_STACK               = None,
	)

	def	__init__( self ):
		super( PrettyPrint, self ).__init__()
		self.settings = dict()
		return

	def	pre_begin_file( self, name  ):
		self.settings = dict()
		self.max_name = 7
		return

	def	next_line( self, line ):
		tokens = map(
			str.strip,
			# Drop comments, then split remainder by equal sign
			line.split( '#', 1 )[0].split( '=', 1 )
		)
		if len(tokens) == 2:
			name  = tokens[0]
			value = tokens[1]
			self.max_name = max( self.max_name, len(name) )
			self.settings[name] = value
		return

	def	report( self, final = False ):
		if not final:
			fmt = '{{0:>{0}}} = {{1}}'.format( self.max_name )
			for key in sorted( self.settings ):
				value = self.settings[ key ]
				quote = "'" if "'" not in value else '"'
				value = quote + value + quote
				if not key in PrettyPrint.KEYWORDS:
					footnote = self.footnote(
						'"{0}" is not known to me; is it new?'.format(
							key
						)
					)
					value += ' # {0}'.format( footnote )
				self.println(
					fmt.format(
						key,
						value
					)
				)
		return
