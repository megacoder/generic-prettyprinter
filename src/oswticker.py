#!/usr/bin/python
# vim: noet sw=4 ts=4

import	datetime
import	os
import	sys

class	OswTicker( object ):

	def	__init__( self, fmt = '%a %b %d %H:%M:%S %Y' ):
		self.fmt       = fmt
		self.old_delta = None
		self.last      = None
		return

	def	tick( self, tick ):
		dt = datetime.datetime.strptime(
			tick,
			self.fmt
		)
		if self.last is None:
			self.last = dt
		delta = dt - self.last
		if old_delta is None:
			old_delta = delta
		if flag:
			mark = '-'
		else:
			mark = ' '
		self.last      = dt
		self.old_delta = delta
		s = '{0} {1} {2}'.format(
			mark,
			tick,
			delta
		)
		return s
