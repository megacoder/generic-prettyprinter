#!/usr/bin/python
# vim: noet sw=4 ts=4
#
# FYI: Currently, the OSWbb heartbeat file is generated like this:
#	zzz ***Wed Oct 22 19:00:00 EEST 2014
# But this is subject to change at any time.

import	datetime
import	os
import	sys
import	superclass

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	NAME = 'oswts-pp'
	DESCRIPTION="""Display OSWBB's timestamps, highlighting jitter."""

	MARK	= 'zzz ***'
	FMT		= '%a %b %d %H:%M:%S %Y'

	def	__init__( self ):
		super( PrettyPrint, self ).__init__()
		self._setup()
		return

	def	_setup( self ):
		self.timestamps = []
		self.maxlen     = 10
		return

	def	next_line( self, line ):
		if not line.startswith( PrettyPrint.MARK ):
			return
		# Only marker lines past this point
		timestamp = line[len(PrettyPrint.MARK):]
		self.maxlen = max( self.maxlen, len( timestamp ) )
		parts = timestamp.split()
		reftime = '%s %s %s %s %s' % (
			parts[0],
			parts[1],
			parts[2],
			parts[3],
			parts[5]
		)
		try:
			now = datetime.datetime.strptime(
				reftime,
				PrettyPrint.FMT
			)
			self.timestamps.append( ( now, timestamp ) )
		except Exception, e:
			self.println( 'Fmat: %s' % PrettyPrint.FMT )
			self.println( 'Time: %s' % refimt )
			self.println( e )
		return

	def	_center( self, s, width = 40 ):
		padding = ' ' * ((width - len(s)) / 2)
		return padding + s

	def	report( self, final = False ):
		if not final:
			return
		old_delta       = None
		timestamp_title = 'T I M E S T A M P'
		delta_title     = 'Delta'
		fmt             = '%%-%ds %%%ds' %	(
			self.maxlen,
			len( delta_title )
		)
		first = True
		for (now, timestamp) in sorted(
			self.timestamps,
			key = lambda tuple : tuple[0]
		):
			if first:
				self.println(
					fmt % (
						self._center(
							timestamp_title,
							self.maxlen
						),
						self._center(
							delta_title,
							len( delta_title )
						)
					)
				)
				self.println( fmt % (
					'-' * self.maxlen,
					'-' * len( delta_title )
				) )
				old_time = now
			delta = now - old_time
			show = first
			if first:
				old_delta = delta
				first     = False
			jitter = delta - old_delta
			if jitter:
				show = True
			if show:
				self.println(
					fmt % (
						timestamp,
						str( int( delta.total_seconds() + 0.5 ) )
					)
				)
			old_delta = delta
			old_time  = now
		return
