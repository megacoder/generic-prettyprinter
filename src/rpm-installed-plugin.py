#!/usr/bin/python
import	os
import	sys
import	time
import	datetime

import	superclass

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	NAME = 'rpm-installed-pp'
	DESCRIPTION="""List date RPM packages were installed."""

	def	__init__( self ):
		super( PrettyPrint, self ).__init__()
		return

	def	reset( self ):
		self.lines = []
		self.max_name = 15
		return

	def	process( self, f = None ):
		if f is None:
			import	subprocess
			cmd = [
				'/bin/rpm',
				'-qa',
				"--qf='%{INSTALLTIME} %{NAME} %{VENDOR}'\n"
			]
			try:
				odata = []
				for l in subprocess.check_output( cmd ).split( '\n' ):
					odata.append( l[1:-1] )
			except Exception, e:
				print >>sys.stderr, 'Cannot invoke "%s".' % cmd
				raise e
		else:
			odata = f.readlines()
		for line in odata:
			tokens = line.rstrip().split()
			if len(tokens) >= 3:
				when = tokens[0]
				name = tokens[1]
				self.max_name = max( self.max_name, len(name) )
				rest = tokens[2:]
				self.lines.append( (when, name, rest) )
		return

	def	finish( self ):
		self.lines.sort(
			key = lambda (when,name,rest): when
		)
		fmt = '%%s  %%-%ds  %%s' % self.max_name
		for (when, name, rest) in self.lines:
			# stim = time.gmtime( int(when) )
			s = datetime.datetime.fromtimestamp( int(when) )
			print fmt % (
				s,
				name,
				' '.join(rest)
			)
		return
