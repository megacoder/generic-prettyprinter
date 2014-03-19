#!/usr/bin/python
# vim: noet sw=4 ts=4

import	os
import	sys
import	string
import	superclass

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	NAME = 'lvm'
	DESCRIPTION = """Display LVM configuration files in a canonical form."""

	def __init__( self ):
		super( PrettyPrint, self ).__init__()
		return

	def	reset( self ):
		super( PrettyPrint, self ).reset()
		self._prepare()
		return

	def	_prepare( self ):
		self.stanzas     = []
		self.new_stanza( None )
		return

	def	new_stanza( self, header ):
		self.header   = header
		self.footer   = None
		self.stanza   = []
		return

	def	finish_stanza( self, footer ):
		self.stanza.sort()
		self.stanzas.append( (self.header, self.stanza, footer) )
		return

	def	dump_stanza( self, header, body, footer ):
		maxname = 13
		for (f,v) in body:
			maxname = max( maxname, len(f) )
		fmt = '%%%ds = %%s' % (maxname+2)
		body.sort()
		print '\t'.join(header)
		if len(body) > 0: print
		for tokens in body:
			print fmt % ( tokens[0], ' '.join( tokens[1:] ) )
		print
		print '\t'.join(footer)
		return

	def	expand( self, line ):
		# print '|%s|-->' % line,
		for (f,t) in [
			('{', ' { '),
			('}', ' } '),
			('=', ' = '),
			( '[', ' [ '),
			( ']', ' ] ')
		]:
			line = line.replace( f, t )
		# print '|%s|' % line
		return line

	def	next_line( self, line ):
		line = line.split( '#', 1 )[0].strip()
		if len(line) == 0: return
		if line.endswith( '{' ):
			self.new_stanza( self.expand(line).split() )
		elif line.startswith( '}' ):
			self.finish_stanza( self.expand(line).split() )
		else:
			tokens = line.split( '=', 1 )
			n = len(tokens)
			if n == 2:
				for i in xrange( 0, n ):
					tokens[i] = tokens[i].strip()
				self.stanza.append( tokens )
		return

	def	begin_file( self, fn ):
		super( PrettyPrint, self ).begin_file( fn )
		self._prepare()
		return

	def	end_file( self, fn ):
		self.stanzas.sort()
		others = False
		for (header,body,footer) in self.stanzas:
			if others:
				print
			self.dump_stanza( header, body, footer )
			others = True
		super( PrettyPrint, self ).end_file( fn )
		return
