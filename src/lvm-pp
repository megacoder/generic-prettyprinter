#!/usr/bin/python
# vim: noet sw=4 ts=4

import	os
import	sys
import	string

class	LvmPrettyPrint( object ):

	INDENT_WITH = '        '

	def __init__( self ):
		self._reset()
		return

	def	_reset( self ):
		self.stanza = []
		self.max_name = 15
		return

	def	_process( self, f = sys.stdin ):
		for line in f:
			# Column-1 comments are copied verbatim
			if line.lstrip().startswith( '#' ):
				print line,
				continue
			# All other lines are to be correctly indented
			if line.find( '{' ) > -1:
				l = line.rstrip().replace( '{', ' { ' ).replace( '}', ' } ' )
				tokens = l.split()
				print '\t'.join( tokens )
				self._reset()
			elif line.find( '}' ) > -1:
				# Stanza ending
				fmt = '%%%ds = %%s' % self.max_name
				self.stanza.sort()
				for tokens in self.stanza:
					print fmt % ( tokens[0], ' '.join( tokens[1:] ) )
				#
				l = line.rstrip().replace( '{', ' { ' ).replace( '}', ' } ' )
				tokens = l.split()
				print '\t'.join( tokens )
				self._reset()
			else:
				tokens = line.rstrip().split( '=' )
				if len(tokens) != 2:
					print line,
					continue
				self.max_name = max( self.max_name, len(tokens[0]) )
				self.stanza.append( tokens )
		return

	def do_file( self, fn ):
		if not os.path.isfile( fn ): return
		f = open( fn, 'rt' )
		self._process( f )
		f.close()
		return

	def	do_dir( self, dn ):
		try:
			files = os.listdir( dn )
		except Exception, e:
			print >>sys.stderr, 'Cannot list directory "%s".' % dn
			raise e
		files.sort()
		for file in files:
			self.do_name( os.path.join( dn, file ) )
		return

	def	do_name( self, name ):
		if os.path.isfile( name ):
			self.do_file( name )
		elif os.path.isdir( name ):
			self.do_dir( name )
		else:
			# print >>sys.stderr, 'Ignoring "%s".' % name
			pass
		return

if __name__ == '__main__':
	lpp = LvmPrettyPrint()
	me = os.path.basename( sys.argv[0] )
	if len(sys.argv) == 1:
		lpp._process()
		# lpp.do_file( '/etc/multipath.conf' )
		# lpp.do_directory( '/etc/multipath.d' )
	else:
		for arg in sys.argv[1:]:
			if arg == '-':
				lpp._process()
			else:
				lpp.do_name( arg )
	exit(0)
