#!/usr/bin/python
# vim: noet ts=4 sw=4

import	os
import	sys
import	superclass
import	math

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	NAME = 'meminfo'
	DESCRIPTION="""Display /proc/meminfo in canonical style."""

	def	__init__( self ):
		super( PrettyPrint, self ).__init__()
		return

	def	reset( self ):
		super( PrettyPrint, self ).reset()
		self._prepare()
		return

	def	_prepare( self ):
		self.lines = []
		self.maxfield = 12
		return

	def	begin_file( self, name ):
		super( PrettyPrint, self ).begin_file( name )
		self._prepare()
		return

	def	next_line( self, line ):
		tokens = line.rstrip().split( ':' )
		if len(tokens) > 0:
			field = tokens[0].strip()
			value = tokens[1].strip()
			self.maxfield = max( self.maxfield, len(field) )
			values = value.split()
			# Some entries have no specific units specified
			if not value.endswith( 'kB' ):
				# Null units to make the columns line up
				values.append( '  ' )
			if len(values) >= 2 :
				self.lines.append( (field, values) )
		return

	def	_begin_notes( self ):
		self.first = True
		return

	def	_addto_notes( self, msg, val = None, fmt = None ):
		if self.first:
			self.first = False
			self.println()
			self.println( 'Observations about these values.' )
			self.println( '--------------------------------' )
		if val:
		    if not fmt:
			fmt = '{0:>14s}: {1}'
		    self.println(
			fmt.format(
			    val,
			    msg
			)
		    )
		else:
		    if not fmt:
			fmt = '{0}'
		    self.println(
			fmt.format( msg )
		    )
		return

	def	_end_notes( self ):
		return

	def	report( self, final = False ):
		if len(self.lines) == 0:
			self._prepare()
			return
		maxvalue = 12
		for (field,values) in self.lines:
			maxvalue = max( maxvalue, len(values[0]) )
		ffmt = '%%-%ds' % (self.maxfield+1)
		vfmt = '%%%ds %%s' % maxvalue
		fmt = ffmt + '	' + vfmt
		observed = {}
		for (field, values) in self.lines:
			observed[field] = int(values[0])
			self.println( fmt % (field + ':', values[0], values[1]) )
		self._begin_notes()
		try:
			if observed['Committed_AS'] > observed['CommitLimit']:
				self._addto_notes(
					'Committed_AS(%d)>CommitLimit(%d) suggests system overload.' % (
						observed['Committed_AS'],
						observed['CommitLimit']
					)
				)
		except Exception, e:
			self._addto_notes(
				'Could not check CommitLimit'
			)
			self._addto_notes(
				str(observed)
			)
			self._addto_notes( e )
		try:
			managed_memory = float( observed[ 'MemTotal' ] )
			if 'HugePages_Total' in observed:
			    managed_memory -= observed['HugePages_Total']
			min_free_kbytes = int(
			    (math.sqrt( managed_memory ) * 4.0) + 0.5
			)
			recommended_min_free_kbytes = int(
			    (managed_memory * 0.005) + 0.5
			)
			self._addto_notes(
			    'Default vm.min_free_kbytes',
			    val = '{0} kB'.format( min_free_kbytes )
			)
			self._addto_notes(
			    'Recommended vm.min_free_kbytes',
			    val = '{0} kB'.format(
				recommended_min_free_kbytes
			    )
			)
		except Exception, e:
			self._addto_notes(
				'Could not calculate default vm.min_free_kbytes'
			)
			self._addto_notes( e )
		try:
			if 'HugePages_Total' in observed:
				hp = observed['HugePages_Total']
				if 'HugePages_Rsvd' in observed:
					hp -= observed['HugePages_Rsvd']
				wasted_memory = hp * observed['Hugepagesize']
				if wasted_memory > 0:
				    self._addto_notes(
					'Physical memory in unused HugePages',
					val = '{0} kB ({1} pages)'.format(
					    wasted_memory,
					    hp
					)
				    )
		except Exception, e:
			self._addto_notes(
				'Could not calculate wasted hugepages space.'
			)
			self._addto_notes( e )
		try:
			if 'HugePages_Total' in observed:
				working_space = (
					observed['MemTotal'] - (
						observed['HugePages_Total'] * observed['Hugepagesize']
					)
				)
				self._addto_notes(
				    'Physical memory not in HugePages',
				    val = '{0} kB'.format( working_space )
				)
		except Exception, e:
			self._addto_notes(
				'Could not calculate available physical memory.'
			)
			self._addto_notes( e )
		try:
			dom0mem = (
				502 + int(
					(observed['MemTotal'] / 1024.0 * 0.0205) + 0.5
				)
			)
			self._addto_notes(
			    'Recommended memory if dom0',
			    val = '{0} MB'.format( dom0mem )
			)
		except Exception, e:
			self._addto_notes(
				'Could not calculate recommended dom0 partition size.'
			)
			self._addto_notes(
				e
			)
		self._end_notes()
		self._prepare()
		return
