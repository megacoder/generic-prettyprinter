#!/usr/bin/python
# vim: noet sw=4 ts=4

import	os
import	sys
import	string
import	superclass
import	re

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	NAME = 'arp'
	DESCRIPTION="""Display arp(1) in canonical style."""

	def __init__( self ):
		super( PrettyPrint, self ).__init__()
		self.pre_begin_file()
		return

	def	pre_begin_file( self ):
		self.need_title = True
		self.items      = []
		self.title      = ""
		return

	def	next_line( self, line ):
		line = line.strip()
		if len(line) > 0:
			if self.need_title:
				self.need_title = False
				self.title = line
			else:
				ip = line.split()[0].split( '.' )
				# self.items.append( (ip, line) )
				self.items.append( ([ int(x) for x in ip], line) )
		return

	def	report( self, final = False ):
		if len(self.items) > 0:
			self.items.sort( key = lambda (ip,line): ip )
			print self.title
			for (ip,line) in self.items:
				print line
		return
