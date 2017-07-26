#!/usr/bin/python
# vim: noet sw=4 ts=4

import	os
import	sys
import	superclass
import	align

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	NAME = 'slabinfo-pp'
	DESCRIPTION = """Display /proc/slabinfo in conical form."""

	def	__init__( self ):
		super( PrettyPrint, self ).__init__()
		return

	def	pre_begin_file( self ):
		self.items = align.Align( titles = 1 )
		return

	def	max_sizes( self, tokens ):
		i = 1
		for token in tokens:
			try:
				self.widths[i] = max( self.widths[i], len(token) )
			except:
				self.widths[i] = len(token)
			i += 1
		return

	def	next_line( self, line ):
		# print 'line=[%s]' % line
		if line.startswith( 'slabinfo' ):
			# Ignore version line
			pass
		elif line.startswith( '#' ):
			# Column titles
			tokens = [ '# name' ] + line.split()[2:]
			self.items.add( tokens )
		else:
			tokens = line.split()
			self.items.add( tokens )
		return

	def	report( self, final = False ):
		if not final:
			for _,items in self.items.get_items():
				self.println( ' '.join( items ) )
		return

if __name__ == '__main__':
	fn = '<selftest>'
	pp = PrettyPrint()
	pp.pre_begin_file()
	pp.begin_file( fn )
	for line in [

'slabinfo - version: 2.1',
'# name            <active_objs> <num_objs> <objsize> <objperslab> <pagesperslab> : tunables <limit> <batchcount> <sharedfactor> : slabdata <active_slabs> <num_slabs> <sharedavail>',
'nf_conntrack_expect      0      0    248   16    1 : tunables    0    0    0 : slabdata      0      0      0',
'nf_conntrack         682    800    320   25    2 : tunables    0    0    0 : slabdata     32     32      0',
'nfs_direct_cache       0      0    360   22    2 : tunables    0    0    0 : slabdata      0      0      0',
'nfs_commit_data       23     23    704   23    4 : tunables    0    0    0 : slabdata      1      1      0',
'nfs_inode_cache      310    310   1032   31    8 : tunables    0    0    0 : slabdata     10     10      0',
'fscache_cookie_jar     92     92     88   46    1 : tunables    0    0    0 : slabdata      2      2      0',
'xfs_dqtrx              0      0    528   31    4 : tunables    0    0    0 : slabdata      0      0      0',
'xfs_rui_item           0      0    664   24    4 : tunables    0    0    0 : slabdata      0      0      0',

	]:
		pp.next_line( line )
	pp.end_file( fn )
	pp.post_end_file()
	pp.report( final = True )

