#!/usr/bin/python
# vim: noet sw=4 ts=4

import	os
import	sys
import	string
import	superclass
import	shlex

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	NAME = 'multipath-pp'
	DESCRIPTION="""Display /etc/multipath.conf in conical style."""

	INDENT_WITH = ' ' * 8

	def __init__( self ):
		super( PrettyPrint, self ).__init__()
		return

	def	reset( self ):
		super( PrettyPrint, self ).reset()
		self.depth = 0
		self.do_capture = False
		self.captured = []
		return

	def _print_tokens( self, tokens, fmt = '{0} {1}'  ):
		if len( tokens ) > 0:
			leadin = PrettyPrint.INDENT_WITH * self.depth
			content = fmt.format( tokens[0], ' '.join( tokens[1:] ) )
			self.println( '{0}{1}'.format( leadin, content ) )
		return

	def	ignore( self, name ):
		ignore_it = False
		if os.path.isfile( name ) and not name.endswith( '.conf' ):
			ignore_it = True
		return

	def	begin_file( self, name ):
		super( PrettyPrint, self ).begin_file( name )
		self.depth = 0
		return

	def	_dump_captured_content( self ):
		fmt = '{0:<%ds} {1}' % self.width
		for tokens in sorted( self.captured, key = lambda t: t[0].lower() ):
			self._print_tokens( tokens, fmt = fmt )
		self.captured = []
		return

	def	next_line( self, line ):
		tokens = [x for x in shlex.shlex( line )]
		if len(tokens) > 0:
			keyword = tokens[0]
			final = tokens[-1]
			if final == '{':
				self._print_tokens( tokens )
				self.depth += 1
				if keyword in [
					'blacklist',
					'blacklist_exceptions',
					'device',
					'multipath',
					'defaults'
				]:
					self.captured = []
					self.do_capture = True
					self.width = 7
			elif final == '}':
				self._dump_captured_content()
				self.do_capture = False
				self.depth -= 1
				self._print_tokens( tokens )
			elif tokens[1] == '=':
				self._print_tokens( tokens )
			elif self.do_capture:
				self.width = max( self.width, len( keyword ) )
				if keyword in [ 'udev_dir' ]:
					args = ''.join( tokens[1:] )
				else:
					args = ' '.join( tokens[1:] )
				self.captured.append( [ keyword, args ] )
			else:
				# Silently discard
				print 'ignoring {0}'.format( tokens )
				pass
		return
