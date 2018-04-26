#!/usr/bin/python
# vim: noet sw=4 ts=4

import	sys
import	os
import	stat
import	superclass

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	NAME = 'mount'

	DESCRIPTION = """Display /proc/mounts or mount(8) in a canonical form."""

	FIELDS = dict(
		name    = None,
		mp      = None,
		type    = None,
		backup  = None,
		fsck    = None,
		attr    = None,
		details = None
	)

	def	__init__( self ):
		super( PrettyPrint, self ).__init__()
		self.pre_begin_file()
		return

	def	pre_begin_file( self, name = None ):
		self.widths = dict()
		self.mounts = dict()
		self.flavor = 'RANCID'
		return

	def	reorder( self, s ):
		return ','.join(
			sorted(
				s.split( ',' )
			)
		)

	def	set_widest( self, l ):
		for i in range( len( l ) ):
			self.widths[ i ] = max(
				self.widths.get( i, 0 ),
				len( l[ i ] )
			)
		return

	def	next_line( self, line ):
		# Tokenize input line
		tokens = map(
			str.strip,
			line.split()
		)
		N = len( tokens )
		if len( tokens ) != 6: return
		if tokens[ -1 ].isdigit():
				# tail -n1 /proc/mounts
				# binfmt_misc /proc/sys/fs/binfmt_misc binfmt_misc rw,relatime 0 0
				self.flavor = 'proc'
				fs          = tokens[ 0 ]
				mp          = tokens[ 1 ]
				kind        = tokens[ 2 ]
				opts        = self.reorder( tokens[ 3 ] )
				freq        = tokens[ 4 ]
				passno      = tokens[ 5 ]
				record      = [ fs, mp, kind, opts, freq, passno ]
		else:
			# mount | tail -n1
			# binfmt_misc on /proc/sys/fs/binfmt_misc type binfmt_misc (rw,relatime)
			self.flavor = 'cmd'
			fs     = tokens[ 0 ]
			mp     = tokens[ 2 ]
			kind   = tokens[ 4 ]
			opts   = self.reorder( tokens[ 5 ][1:-1] )
			record = [ fs, mp, kind, opts ]
		key = '{0},{1}'.format( mp, fs )
		if key in self.mounts:
			k = self.footnote(
				'{0} mounted multiple times'.format( key )
			)
			record += [
				'** See footnote {0}'.format( k )
			]
			print '*** collision "{0}"'.format( key )
			self._print_mounts()
		self.mounts[ key ] = record
		self.set_widest( record )
		return

	def	_print_mounts( self ):
		for key in sorted( self.mounts ):
			print '{0:31}  {1}'.format(
				key,
				'|'.join( self.mounts[ key ] )
			)
		return

	def	report( self, final = False ):
		if final: return
		if self.flavor == 'cmd':
			titles = [
				'Filesystem',
				'Mount Point',
				'Type',
				'Options',
			]
		elif self.flavor == 'proc':
			titles = [
				'Filesystem',
				'Mount Point',
				'Type',
				'Options',
				'Back Up',
				'fsck(8)',
			]
		else:
			self.error(
				'Flavor of the month is "[)]".'.format( self.flavor )
			)
			return
		self.set_widest( titles )
		fmts = map(
			'{{0:{0}}}'.format,
			[ self.widths[key] for key in self.widths ]
		)
		self.write_row( fmts, titles )
		bars = map(
			lambda s : '-' * len( s ),
			titles
		)
		self.write_row( fmts, bars )
		for key in sorted( self.mounts ):
			self.write_row( fmts, self.mounts[ key ] )
		return

	def	write_row( self, fmts, fields ):
		Lfmts   = len( fmts )
		Lfields = len( fields )
		gutter = '  '
		if Lfmts == Lfields:
			self.println(
				gutter.join(
					map(
						lambda i : fmts[i].format( fields[i] ),
						range( Lfields )
					)
				).rstrip()
			)
		return
