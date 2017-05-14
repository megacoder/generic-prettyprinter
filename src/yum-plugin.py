#!/usr/bin/python
# vim: noet sw=4 ts=4

import	os
import	sys
import	superclass

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	NAME        = 'yum.repo'
	DESCRIPTION = """Display /etc/yum.repos.d/*.repo files in style."""

	def	__init__( self ):
		super( PrettyPrint, self ).__init__()
		self.channel_names = dict()
		return

	def	ignore( self, fn ):
		return not fn.endswith( '.repo' )

	def	pre_begin_file( self, name = None ):
		super( PrettyPrint, self ).pre_begin_file( name )
		self.repo_filename = name if name else '_ORPHAN_'
		self._channel_start()
		self.max_width         = 6
		self.channels      = dict()
		return

	def	_channel_start( self, channel_name = None ):
		if channel_name:
			if channel_name in self.channel_names:
				self.footnote(
					'Channel {0} already defined in "{0}"'.format(
						self.channel_names[ channel ]
					)
				)
			else:
				self.channel_names[ channel_name ] = self.repo_filename
		self.channel_name = channel_name
		self.channel_attrs = dict()
		return

	def	_channel_end( self ):
		if self.channel_name:
			# Calculate width of longest attribute seen
			width = max(
				map(
					len,
					self.channel_attrs
				)
			)
			self.max_width = max( self.max_width, width )
			#
			self.channels[ self.channel_name ] = self.channel_attrs
			#
			self.channel_name = None
		return

	def	next_line( self, line ):
		if line.startswith( '[' ):
			self._channel_end()
			self._channel_start( line.strip() )
		else:
			tokens = map(
				str.strip,
				line.split( '#', 1 )[0].split( '=', 1 )
			)
			if len(tokens) == 2:
				name  = tokens[0]
				value = tokens[1]
				self.channel_attrs[ name ] = value
		return

	def	post_end_file( self, name = None ):
		self._channel_end()
		super( PrettyPrint, self ).post_end_file( name )
		return

	def	report( self, final = False ):
		if final: return
		# Find the longest repo attribute amongst all those
		# defined in this file.
		fmt = ' {{0:>{0}}} = {{1}}'.format( self.max_width )
		others = False
		for channel in sorted( self.channels, key = lambda k : k.lower() ):
			if others:
				self.println()
			others = True
			self.println( '{0}'.format( channel ) )
			self.println()
			attrs = self.channels[ channel ]
			for key in sorted( attrs, key = lambda k : k.lower() ):
				self.println(
					fmt.format(
						key,
						attrs[ key ]
					)
				)
		return
