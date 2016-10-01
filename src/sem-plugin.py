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
		self.names = dict()
		self.names['SEMMSL'] = 'Max semaphores per set'
		self.names['SEMNI' ] = 'Max semaphores in system'
		self.names['SEMMNS' ] = 'Total semaphores in system'
		self.names['SEMOPM' ] = 'Max operations per semop(2)'
		self.widest = [ len( s ) for s in self.names ]
		self.values = list()
		return

	def	next_line( self, line ):
		tokens = line.split()
		tokens = map(
			str.strip,
			line.split()
		)
		if len(tokens) == len(self.names):
			self.values.append(
				tokens
			)
			self.widest = [
				max(
					self.widest[i],
					len( tokens[i] )
				) for i in range( len(self.names) )
			]
		return

	def	report( self, final = False ):
		if final:
			N = len(self.names)
			fmts = [
				'{{0:>{0}}}'.format(
					self.widest[i] for i in range( N )
				)
			]
			titles = [
				fmts[i].format( self.names[i] ) for i in range( N )
			]
			bars = [
				'-' * self.widest[i] for i in range( N )
			]
			self.println( ' '.join( titles ) )
			self.println( ' '.join( bars ) )
			for sample in self.values:
				v = [
					fmts[i].format( sample[i] ) for i in range( N )
				]
				self.println( ' '.join( v ) )
			self.println()
			title = 'Legend'
			self.println( title )
			self.println( '-' * len(title) )
			self.println()
			for key in sorted( self.notes ):
				self.println(
					'{0}: {1}'.format(
						key,
						self.notes[ key ]
					)
				)
		return
