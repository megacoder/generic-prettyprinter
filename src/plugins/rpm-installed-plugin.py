#!/usr/bin/python
import	os
import	sys
import	time
import	datetime

class	PrettyPrint( object ):
	def	__init__( self ):
		self.reset()
		return

	def	reset( self ):
		self.lines = []
		return

	def	process( self, f = None ):
		if f is None:
			import	subprocess
			cmd = [
				'/bin/rpm',
				'-qa',
				"--qf='%{INSTALLTIME} %{NAME} %{VENDOR}'\n"
			]
			print 'cmd=[%s]' % cmd
			try:
				p = subprocess.Popen( cmd, stdout=subprocess.PIPE )
				(odata,oerrors) = p.communicate()
				p.close()
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
				rest = tokens[2:]
				self.lines.append( (when, name, rest) )
		return

	def	finish( self ):
		self.lines.sort(
			key = lambda (when,name,rest): when
		)
		print self.lines
		for (when, name, rest) in self.lines:
			# stim = time.gmtime( int(when) )
			s = datetime.datetime.fromtimestamp( int(when) )
			print '%s  %-63s  %s' % (
				s,
				name,
				' '.join(rest)
			)
		return
