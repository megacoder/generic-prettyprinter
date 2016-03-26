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
			delta     = datetime.timedelta()
			mark      = ' '
		else:
			delta = dt - self.last
			if self.old_delta is None:
				mark = ' '
				self.old_delta = delta
			else:
				if delta < self.old_delta:
					mark = '-'
				elif delta > self.old_delta:
					mark = '+'
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
