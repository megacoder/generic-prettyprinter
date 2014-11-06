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

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	NAME = 'oswbb-hearbeat-pp'
	DESCRIPTION="""Display OSWBB's heartbeat file, highlighting jitter."""

	def	__init__( self ):
		super( PrettyPrint, self ).__init__()
		return

	def	begin_file( self, fn ):
		super( PrettyPrint, self ).begin_file()
		self.old_delta = None
		self.last      = None
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
				try:
					dt = datetime.datetime.strptime(
						when,
						'%a %b %d %H:%M:%S %Y'
					)
				except Exception, e:
					self.println( e )
					return
				if self.last is None:
					self.last = dt
				delta = dt - self.last
				if old_delta is None:
					old_delta = delta
				if flag:
					mark = '-'
				else:
					mark = ' '
				print '%s %s %s' % (
					mark,
					tokens[1],
					delta
				)
				self.last = dt
				self.old_delta = delta
		return
