#!/usr/bin/python
# vim: noet sw=4 ts=4

import	sys
import	os
import	superclass

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	NAME        = 'apache-pp'
	DESCRIPTION = """Print apache-style configuration files."""

	PLAIN = [ 'info', 'deviceuri' ]

	def	__init__( self ):
		super(PrettyPrint, self).__init__()
		self.reset()
		return

	def	start( self ):
		super(PrettyPrint, self).__init__()
		self.sections = []
		return

	def	_init_section( self ):
		self.kind    = 'Dunno'
		self.options = []
		self.name    = 'Dunno'
		return

	def	pre_begin_file( self ):
		self._init_section()
		return

	def	next_line( self, line ):
		line = line.split( '#', 1 )[0].strip()	# Drop comments!
		if len(line) > 0:
			lowLine = line.lower()
			for (f,t) in [ ('\t', ' '), ('<', '< '), ('>', ' >') ]:
				line = line.replace( f, t )
			if lowLine.startswith( '</' ):
				self.sections.append( (self.kind, self.name, self.options) )
			elif lowLine.startswith( '<' ):
				self._init_section()
				tokens = line.split()
				self.kind = tokens[1]
				if len(tokens) > 2:
					self.name = ' '.join(tokens[2:-1])
			else:
				tokens = line.split( ' ' )
				if len(tokens) >= 2:
					self.options.append( (tokens[0], tokens[1:]) )
		return

	def	_dump_section( self, kind, label, options ):
		self.println( '<{0} {1}>'.format( kind, label ) )
		options.sort()
		widths = map(
			lambda (n,v) : len(n),
			options
		)
		fmts = map(
			lambda x : '{:<%d}' % x,
			widths
		)
		names = map(
			lambda (n,v) : n,
			lambda (o,v) : o
		)
		values = map(
			lambda f,v : f.format( v ),
			fmts,
			map(
				lambda (n,v) : v,
				options
			)
		)
		for (name, vals) in options:
			maxname = max( maxname, len(name) )
			if name.lower() not in PrettyPrint.PLAIN:
				for i in range( len( vals ) ):
					width = len( vals[i] )
					try:
						widths[i] = max( widths[i], width )
					except Exception, e:
						widths[i] = width
		# fmt = ' %%-%ds ' % maxname
		fmt = ' {0:<%d}' % maxname
		for (name, vals) in options:
			# print fmt % name,
			if name.lower() in PrettyPrint.PLAIN:
				# print ' '.join( vals ),
				clauses = ' '.join( vals )
			else:
				clauses = ''
				for i in xrange( 0, len(vals) ):
					# vfmt = '%%-%ds' % widths[i]
					vfmt = ' {1:<%d}' % widths[i]
					clauses += vfmt.format( vals[i] )
			# print
			self.println(
			)
			print
		self.println( '</{0}>'.format( kind ) )
		return

	def	end_file( self, fname ):
		for (kind, name, options) in sorted(
			self.sections,
			key = lambda (k,n,o): '{0} {1}'.format( k, n.lower()
		)):
			self._dump_section( kind, name, options )
		self._clear_all_sections()
		return
