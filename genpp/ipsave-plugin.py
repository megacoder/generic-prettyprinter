#!/usr/bin/python
# vi: noet sw=4 ts=4

import	os
import	sys
import	superclass
import	string

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	NAME = 'ipsave-pp'
	DESCRIPTION = """Display '/etc/sysconfig/iptables' rules in canonical style."""

	def	__init__( self, name = '{firewall}' ):
		super( PrettyPrint, self ).__init__()
		self.firewall     = dict()	# Holds known fireall tables
		self.table        = dict()	# Holds chains we know
		self.table_name   = None
		self.chain        = list()	# Holds list of rules
		self.chain_name   = None
		self.rule_widths  = dict()	# Widths of all filter rule fields
		self.chain_widths = dict()	# Widths of all chain titles
		return

	def	next_line( self, line ):
		tokens = map(
			str.strip,
			line.split( '#', 1 )[ 0 ].split()
		)
		Ntokens = len( tokens )
		if Ntokens == 0: return
		if tokens[0].startswith( '*' ):
			# Tables begin with star (*) through 'COMMIT' line
			self.table      = dict()
			self.table_name = tokens[0]
		elif tokens[0].startswith( ':' ):
			# Chain begins with colon (:) and ends with 'COMMIT' or another
			# ':' line
			if self.chain_name:
				self.table[ self.chain_name ] = self.chain
			self.chain_name = tokens[0]
			self.chain      = list()
			self.chain.append( tokens )
			for i in range( len( tokens ) ):
				self.chain_widths[i] = max(
					self.chain_widths.get( i, 1 ),
					len( tokens[i] )
				)
		elif tokens[0] == 'COMMIT':
			# End of table marked by 'COMMIT'
			self.chain.append( tokens )
			if self.chain_name:
				self.table[ self.chain_name ] = self.chain
				self.chain_name               = None
			if self.table_name:
				self.firewall[ self.table_name ] = self.table
			self.table_name = None
		else:
			# Chain rule
			self.chain.append( tokens )
			for i in range( len( tokens ) ):
				self.rule_widths[i] = max(
					self.rule_widths.get( i, 1 ),
					len( tokens[i] )
				)
		return

	def	report( self, final = False ):
		if final: return
		chain_fmts = map(
			'{{0:<{0}}}'.format,
			[ self.chain_widths[ w ] for w in sorted( self.chain_widths ) ]
		)
		rule_fmts = map(
			'{{0:<{0}}}'.format,
			[ self.rule_widths[ w ] for w in sorted( self.rule_widths ) ]
		)
		for tname in sorted( self.firewall ):
			self.println()
			self.println( '{0}'.format( tname ) )
			chains = self.firewall[ tname ]
			for chain in sorted( chains ):
				rules = chains[ chain ]
				for rule in rules:
					if rule[0].startswith( ':' ):
						gutter = ' '
						columns = map(
							lambda i: chain_fmts[i].format( rule[i] ),
							range( len( rule ) )
						)
					else:
						gutter = '  '
						columns = map(
							lambda i: rule_fmts[i].format( rule[i] ),
							range( len( rule ) )
						)
					self.println( gutter + ' '.join( columns ) )
		return

if __name__ == '__main__':
	for arg in sys.argv[1:]:
		pp = PrettyPrint()
		try:
			pp.process( arg )
		except Exception, e:
			raise e
	exit( 0 )
