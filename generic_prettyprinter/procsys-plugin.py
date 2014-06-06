#!/usr/bin/python
# vim: noet sw=4 ts=4

import	os
import	sys
import	string
import	superclass

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	NAME = 'procsys'
	DESCRIPTION="""Display /proc/sys/* in conical style."""

	def __init__( self ):
		super( PrettyPrint, self ).__init__()
		self.others = False
		return

	def	do_name( self, name ):
		"""Incoming names are relative to /proc/sys."""
		if os.path.isdir( name ):
			self.do_dir( name )
		return

	def	do_dir( self, dn ):
		try:
			names = os.listdir( dn )
		except Exception, e:
			return
		if self.others:
			print
		self.others = True
		title = 'Settings for %s' % dn
		print title
		print '-' * len(title)
		print
		names.sort()
		max_name = 0
		for name in names:
			max_name = max( max_name, len(name) )
		fmt = '%%%ds: %%s' % (max_name + 1)
		for name in names:
			fn = os.path.join( dn, name )
			if os.path.isfile( fn ):
				try:
					f = open( fn, 'rt' )
					value = f.readline().strip()
					f.close()
					print fmt % (name, value)
				except Exception, e:
					pass
		for name in names:
			fn = os.path.join( dn, name )
			if os.path.isdir( fn ):
				self.do_dir( fn )
		return
