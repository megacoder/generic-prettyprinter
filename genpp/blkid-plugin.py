#!/usr/bin/python
# vim: noet sw=4 ts=4

import	os
import	string
import	superclass
import	sys
import	shlex

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	NAME = 'blkid-pp'
	DESCRIPTION="""List output of blkid(8) in a canonical form."""

	INDENT_WITH = '        '

	def __init__( self ):
		super( PrettyPrint, self ).__init__()
		return

	def	reset( self ):
		super( PrettyPrint, self ).reset()
		self._prepare()
		return

	def	_prepare( self ):
		self.lines = []
		self.max_name = 15
		self.attrlens = {}
		return

	def	next_line( self, line ):
		try:
			name, tokens = line.rstrip().split( ':', 1 )
			attrs = {}
			for arg in shlex.split( tokens ):
				key, value = map(
					str.strip,
					arg.split( '=', 1 )
				)
				arg = '{0}="{1}"'.format( key, value )
				self.attrlens[key] = max(
					len(key),
					self.attrlens[key] if key in self.attrlens.keys() else 0
				)
				attrs[key] = arg
				self.attrlens[key] = max(
					len(arg),
					self.attrlens[key] if key in self.attrlens.keys() else 0
				)
			self.lines.append( [ name, attrs ] )
			self.max_name = max( self.max_name, len(name) )
		except Exception, e:
			return
		return

	def	report( self, final = False ):
		if final: return
		nfmt = '{0:<%d}' % ( self.max_name + 1 )
		keys = self.attrlens.keys()
		keys.sort()
		fmts = {}
		for key in keys:
			fmts[key] = ' {0:<%d.%d}' % (
				self.attrlens[key],
				self.attrlens[key]
			)
		for name, attrs in sorted(
			self.lines,
			key = lambda (n,a) : n.lower()
		):
			line = nfmt.format( ( name + ':' ) )
			attrkeys = attrs.keys()
			options = []
			for key in keys:
				options.append( fmts[key].format(
					attrs[key] if key in attrkeys else ""
				))
			line += ( ' '.join( options ) )
			self.println( line.rstrip() )
		return
