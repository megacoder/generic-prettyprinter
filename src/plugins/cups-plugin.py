#!/usr/bin/python
# vim: noet sw=4 ts=4

import	sys
import	os
from	superclass import MetaPrettyPrinter

class	PrettyPrint( MetaPrettyPrinter ):

	NAME	= 'cups-pp'
	DESCRIPTION = """Print cups configuration file."""

	def	__init__( self ):
		super(PrettyPrint, self).__init__()
		self.reset()
		return

	def	reset( self ):
		self.depth = 0
		self.comment_column = 40
		self.leadin = '  '
		return

	def	indent( self, content, comment ):
		# Indent content first
		line = (self.leadin * self.depth) + content
		# Align comments before writing line
		if len(comment) > 0:
			line = line + (' '*max( 1, 40 - len(line))) + '# ' + comment
		print line
		return

	def	process( self, fd = sys.stdin ):
		for line in fd:
			parts = line.strip().split( '#', 1 )
			l = len(parts)
			if l == 0:
				# Blank line
				print
				continue
			if l == 1:
				content = parts[0]
				comment = ''
			else:
				content = parts[0]
				comment = parts[1]
			content = parts[0]
			if len(content) == 0:
				# No content, treat comment as content
				self.indent( '#' + comment, '' )
				continue
			# Align args after command
			parts = content.split( ' ', 1 )
			if len(parts) == 1:
				verb = parts[0]
				args = ''
			else:
				verb = parts[0]
				args = parts[1]
			content = '%-15s %s' % (verb, args)
			if not content.startswith( '<' ):
				# Non-directive line
				self.indent( content, comment )
			else:
				# Directive line
				if content.startswith( '</' ):
					# pop: move left, then print end-directive
					self.depth = max( 0, self.depth - 1 )
					self.indent( content,  comment )
				else:
					# push: print, then move right
					parts = content[:-1].split()
					if len(parts) > 1:
						verb = parts[0]
						args = parts[1:]
						args.sort()
						content = '%-15s %s>' % ( verb, ' '.join(args))
					self.indent( content, comment )
					self.depth += 1
		return
