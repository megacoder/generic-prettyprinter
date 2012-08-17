#!/usr/bin/python
# Print /etc/sysconfig/oracleasm in a canonical style.

import	os
import	sys
import	superclass

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	NAME = 'asm'
	DESCRIPTION = """Display /etc/sysconfig/oracleasm files in canonical style."""
	NAMES = [
		'ORACLEASM_ENABLED',
		'ORACLEASM_GID',
		'ORACLEASM_SCANBOOT',
		'ORACLEASM_SCANEXCLUDE',
		'ORACLEASM_SCANORDER',
		'ORACLEASM_UID',
	]

	def __init__( self ):
		super( PrettyPrint, self ).__init__()
		return

	def	reset( self ):
		super( PrettyPrint, self ).reset()
		self._prepare_settings()
		return

	def	_prepare_settings( self ):
		self.used = {}
		for name in PrettyPrint.NAMES:
			self.used[name] = False
		self.lines = []
		return

	def next_line( self, line ):
		octothorpe = line.find( '#' )
		if octothorpe > -1:
			line = line[:octothorpe]
		tokens = line.strip().split( '=', 1 )
		if len(tokens) == 2:
			name = tokens[0].strip()
			value = tokens[1].strip()
			# if value[0] != '"' and value[0] != "'":
			# 	value = '"' + value + '"'
			self.used[name] = True
			self.lines.append( (name, value) )
		return

	def begin_file( self, name ):
		if self.multi > 1:
			print '#' * 80
			print '# File %d of %d: %s' % (self.fileno, self.multi, name)
			print '#' * 80
		self.lines = []
		return

	def end_file( self, name ):
		self.lines.sort()
		for (name, value) in self.lines:
			print '%s=%s' % ( name, value )
		for key in self.used.keys():
			if not self.used[key]:
				print '# Setting "%s" not specified.' % key
		if self.multi > 1 and self.multi != self.fileno:
			print
		return

