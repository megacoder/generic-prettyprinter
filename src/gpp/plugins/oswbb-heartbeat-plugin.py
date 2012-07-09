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

	def	process( f = sys.stdin ):
		last = None
		old_delta = None
		fmt = '%a %b %d %H:%M:%S %Y'
		print '#  Day Mon Dy HH:MM:SS YYYY  Delta'
		print '#  --- --- -- -------- ---- -------'
		for line in f:
			if not line.startswith( 'oswbb heartbeat' ): continue
			tokens = line.rstrip().split( ':', 1 )
			if len( tokens ) == 2:
				parts = tokens[1].split()
				if len(parts[2]) != 2:
					parts[2] = '0' + parts[2]
				when = ' '.join( parts[0:4] + [parts[-1]] )
				try:
					dt = datetime.datetime.strptime( when, fmt )
				except Exception, e:
					raise e
					continue
				if last is None:
					last = dt
				delta = dt - last
				if old_delta is None:
					old_delta = delta
				if delta != old_delta:
					flag = '- '
				else:
					flag = '  '
				print '%s %s %s' % ( flag, when, delta )
				last = dt
				old_delta = delta
		return
