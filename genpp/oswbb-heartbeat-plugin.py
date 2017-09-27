#!/usr/bin/python
# vim: noet sw=4 ts=4
#
# FYI: Currently, the OSWbb heartbeat file is generated like this:
#	$ date '+oswbb hearbeat %a %b %d %H:%M:%S %Y'
# But this is subject to change at any time.

import	datetime
import	os
import	sys
import	superclass
import	oswticker

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	NAME = 'oswbb-hearbeat-pp'
	DESCRIPTION="""Display OSWBB's heartbeat file, highlighting jitter."""

	def	__init__( self ):
		super( PrettyPrint, self ).__init__()
		return

	def	begin_file( self, fn ):
		super( PrettyPrint, self ).begin_file()
		self.ot = oswticker.OswTicker( '%a %b %d %H:%M:%S %Y' )
		self.println(
			'#  Day Mon Dy HH:MM:SS YYYY  Delta'
		)
		self.println(
			'#  --- --- -- -------- ---- -------'
		)
		return

	def	next_line( s ):
		if line.startswith( 'oswbb heartbeat:' ):
			tokens = line.split( ':', 1 )
			if len( tokens ) == 2:
				parts = tokens[1].split()
				if len(parts[2]) != 2:
					parts[2] = '0' + parts[2]
				when = ' '.join( parts[0:4] + [parts[-1]] )
				self.println(
					self.ot.tick( when )
				)
		return

	def	post_end_file( self ):
		self.ot.report()
		return
