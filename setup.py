#!/usr/bin/env python2
# vim: noet sw=4 ts=4

from	setuptools	import	setup

import	glob
import	os

NAME	= 'genpp'
VERSION = '2.0.7'

with open( '{0}/version.py'.format( 'genpp' ), 'w') as f:
	print >>f, 'Version="{0}"'.format( VERSION )

setup(
	name             =	NAME,
	version          =	VERSION,
	description      =	'Generic Pretty Printer, using plugins',
	author           =	'Tommy Reynolds',
	author_email     =	'Tommy.Reynolds@MegaCoder.com',
	license          =	'MIT',
	url              =	'http://www.MegaCoder.com',
	long_description =	open('README.md').read(),
	packages         =	[ 'genpp' ],
	package_dir      =	{
			'genpp': 'genpp'
	},
	scripts			 =	{
		"scripts/genpp",
	},
)
