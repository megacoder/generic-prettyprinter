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

	def	pre_begin_file( self, fn = None ):
		super( PrettyPrint, self ).pre_begin_file( fn )
		self.entries = dict()
		self.ordered_keys = []
		return

	def	next_line( self, line ):
		tokens = map(
			str.strip,
			line.rstrip().split( ':' )
		)
		N = len( tokens )
		if N == 2:
			field  = tokens[0]
			detail = tokens[1].split()
			value  = detail[0]
			rest   = detail[1:]
			self.ordered_keys.append( field )
			self.entries[ field ] = dict(
				name  = field,
				value = value,
				rest  = rest,
				notes = []
			)
		return

	def	_get_entry( self, name, default = 0 ):
		return int(self.entries[name]['value']) if name in self.entries else default

	def	_add_note( self, key, s ):
		n = self.footnote( s )
		self.entries[key]['notes'].append( str(n) )
		return

	def	_infer_overcommit( self ):
		# Check for memory overcommit
		CommitLimit  = float( self._get_entry( 'CommitLimit' ) )
		Committed_AS = float( self._get_entry( 'Comitted_AS' ) )
		if CommitLimit > 0.0:
			ratio = (Committed_AS / CommitLimit) * 100.0
			if ratio > 0.0:
				self._add_note(
					'Committed_AS',
					'Memory commit ratio = {0:.2f}'.format( ratio )
				)
			if ratio > 100.0:
				self._add_note(
					'Committed_AS',
					'*** WORKING SET TOO LARGE: Committed_AS > CommitLimit ***'
				)
		return

	def	_infer_hugepages( self ):
		managed_memory  = self._get_entry( 'MemTotal' )
		managed_memory -= self._get_entry( 'HugePages_Total' )
		min_free_kbytes = int(
			( math.sqrt( managed_memory ) * 4.0 ) + 0.5
		)
		self._add_note(
			'MemTotal',
			'Default vm.min_free_kbytes = {0}'.format(
				min_free_kbytes
			)
		)
		recommended_min_free_kbytes = int(
			(managed_memory * 0.005) + 0.5
		)
		self._add_note(
			'MemTotal',
			'Recommended vm.min_free_kbytes = {0}'.format(
				recommended_min_free_kbytes
			)
		)
		return

	def	_infer_wasted_memory( self ):
		hp = self._get_entry( 'HugePages_Total' )
		hp -= self._get_entry( 'HugePages_Rsvd' )
		wasted = hp * self._get_entry( 'Hugepagesize' )
		if wasted > 0:
			self._add_note(
				'HugePages_Total',
				'Wasted physical memory {0}'.format( wasted )
			)
		return

	def	_infer_avail_memory( self ):
		avail = self._get_entry( 'MemTotal' ) - (
			self._get_entry( 'HugePages_Total' ) *
			self._get_entry( 'Hugepagesize' )
		)
		self._add_note(
			'MemTotal',
			'Physical memory not in HugePages: {0}'.format(
				avail
			)
		)
		return

	def	_infer_dom0_memory( self ):
		dom0mem = (
			502 + int(
				(self._get_entry( 'MemTotal' ) / 1024.0 * 0.0205) + 0.5
			)
		)
		self._add_note(
			'MemTotal',
			'Recommended memory if is dom0: {0}'.format(
				dom0mem
			)
		)
		return

	def	report( self, final = False ):
		if final: return
		self._infer_overcommit()
		self._infer_hugepages()
		self._infer_wasted_memory()
		self._infer_avail_memory()
		self._infer_dom0_memory()
		#
		keys = self.entries.keys()
		key_width = max(
			map(
				len,
				keys
			)
		)
		value_width = max(
			map(
				len,
				[
					self.entries[key]['value'] for key in self.entries
				]
			)
		)
		fmt = '{{0:{0}s}} {{1:>{1}s}} {{2:2s}} {{3}}'.format(
			key_width + 1,
			value_width
		)
		#
		self.println()
		for key in self.ordered_keys:
			self.println(
				fmt.format(
					'{0}:'.format( key ),
					self.entries[key]['value'],
					' '.join( self.entries[key]['rest'] ),
					', '.join( self.entries[key]['notes'] )
				)
			)
		return
