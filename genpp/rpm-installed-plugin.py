#!/usr/bin/python
# vim: noet sw=4 ts=4

import	os
import	sys
import	time
import	datetime
import	subprocess

import	superclass

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	NAME        = 'rpm-installed-pp'
	DESCRIPTION = """List date RPM packages were installed."""
	GLOB        = None

	def	__init__( self ):
		super( PrettyPrint, self ).__init__()
		return

	def	reset( self ):
		super( PrettyPrint, self ).reset()
		self.lines    = []
		self.max_name = 15
		return

	def	next_line( self, line ):
		self.do_line( line )
		return

	def	do_line( self, line ):
		tokens = map(
			str.strip,
			line.split()
		)
		if len(tokens) >= 3:
			when = tokens[0]
			name = tokens[1]
			self.max_name = max( self.max_name, len(name) )
			rest = tokens[2:]
			self.lines.append( (when, name, rest) )
		return

	def	do_it_myself( self ):
		cmd = [
			'/bin/rpm',
			'-qa',
			"--qf='%{INSTALLTIME} %{NAME} %{VENDOR}'\n"
		]
		try:
			for line in subprocess.check_output( cmd ).split( '\n' ):
				self.lines.append( l.strip() )
		except Exception, e:
			print >>sys.stderr, 'Cannot invoke "%s".' % cmd
			raise e
		return

	def	report( self, final = False ):
		if not final:
			if self.lines == []:
				self.do_it_myself()
			fmt = '%%s  %%-%ds  %%s' % self.max_name
			for (when, name, rest) in sorted(
				self.lines,
				key = lambda (when,name,rest): when
			):
				# stim = time.gmtime( int(when) )
				s = datetime.datetime.fromtimestamp( int(when) )
				self.println(
					fmt % ( s, name, ' '.join(rest) )
				)
		return
