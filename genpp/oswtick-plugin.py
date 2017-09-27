#!/usr/bin/python
# vim: noet sw=4 ts=4
#
# FYI: Currently, the OSWbb heartbeat file is generated like this:
#	$ date '+zzz ***%a %b %d %H:%M:%S %Y'
# But this is subject to change at any time.

import	datetime
import	os
import	sys
import	superclass
import	oswticker

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	NAME = 'oswbb-tick'
	DESCRIPTION="""Display OSWBB's log ticks, highlighting jitter."""

	def	__init__( self ):
		super( PrettyPrint, self ).__init__()
		return

	def	begin_file( self, fn ):
		super( PrettyPrint, self ).begin_file( fn )
		self.ot = oswticker.OswTicker( '%a %b %d %H:%M:%S %Y' )
		self.println(
			'# Day Mon Dy HH:MM:SS YYYY  Delta'
		)
		self.println(
			'# --- --- -- -------- ---- -------'
		)
		return

	def	next_line( self, line ):
		if line.startswith( 'zzz ***' ):
			parts = line[7:].split()
			# parts[0] == Day name
			# parts[1] == Month name
			# parts[2] == Day of month
			# parts[3] == HH:MM:SS
			# parts[4] == TZ
			# parts[5] == YEAR
			if len( parts ) == 6:
				if len(parts[2]) == 1:
					parts[2] = '0' + parts[2]
				when = ' '.join( parts[0:4] + parts[5:] )
				self.println(
					self.ot.tick( when )
				)
		return

	def	post_end_file( self ):
		self.ot.report()
		return
