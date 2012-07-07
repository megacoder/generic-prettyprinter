#!/usr/bin/python
# vim: noet sw=4 ts=4

import	sys
import	os
import	stat
import	superclass

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	NAME = 'mount-pp'
	DESCRIPTION = """Display /proc/mounts or mount(8) in a canonical form."""

	def	__init__( self ):
		super( PrettyPrint, self ).__init__()
		return

	def	reset( self ):
		self.lines = []
		self.is_proc = False
		return

	def	process( self, f = sys.stdin ):
		first = True
		for line in f:
			tokens = line.rstrip().split()
			n = len( tokens )
			if n != 6:
				self.error( 'Huh? %s' % line.rstrip() )
			else:
				if first:
					self.is_proc = tokens[5].isdigit()
					first = False
				if self.is_proc:
					# /proc/mounts type of file.
					name   = tokens[0]
					mp     = tokens[1]
					type   = tokens[2]
					attr   = tokens[3].split( ',' )
					backup = tokens[4]
					fsck   = tokens[5]
				else:
					# /bin/mount type of file
					name   = tokens[0]
					mp     = tokens[2]
					type   = tokens[4]
					attr   = tokens[5][1:-1].split( ',' )
					backup = None
					fsck   = None
				attr.sort()
				self.lines.append(
					( name, mp, type, attr, backup, fsck )
				)
		return

	def	finish( self ):
		others = False
		fmt = '%-39s %s\n\ttype=%s\tattr=%s'
		self.lines.sort()
		for (name, mp, type, attr, backup, fsck) in self.lines:
			# print name, mp, type, ','.join(attr), backup, fsck
			if others:
				print
			others = True
			print fmt % (
				name,
				mp,
				type,
				','.join(attr)
			)
			if self.is_proc:
				print '\tbackup=%s\tfsck=%s' % (backup, fsck)
		return
