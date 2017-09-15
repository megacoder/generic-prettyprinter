#!/usr/bin/python
# vi: noet sw=4 ts=4

import	os
import	sys
import	superclass
import	string

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	NAME = 'iptables-pp'
	DESCRIPTION = """Display 'iptables -L' output in canonical style."""

	def	__init__( self ):
		super( PrettyPrint, self ).__init__()
		return

	def	pre_begin_file( self, name = None ):
		self.tables = dict()
		self.tname = None
		return

	def	own_glob( self ):
		return '-'

	def	next_line( self, line ):
		tokens = map(
			str.strip,
			line.split( '#', 1 )[0].split()
		)
		if len( tokens ) == 0: return
		key = tokens[0]
		if key.startswith( '*' ):
			# New table
			self.tname = key[1:]
			self.tables[ self.tname ] = dict()
		elif key.startswith( ':' ):
			# New chain for table
			chain_name = key[1:]
			self.tables[ self.tname ][ chain_name ] = dict({
				'args' : tokens[1:],
				'rules' : list()
			})
		elif key.startswith( '-' ):
			# New rule for table chain
			if len( tokens ) < 2: return
			chain_name = tokens[ 1 ]
			if chain_name in self.tables[ self.tname ]:
				self.tables[ self.tname ][ chain_name ]['rules'].append(
					tokens
				)
			else:
				self.error(
					'unknown chain: {0}: {1}'.format(
						chain_name,
						tokens
					)
				)
		elif key == 'COMMIT':
			# End the table
			pass
		else:
			# Dunno
			self.println( 'Ignoring line: {0}'.format( line ) )
			pass
		return

	def	report( self, final = False ):
		if final: return
		for table_name in sorted( self.tables ):
			self.println(
				'*{0}'.format( table_name )
			)
			chain_width = max(
				map(
					len,
					self.tables[ table_name ]
				)
			)
			chain_fmt = ':{{0:{0}s}} {{1}}'.format( chain_width )
			for chain_name in sorted( self.tables[ table_name ] ):
				self.println(
					chain_fmt.format(
						chain_name,
						'\t'.join( self.tables[ table_name ][chain_name]['args'] ),
					)
				)
				for rule in self.tables[ table_name ][ chain_name
											  ]['rules']:
					self.println(
						' '.join( rule )
					)
			self.println( 'COMMIT' )
		return
