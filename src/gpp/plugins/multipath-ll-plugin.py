#!/usr/bin/python
# vim: noet sw=4 ts=4

import	os
import	sys
import	string
import	superclass

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	NAME = 'multipath-ii'
	DESCRIPTION="""Display "# multipath -ll" in conical style."""

	def __init__( self ):
		super( PrettyPrint, self ).__init__()
		return

	def	reset( self ):
		super( PrettyPrint, self ).reset()
		self._new_path()
		self.paths   = []
		self.maxname = 0
		self.maxuuid = 0
		self.maxdev  = 0
		return

	def	_new_path( self ):
		self.components = []
		self.pathname = []
		self.attrs = []
		return

	def	begin_file( self, name ):
		super( PrettyPrint, self ).begin_file( name )
		self.reset()
		return

	def	end_file( self, name ):
		self._dump_paths()
		return

	def	next_line( self, line ):
		if line[0].isalnum():
			if len(self.components) > 0:
				self.paths.append((self.pathname, self.attrs, self.components))
			self._new_path()
			tokens = line.split()
			if len(tokens) == 4:
				name = tokens[0]
				self.maxname = max( self.maxname, len(name) )
				uuid = tokens[1]
				self.maxuuid = max( self.maxuuid, len(uuid) )
				dev  = tokens[2]
				self.maxdev = max( self.maxdev, len(dev) )
				san  = tokens[3]
				self.pathname = [name, uuid, dev, san]
		elif line[0] == '[':
			self.attrs = line.strip()
		else:
			self.components.append( line )
		return

	def	_key( self, ((name,uuid,dev,san),attr,parts) ):
		return dev.lower()

	def	_dump_paths( self ):
		if len(self.paths) > 0:
			self.paths.sort( key = self._key )
			tfmt = '%%-%ds %%-%ds %%-%ds %%s' % (
				self.maxname,
				self.maxuuid,
				self.maxdev
			)
			for ((name,uuid,dev,san),attr,parts) in self.paths:
				print tfmt % (name, uuid, dev, san)
				print '%s' % attr
				for part in parts:
					print '%s' % part
		self.reset()
		return

	def	finish( self ):
		self._dump_paths()
		return
