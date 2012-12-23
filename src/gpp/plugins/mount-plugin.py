#!/usr/bin/python
# vim: noet sw=4 ts=4

import	sys
import	os
import	stat
import	superclass

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	NAME = 'mount'
	DESCRIPTION = """Display /proc/mounts or mount(8) in a canonical form."""
	FIELDS = ['name', 'mp', 'type', 'backup', 'fsck', 'attr' ]

	def	__init__( self ):
		super( PrettyPrint, self ).__init__()
		return

	def	reset( self ):
		super( PrettyPrint, self ).reset()
		self._prepare()
		return

	def	_prepare( self ):
		self.widths = {}
		self.content = []
		self.is_proc = False
		self.first = True
		return

	def	begin_file( self, name ):
		super( PrettyPrint, self ).begin_file( name )
		self._prepare()
		return

	def	next_line( self, line ):
		tokens = line.rstrip().split()
		n = len( tokens )
		if n != 6:
			self.error( 'Huh? %s' % line.rstrip() )
		else:
			if self.first:
				self.is_proc = tokens[5].isdigit()
				self.first = False
			fields = {}
			if self.is_proc:
				# /proc/mounts type of file.
				fields['name']   = tokens[0]
				fields['mp']     = tokens[1]
				fields['type']   = tokens[2]
				attr             = tokens[3].split( ',' )
				fields['backup'] = tokens[4]
				fields['fsck']   = tokens[5]
			else:
				# /bin/mount type of file
				fields['name']   = tokens[0]
				fields['mp']     = tokens[2]
				fields['type']   = tokens[4]
				attr             = tokens[5][1:-1].split( ',' )
				fields['backup'] = None
				fields['fsck']   = None
			attr.sort()
			fields['attr'] = ','.join(attr)
			for key in fields.keys():
				field = fields[key]
				if field is not None:
					try:
						self.widths[key] = max(self.widths[key], len(field))
					except:
						self.widths[key] = len(field)
			self.content.append( fields )
		return

	def	end_file( self, name ):
		self.content.sort( key = lambda f: f['name'] )
		for fields in self.content:
			line = ""
			sep = ''
			for key in PrettyPrint.FIELDS:
				try:
					field = fields[key]
					if field is not None:
						fmt = '%%s%%-%ds' % self.widths[key]
						line += fmt % (sep, field)
						sep = ' '
				except:
					pass
			print line.rstrip()
		super( PrettyPrint, self ).end_file( name )
		return
