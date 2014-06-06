#!/usr/bin/python
# vim: noet sw=4 ts=4

import	os
import	sys
import	string
import	superclass
import	re

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	NAME = 'arp'
	DESCRIPTION="""Display arp(1) in conical style."""

	def __init__( self ):
		super( PrettyPrint, self ).__init__()
		return

	def	reset( self ):
		super( PrettyPrint, self ).reset()
		self.prepare()
		return

	def	prepare( self ):
		self.need_title = True
		self.items      = []
		self.title      = ""
		return

	def	begin_file( self, name ):
		super( PrettyPrint, self ).begin_file( name )
		self.prepare()
		return

	def	end_file( self, name ):
		self._show_content()
		super( PrettyPrint, self ).end_file( name )
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

	def	_show_content( self ):
		if len(self.items) > 0:
			self.items.sort( key = lambda (ip,line): ip )
			print self.title
			for (ip,line) in self.items:
				print line
		return
