#!/usr/bin/env python27
# vim: noet sw=4 ts=4

VERSION	= '1.0.59'

try:
	# If this works, you can use eggs
	from	setuptools				import	setup
	print 'Able to use EGG tools.'
except:
	# If this works, you get a tarball
	from	distutils.core			import	setup
	print 'Falling back to distutils.'

import	glob
import	os

with open( 'src/version.py', 'w' ) as f:
	print >>f, 'Version="{0}"'.format( VERSION )

setup(
	name             =	'gpp',
	version          =	VERSION,
	description      =	'Generic Pretty Printer, using plugins',
	author           =	'Tommy Reynolds',
	author_email     =	'Tommy.Reynolds@MegaCoder.com',
	license          =	'GPL',
	url              =	'http://www.MegaCoder.com',
	long_description =	open('README.md').read(),
	packages         =	[ 'gpp' ],
	package_dir      =	{ 'gpp' : 'src' },
	scripts          =	[ 'bin/gpp' ],
)
