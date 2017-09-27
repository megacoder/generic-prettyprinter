#!/usr/bin/python
# vim: noet ts=4 sw=4

import	os
import	shlex
import	superclass
import	sys

class	PrettyPrint( superclass.MetaPrettyPrinter ):

	NAME = 'network-pp'
	DESCRIPTION="""Display /etc/sysconfig/network in canonical form."""

	def __init__( self ):
		super( PrettyPrint, self ).__init__()
		self.items = dict()
		self.notes = dict({
			'NOZEROCONF' :
			'Do not set a route for dynamic link-local addresses',
			'NETWORKDELAY' :
			'Delay N seconds after all nics are initialized.',
			'IPV6FORWARDING' : 'Control global forwarding of incoming '
				'IPv6 packets on all interfaces.',
			'IPV6_AUTOCONF' : 'Set default for device-based autoconfig.',
			'IPV6_ROUTER' : 'Set default for device-based host/route '
				'behaviour.',
			'IPV6_AUTOTUNNEL' : 'Control automatic IPv6 tunneling.',
			'IPV6_DEFAULTGW' : 'Add default route through specified '
				'gateway.',
			'IPV6_DEFAULTDEV' : 'Add default route through this device.',
			'IPV6_RADVD_PIDFILE' : 'PID file for controlling radvd.',
			'IPV6TO4_RADVD_PIDFILE' : 'PID file for controlling radvd.',
			'IPV6_RADVD_TRIGGER_ACTION' : 'How to trigger radvd.',
			'FORWARD_IPV4' : 'OBSOLETE - enable IP forwarding.',
			'NETWORKWAIT' : 'OBSOLETE - moved to systemd.',
			'HOSTNAME' : 'OBSOLETE - desired hostname.',
		})
		return

	def next_line( self, line ):
		tokens = [
			x for x in shlex.shlex( line )
		]
		if len(tokens) == 3 and tokens[1] == '=':
			name  = tokens[0]
			value = tokens[2]
			item  = dict({
				'name'	: name,
				'value' : value,
			})
			self.items[ name ] = item
		return

	def	report( self, final = False ):
		if final:
			pass
		else:
			width = max(
				map(
					len,
					self.items
				)
			)
			fmt = '{{0:>{0}s}} = {{1}}{{2}}{{1}}'.format( width )
			for item in sorted(
				self.items
			):
				entry = self.items[ item ]
				name  = entry['name']
				value = entry['value']
				if value[0] == "'" or value[0] == '"':
					value = value[1:-1]
				delim = '"' if "'" in value else "'"
				entry['code'] = fmt.format(
					name,
					delim,
					value,
				)
				entry['comment'] = self.notes.get( item.upper(), None )
				self.items[item] = entry
			#
			width = max(
				map(
					len,
					[ self.items[key]['code'] for key in self.items ]
				)
			)
			fmt = '{{0:{0}.{0}s}}{{1}}'.format( width )
			for key in sorted(
				self.items,
				key = lambda k : k.upper()
			):
				item = self.items[ key ]
				code = item[ 'code' ]
				comment = item[ 'comment' ]
				self.println(
					fmt.format(
						code,
						'  # {0}'.format( comment ) if comment else ''
					)
				)
		return
