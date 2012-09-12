#!/usr/bin/python
# vim: noet sw=4 ts=4

import	sys
import	os
import	superclass

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	NAME	= 'apache-pp'
	DESCRIPTION = """Print apache-style configuration files."""

	PLAIN = [ 'info', 'deviceuri' ]

	def	__init__( self ):
		super(PrettyPrint, self).__init__()
		self.reset()
		return

	def	reset( self ):
		super(PrettyPrint, self).reset()
		self._init_section()
		self._clear_all_sections()
		return

	def	_clear_all_sections( self ):
		self.sections = []
		return

	def	_init_section( self ):
		self.kind    = 'Dunno'
		self.options = []
		self.name    = 'Dunno'
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

	def	_dump_section( self, kind, name, options ):
		print '<%s %s>' % (kind, name)
		options.sort()
		maxname = 15
		widths = {}
		for (name, vals) in options:
			maxname = max( maxname, len(name) )
			if name.lower() not in PrettyPrint.PLAIN:
				for i in xrange( 0, len(vals) ):
					width = len(vals[i])
					try:
						widths[i] = max( widths[i], width )
					except Exception, e:
						widths[i] = width
		fmt = ' %%-%ds ' % maxname
		for (name, vals) in options:
			print fmt % name,
			if name.lower() in PrettyPrint.PLAIN:
				print ' '.join( vals ),
			else:
				for i in xrange( 0, len(vals) ):
					vfmt = '%%-%ds' % widths[i]
					print vfmt % vals[i],
			print
		print '</%s>' % kind
		return

	def	end_file( self, fname ):
		self.sections.sort( key = lambda (k,p,o): '%s %s' % (k,p.lower()) )
		for (kind, name, options) in self.sections:
			self._dump_section( kind, name, options )
		self._clear_all_sections()
