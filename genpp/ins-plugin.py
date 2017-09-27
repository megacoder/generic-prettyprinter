#!/usr/bin/python

import	os
import	sys
import	superclass
import	math

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	NAME = 'ins'
	DESCRIPTION="""Display '$ ip neigh show' in canonical style."""

	def	__init__( self ):
		super( PrettyPrint, self ).__init__()
		return

	def	reset( self ):
		super( PrettyPrint, self ).reset()
		self._prepare()
		return

	def	_prepare( self ):
		self.content = []
		self.maxvia = 12
		return

	def	begin_file( self, name ):
		super( PrettyPrint, self ).begin_file( name )
		self._prepare()
		return

	def	_add( self, ip, dev, mac, state ):
		tokens = ip.split('.')
		for i in xrange( 0, len(tokens) ):
			tokens[i] = int(tokens[i])
		via = state + ':' + dev
		self.maxvia = max( self.maxvia, len(via) )
		self.content.append(
			(tokens, ip, mac, via)
		)
		return

	def	next_line( self, line ):
		tokens = line.split('#',1)[0].strip().split()
		if len(tokens) == 6:
			ip = tokens[0]
			dev = tokens[2]
			mac = tokens[4]
			state = tokens[5]
			self._add( ip, dev, mac, state )
		return

	def	end_file( self, name ):
		self.content.sort(
			key = lambda (t,i,m,v): t
		)
		fmt = '%%-15s  %%-%ds  %%s' % (self.maxvia)
		for (key,ip,mac,via) in self.content:
			print fmt % (ip, via, mac)
		super( PrettyPrint, self ).end_file( name )
		return
