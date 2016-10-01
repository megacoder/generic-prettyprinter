#!/usr/bin/python
# vim: noet sw=4 ts=4

import	sys
import	os
import	stat
import	superclass

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	NAME = 'mount'

	DESCRIPTION = """Display /proc/mounts or mount(8) in a canonical form."""

	FIELDS = dict(
		name    = None,
		mp      = None,
		type    = None,
		backup  = None,
		fsck    = None,
		attr    = None,
		details = None
	)

	def	__init__( self ):
		super( PrettyPrint, self ).__init__()
		self.pre_begin_file()
		return

	def	pre_begin_file( self, name = None ):
		self.widths  = dict()
		self.content = list()
		self.is_proc = False
		self.first   = True
		return

	def	next_line( self, line ):
		tokens = map(
			str.strip,
			line.split()
		)
		if len(tokens) == 6:
			# Make 7 tokens if only 6
			tokens.append( None )
		if len(tokens) != 7:
			self.footnote(
				'Expected 7 tokens, got {0}'.format( len( tokens ) )
			)
			return
		if self.first:
			self.is_proc = tokens[5].isdigit()
			self.first = False
		fields = dict()
		if self.is_proc:
			# /proc/mounts type of file.
			fields['name']    = tokens[0]
			fields['mp']      = tokens[1]
			fields['type']    = tokens[2]
			attr              = tokens[3].split( ',' )
			fields['backup']  = tokens[4]
			fields['fsck']    = tokens[5]
			fields['details'] = tokens[6]
		else:
			# /bin/mount type of file
			fields['name']    = tokens[0]
			fields['mp']      = tokens[2]
			fields['type']    = tokens[4]
			# Reorder the mount flags for readability.
			fields['attr']	  = ','.join(
				[ x for x in sorted( tokens[5][1:-1].split( ',' ) ) ]
			)
			fields['backup']  = None
			fields['fsck']    = None
			fields['details'] = tokens[6]
		for key in fields:
			field = fields[key]
			if field:
				if key not in self.widths:
					self.widths[key] = len(field)
				else:
					self.widths[key] = max( self.widths[key], len(field) )
		self.content.append( fields )
		return

	def	report( self, final = False ):
		if not final:
			for fields in sorted(
				self.content,
				key = lambda f: f['name']
			):
				columns = list()
				for key in PrettyPrint.FIELDS:
					if key in fields and fields[key]:
						fmt = '{{0:<{0}}}'.format( self.widths[key] )
						columns.append(
							fmt.format( fields[key] )
						)
				self.println( ' '.join( columns ) )
		return
