#!/usr/bin/python
# vim: noet sw=4 ts=4

import	os
import	sys
import	math
import	superclass

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	NAME = 'ntp-pp'
	DESCRIPTION="""Output /etc/ntp.conf in canonical form."""

	def __init__( self ):
		super( PrettyPrint, self ).__init__()
		return

	def ignore( self, name ):
		return not name.endswith( '.conf' )

	def pre_begin_file( self, fn = None ):
		self.groups = dict()
		return

	def next_line( self, line ):
		tokens = line.split( '#', 1 )[0].split()
		if len(tokens) > 0:
			key = tokens[0].lower()
			self.groups[key] = self.groups(key,list()).append(tokens)
		return

	def report( self, final = False ):
		if final: return
		# Space groups of similar lines similarly
		for key in sorted( self.groups ):
			# One pass to calculate the widths of this group columns
			widths = dict()
			for tokens in self.groups[key]:
				widths = map(
					lambda i: max( widths.get(i,0), len(tokens[i])),
					range( len(tokens) )
				)
			# Build the column formats
			fmts = map(
				lambda i: '{{0:{0}}}'.format( widths[i] ),
				range( len( widths ) )
			)
			# Output this group
			self.println()
			for tokens in sorted( self.groups[key] ):
				cols = map(
					lambda i : fmts[i].format( tokens[i] ),
					range( len( tokens ) )
				)
				self.println( ' '.join( cold ) )
		return
