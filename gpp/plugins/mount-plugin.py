#!/usr/bin/python
# vim: noet sw=4 ts=4

import	sys
import	os
import	stat

class	Mounts( object ):

	def	__init__( self ):
		self._reset()
		return

	def	_reset( self ):
		self.lines = []
		self.is_proc = False
		return

	def	do_name( self, name ):
		try:
			mode = os.stat( name )[stat.ST_MODE]
		except Exception, e:
			print >>sys.stderr, 'Cannot stat "%s".' % name
			raise e
		if stat.S_ISREG( mode ):
			self.do_file( name )
		elif stat.S_ISDIR( mode ):
			self.do_dir( name )
		else:
			print >>sys.stderr, 'Ignoring "%s".' % name
		return

	def	do_dir( self, dn ):
		try:
			files = os.listdir( dn )
		except Exception, e:
			print >>sys.stderr, 'Cannot read directory "%s".' % dn
			raise e
		files.sort()
		for file in files:
			self.do_name( os.path.join( dn, file ) )
		return

	def	do_file( self, fn ):
		try:
			f = open( fn, 'rt' )
		except Exception, e:
			print >>sys.stderr, 'Cannot read file "%s".' % fn
			raise e
		self._process( f )
		f.close()
		return

	def	_process( self, f = sys.stdin ):
		first = True
		for line in f:
			tokens = line.rstrip().split()
			n = len( tokens )
			if n != 6:
				print >>sys.stderr, 'Huh? %s' % line.rstrip()
			else:
				if first:
					self.is_proc = tokens[5].isdigit()
					first = False
				if self.is_proc:
					# /proc/mounts type of file.
					name   = tokens[0]
					mp     = tokens[1]
					type   = tokens[2]
					attr   = tokens[3].split( ',' )
					backup = tokens[4]
					fsck   = tokens[5]
				else:
					# /bin/mount type of file
					name   = tokens[0]
					mp     = tokens[2]
					type   = tokens[4]
					attr   = tokens[5][1:-1].split( ',' )
					backup = None
					fsck   = None
				attr.sort()
				self.lines.append(
					( name, mp, type, attr, backup, fsck )
				)
		return

	def	fini( self ):
		others = False
		fmt = '%-39s %s\n\ttype=%s\tattr=%s'
		self.lines.sort()
		for (name, mp, type, attr, backup, fsck) in self.lines:
			# print name, mp, type, ','.join(attr), backup, fsck
			if others:
				print
			others = True
			print fmt % (
				name,
				mp,
				type,
				','.join(attr)
			)
			if self.is_proc:
				print '\tbackup=%s\tfsck=%s' % (backup, fsck)
		return

if __name__ == '__main__':
	mpp = Mounts()
	if len(sys.argv) == 1:
		mpp._process()
	else:
		for fn in sys.argv[1:]:
			if fn == '-':
				mpp._process()
			else:
				mpp.do_name( fn )
	mpp.fini()
	exit(0)
