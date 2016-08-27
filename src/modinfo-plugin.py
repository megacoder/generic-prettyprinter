#!/usr/bin/python

import	os
import	sys
import	superclass

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	NAME = 'modinfo-pp'
	DESCRIPTION = """Display modinfo(8) output in canonical style."""

	def	__init__( self ):
		super( PrettyPrint, self ).__init__()
		return

	def	reset( self ):
		super( PrettyPrint, self ).reset()
		self._prepare()
		return

	def	pre_begin_file( self ):
		self.info   = dict()
		return

	def	next_line( self, line ):
		tokens = line.split( ':', 1 )
		tokens = map(
		    str.strip,
		    line.split( ':', 1 )
		)
		if len(tokens) == 2:
			field = tokens[0]
			value = tokens[1]
			if field == "filename":
			    # Line break
			    self.report()
			self.info[ field ] = value
		return

	def	report( self, final = False ):
	    if not final:
		if self.info != {}:
		    maxkey = max(
			7,
			map( ken, self.info )
		    )
		    fmt = '{{0:<{0}}}}: {{1}}'.format( maxkey )
		    for key in sorted( self.info ):
			self.println(
			    fmt.format( key, self.info[key] )
			)
	    return
