#!/usr/bin/python
# vim: noet sw=4 ts=4

import	sys
import	os
import	stat
import	superclass

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	NAME = 'partitions'
	DESCRIPTION = """Display /proc/partitions in a canonical form."""

	def	__init__( self ):
		super( PrettyPrint, self ).__init__()
		return

	def	reset( self ):
		super( PrettyPrint, self ).reset()
		self._prepare()
		return

	def	_prepare( self ):
		self.content = []
		return

	def next_line( self, line ):
		tokens = line.split('#',1)[0].strip().split()
		n = len( tokens )
		if n == 4:
			if tokens[0] != 'major':
				major = int(tokens[0])
				minor = int(tokens[1])
				nbloc = int(tokens[2])
				name  = tokens[3]
				self.content.append(
					(major, minor, nbloc, name)
				)
		return

	def	report( self, final = False ):
		if len( self.content ) > 0:
			self.content.sort(
				key = lambda (maj,mnr,nbloc,name) : name.lower()
			)
			print '%7s\t%7s\t%15s\t%s' % (
				'Major',
				'Minor',
				'# Blocks',
				'Name'
			)
			print '%7s\t%7s\t%15s\t%s' % (
				'-------',
				'-------',
				'---------------',
				'----'
			)
			for (major, minor, nbloc, name) in self.content:
				print '%7d\t%7d\t%15d\t%s' % (
					major, minor, nbloc, name
				)
		self._prepare()
		return
