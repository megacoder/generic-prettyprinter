#!/usr/bin/python
# vim: noet ts=4 sw=4

import	os
import	sys
import	compileall
import	subprocess

class	Plugger():

	def	__init__( self ):
		self.suffix     = '-plugin.py'
		self.lsuffix    = len( self.suffix )
		self.plugins    = dict()
		self.debug_on	= True
		return

	def	run( self, cmd ):
		cli = '$ {0}'.format( ' '.join( cmd ) )
		try:
			rc = subprocess.check_call(
				cmd,
				stderr = subprocess.STDOUT,
				shell  = False
			)
			if rc == 0:
				output = [ 'OK' ]
			else:
				output = [ '** Exit code {0}'.format( rc ) ]
		except subprocess.CalledProcessError, e:
			output = [ 'Compilation failed' ]
		except Exception, e:
			print >>sys.stderr, cli
			raise e
		return output

	def	process( self, where ):
		for rootdir, dirs, names in os.walk( where ):
			candidates = [
				fn for fn in names if fn.endswith( self.suffix )
			]
			for fn in candidates:
				key = fn[:-self.lsuffix]
				self.plugins[ key ] = os.path.join( rootdir, fn )
		return

	def	report( self, final = False ):
		max_name = max(
			map(
				len,
				self.plugins
			)
		)
		fmt = '{{0:>{0}}} {{1}}'.format( max_name )
		for key in sorted( self.plugins ):
			fn = self.plugins[ key ]
			cmd = [
				'/bin/python',
				'-B',
				'-OO',
				'-u',
				'-c',
				'exit(0)',
				fn
			]
			output = self.run( cmd )
			for line in output:
				print fmt.format( key, line )
				key = ''
		return

if __name__ == '__main__':
	p = Plugger()
	if len(sys.argv) == 1:
		p.process( 'src' )
	else:
		for dn in sys.argv[1:]:
			p.process( dn )
	p.report()
	exit(0)

