#!/usr/bin/python
# vim: noet sw=4 ts=4

import	os
import	sys
import	string
import	superclass
import	re

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	NAME = 'pam'
	DESCRIPTION="""Display /etc/pam.d in conical style."""

	def __init__( self ):
		super( PrettyPrint, self ).__init__()
		return

	def	reset( self ):
		super( PrettyPrint, self ).reset()
		self.prepare()
		return

	def	prepare( self ):
		self.maxname   = 7
		self.maxgroup  = 7
		self.maxmodule = 7
		self.items     = []
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
		octothorpe = line.find( '#' )
		if octothorpe > -1:
			line = line[:octothorpe]
		line = line.strip()
		m = re.search( '^([^]]*)(\[[^]]*\])(.*)$', line )
		if m is not None:
			token = m.group(2).replace( ' ', '\1' )
			line = m.group(1) + token + m.group(3)
		tokens = line.split()
		if len(tokens) >= 3:
			name = tokens[0]
			self.maxname = max( self.maxname, len(name) )
			group = tokens[1]
			self.maxgroup = max( self.maxgroup, len(group) )
			module = tokens[2]
			self.maxmodule = max( self.maxmodule, len(module) )
			self.items.append( (name, group, module, tokens[3:]) )
		return

	def	_show_content( self ):
		if len(self.items) > 0:
			fmt = '%%-%ds  %%-%ds  %%-%ds  %%s' % (
				self.maxname,
				self.maxgroup,
				self.maxmodule
			)
			for (name,group,module,options) in self.items:
				options.sort()
				s = fmt % (name, group, module, ' '.join(options))
				print s.replace( '\1', ' ' )
		return
