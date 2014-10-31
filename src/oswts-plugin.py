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
		self.first = True
		self.old_time = None
		return

	def	next_line( self, line ):
		if line.startswith( PrettyPrint.MARK ):
			timestamp = line[len(PrettyPrint.MARK):]
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
			except Exception, e:
				self.println( 'Fmat: %s' % PrettyPrint.FMT )
				self.println( 'Time: %s' % refimt )
				self.println( e )
				return
			if self.first:
				self.old_time = now
			delta = now - self.old_time
			show = self.first
			show = True # FIXME
			if self.first:
				self.old_delta = delta
				self.first     = False
			jitter = delta - self.old_delta
			if jitter:
				show = True
			if show:
				msg = '%s %3s' %	(
					timestamp,
					str( int( delta.total_seconds() + 0.5 ) )
				)
				self.println( msg )
			self.old_delta = delta
			self.old_time  = now
		return
