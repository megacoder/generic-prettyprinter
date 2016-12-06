#!/usr/bin/python
# vim: noet sw=4 ts=4

import	os
import	sys
import	superclass
import	align

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	NAME = 'crontab-pp'
	DESCRIPTION = """Display crontab files in canonical style."""

	def	__init__( self ):
		super( PrettyPrint, self ).__init__()
		return

	def pre_begin_file( self ):
		self.vars = []
		self.items = align.Align( titles = 1 )
		self.items.add([
			'# MN',
			'HR',
			'DOM',
			'MON',
			'DOW',
			'COMMAND ___'
		])
		alignment = 'aaaccl'
		self.items.set_title_alignment( alignment )
		self.items.set_alignment( alignment )
		return

	def	next_line( self, line ):
		line = line.split( '#', 1 )[0].strip()
		if line.find( '=' ) > -1:
			tokens = map(
				str.strip,
				line.split( '=', 1 )
			)
			self.vars.append( '='.join( tokens ) )
		else:
			tokens = line.split( None, 5 )
			self.items.add( tokens )
		return

	def	report( self, final = False ):
		if not final:
			for line in self.vars:
				self.println( line )
			if len(self.vars) > 0:
				self.println()
			for _,items in self.items.get_items():
				self.println( ' '.join( items ) )
		return

# Minimal skeleton for testing individual modules

if __name__ == '__main__':
	fn = '<selftest>'
	pp = PrettyPrint()
	pp.pre_begin_file()
	pp.begin_file( fn )
	for line in [
		'MAILTO=mad@you.now',
		'* * * * * echo can you hear me now'
	]:
		pp.next_line( line )
	pp.end_file( fn )
	pp.post_end_file()
	pp.report( final = True )

