#!/usr/bin/python
# vim: noet sw=4 ts=4

import	os
import	sys
import	superclass

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	NAME        = 'printk'
	DESCRIPTION = """Display /proc/sys/kernel/printk files in style."""

	def	__init__( self ):
		super( PrettyPrint, self ).__init__()
		return

	def	_decode( self, level ):
		levels = dict({
			'0': 'kernel emergency; system is unusable',
			'1': 'kernel alert; immediate action required',
			'2': 'kernel condition is critical',
			'3': 'general kernel error',
			'4': 'kernel warning',
			'5': 'significant kernel condition',
			'6': 'informational message',
			'7': 'debug message',
		})
		key = str( level )
		if key in levels:
			value = levels[ key ]
		else:
			value = 'Level-{0}'.format( key )
		return value

	def	decode( self, level ):
		if isinstance( level, list ):
			value = [
				self._decode( L ) for L in level
			]
		else:
			key = str( key )
			value = self._decode( key )
		return value

	def	next_line( self, line ):
		tokens = line.split()
		if len( tokens ) != 4: return
		#
		fields = [
			'console_loglevel',
			'default_loglevel',
			'lowest_loglevel',
			'default_console_loglevel',
		]
		width = max(
			map(
				len,
				fields
			)
		)
		fmt = 'Field {{0}}: {{1:>{0}}} {{2}}'.format(
			width
		)
		#
		self.println(
			'Original:  {0}'.format( line )
		)
		self.println()
		values = self.decode( tokens )
		for i, field in enumerate( fields ):
			self.println(
				fmt.format(
					i + 1,
					fields[ i ],
					values[ i ],
				)
			)
		return
