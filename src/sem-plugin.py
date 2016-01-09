#!/usr/bin/python
# vi: noet sw=4 ts=4

import	os
import	sys
import	superclass

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	NAME = 'sem-pp'
	DESCRIPTION = """Display /proc/sys/kernel/sem files in canonical style."""

	def	__init__( self ):
		super( PrettyPrint, self ).__init__()
		self.notes = dict()
		self.names = []
		self._add_name( r'SEMMSL', r'Max semaphores per set' )
		self._add_name( r'SEMMNI', r'Max semaphore sets in system' )
		self._add_name( r'SEMMNS', r'Total semaphores in system' )
		self._add_name( r'SEMOPM', r'Max operations per semop(2)' )
		self.nNames = len( self.names )
		self.widest = [
			len( s ) for s in self.names
		]
		self.values = []
		return

	def	_add_name( self, name, desc = 'N/A' ):
		self.names.append( name )
		self.notes[name] = desc
		return

	def	next_line( self, line ):
		tokens = line.split()
		if len(tokens) == self.nNames:
			self.values.append(
				tokens
			)
			self.widest = [
				max(
					self.widest[i],
					len( tokens[i] )
				) for i in range( self.nNames )
			]
		return

	def	report( self, final = False ):
		if final:
			fmts = [
				'{0:>%d}' % self.widest[ i ] for i in range( self.nNames )
			]
			titles = [
				fmts[i].format( self.names[i] ) for i in range( self.nNames )
			]
			bars = [
				'-' * self.widest[ i ] for i in range( self.nNames )
			]
			self.println( ' '.join( titles ) )
			self.println( ' '.join( bars ) )
			for sample in self.values:
				v = [
					fmts[ i ].format( sample[ i ] ) for i in range( self.nNames )
				]
				self.println( ' '.join( v ) )
			for key in sorted( self.notes.keys() ):
				note = '{0} - {1}'.format(
					key,
					self.notes[ key ]
				)
				self.footnote(
					note
				)
		return
