#!/usr/bin/python
# vim: noet sw=4 ts=4

import	sys
import	os
import	superclass

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	NAME = 'hosts-pp'
	DESCRIPTION="""Display /etc/hosts in canonical style."""

	def	__init__( self ):
		super( PrettyPrint, self ).__init__()
		return

	def	reset( self ):
		super( PrettyPrint, self ).reset()
		self._prepare()
		return

	def	_prepare( self ):
		self.lines = []
		self.max_canonical_name = 0
		return

	def	next_line( self, line ):
		tokens = line.split( '#', 1 )[0].split()
		n = len( tokens )
		if n >= 2:
			addr = tokens[0]
			name = tokens[1]
			self.max_canonical_name = max( self.max_canonical_name, len(name) )
			aliases = []
			if n > 2:
				aliases = tokens[2:]
				aliases.sort()
			ip = 0
			if addr.find(':') == -1:
				for octet in addr.split('.'):
					ip = ip * 256 + int(octet)
			self.lines.append(
				(ip, addr, name, aliases)
			)
		return

	def	report( self, final = False ):
		self.lines.sort( key = lambda (ip,addr,name,aliases): ip )
		fmt = '%%-15s %%-%ds %%s' % self.max_canonical_name
		for ip, addr, name, aliases in self.lines:
			print fmt % (addr, name, ' '.join(aliases) )
		self._prepare()
		return
