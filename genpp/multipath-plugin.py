#!/usr/bin/python
# vim: noet sw=4 ts=4

import	os
import	sys
import	string
import	superclass
import	shlex
import	bunch

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	NAME = 'multipath-pp'
	DESCRIPTION="""Display /etc/multipath.conf in conical style."""

	INDENT_WITH = ' ' * 8

	def __init__( self ):
		super( PrettyPrint, self ).__init__()
		self.sections = bunch.Bunch()
		self.sections.defaults = [
			'polling_interval',
			'max_polling_interval',
			'multipath_dir',
			'find_multipaths',
			'verbosity',
			'reassign_maps',
			'path_selector',
			'path_grouping_policy',
			'uid_attribute',
			'prio',
			'prio_args',
			'features',
			'path_checker',
			'failback',
			'rr_min_io',
			'rr_min_io_rq',
			'rr_weight',
			'no_path_retry',
			'user_friendly_names',
			'flush_on_last_del',
			'max_fds',
			'checker_timeout',
			'fast_io_fail_tmo',
			'dev_loss_tmo',
			'queue_without_daemon',
			'bindings_file',
			'wwids_file',
			'prkeys_file',
			'log_checker_err',
			'reservation_key',
			'retain_attached_hw_handler',
			'detect_prio',
			'detect_checker',
			'hw_str_match',
			'force_sync',
			'deferred_remove',
			'config_dir',
			'delay_watch_checks',
			'delay_wait_checks',
			'missing_uev_wait_timeout',
			'skip_kpartx',
			'ignore_new_boot_devs',
			'retrigger_tries',
			'retrigger_delay',
			'new_bindings_in_boot',
			'remove_retries',
			'max_sectors_kb',
			'unpriv_sgio',
		]
		self.sections.blacklist = [
			'wwid',
			'devnode',
			'device',		# Yes, this is a section name!
		]
		self.sections.blacklist_exceptions = [
			'wwid',
			'devnode',
			'device',			# Yes, this is a section name!
		]
		self.sections.multipaths = [
			'wwid',
			'alias',
			'path_grouping_policy',
			'path_selector',
			'prio',
			'prio_args',
			'failback',
			'rr_weight',
			'flush_on_last_del',
			'user_friendly_names',
			'no_path_retry',
			'rr_min_io',
			'rr_min_io_q',
			'features',
			'reservation_key',
			'deferred_remove',
			'delay_watch_checks',
			'delay_wait_checks',
			'skip_kpartx',
			'max_sectors_kb',
			'unpriv_sgio',
		]
		self.sections.devices = [
			'vendor',
			'product',
			'product_blacklist',
			'alias_prefix',
			'hardware_handler',
			'path_grouping_policy',
			'uid_attribute',
			'path_selector',
			'path_checker',
			'prio',
			'prio_args',
			'features',
			'failback',
			'rr_weight',
			'no_path_retry',
			'user_friendly_names',
			'rr_min_io',
			'rr_min_io_rq',
			'fast_io_fail_tmo',
			'dev_loss_tmo',
			'flush_on_last_del',
			'retain_attached_hw_handler',
			'detect_prio',
			'deferred_remove',
			'delay_watch_checks',
			'delay_wait_checks',
			'skip_kpartx',
			'max_sectors_kb',
			'unpriv_sgio',
		]
		self.lines = list()
		return

	def	ignore( self, name ):
		boring = False
		if os.path.isfile( name ) and not name.endswith( '.conf' ):
			boring = True
		return boring
	def	next_line( self, line ):
		tokens = [
			t for t in shlex.split( line, posix = True, comments = True )
		]
		if len( tokens ):
			self.lines.append(
				(
					self.get_filename(),
					self.get_lineno(),
					line,
					tokens[0:1] + tokens[ 1: ],
				)
			)
		return

	def	new_node( self, name = None ):
		return bunch.Bunch(
			name     = name,
			tokens   = list(),
			attrs    = list(),
			children = list()
		)

	def	parse_lines( self ):
		stack = list()
		root = self.new_node()
		stack.append( root )
		for (fn,lno,line,tokens) in self.lines:
			node = stack[ -1 ]
			# print 'tokens={0}'.format( tokens )
			if tokens[ -1 ] == '{':
				child = self.new_node( tokens[ 0 ] )
				child.tokens = tokens
				node.children.append( child )
				stack.append( child )
			elif tokens[ 0 ] == '}':
				stack.pop()
			else:
				node.attrs.append( tokens )
		return	root

	def	quote( self, s ):
		return s if s.isalnum() else '"{0}"'.format( s )

	def	print_node( self, node, indent = 0 ):
		# print 'node={0}'.format( node )
		gutter = '  '
		if node.name:
			self.println(
				'{0}{1}'.format(
					gutter * indent,
					'\t'.join( node.tokens )
				)
			)
			indent += 1
		if len(node.attrs):
			width = max(
				map(
					lambda t: len( t[ 0 ] ),
					node.attrs
				)
			)
			fmt = '{{0:{0}}} {{1}}'.format( width )
			for attr in sorted(
				node.attrs,
				key = lambda t: t[ 0 ].lower()
			):
				self.println(
					'{0}{1}'.format(
						gutter * indent,
						fmt.format(
							attr[ 0 ],
							self.quote( ' '.join( attr[ 1: ]  ))
						)
					)
				)
		#
		for child in sorted(
			node.children,
			key = lambda b : b.name.lower()
		):
			self.print_node( child, indent )
		if node.name:
			indent -= 1
			self.println(
				'{0}}}'.format( gutter * indent )
			)
		return

	def	print_tree( self, root ):
		self.print_node( root )
		return

	def	report( self, final = False ):
		if final: return
		root = self.parse_lines()
		self.print_tree( root )
		return
