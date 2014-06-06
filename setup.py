#!/usr/bin/env python
# vim: noet sw=4 ts=4

VERSION	= '1.0.10'

from	distutils.core			import	setup
import	glob
import	os

setup(
	name             =	'generic_prettyprinter',
	version          =	VERSION,
	description      =	'Generic Pretty Printer, using plugins',
	author           =	'Tommy Reynolds',
	author_email     =	'Tommy.Reynolds@MegaCoder.com',
	license          =	'GPL',
	url              =	'http://www.MegaCoder.com',
	long_description =	open('README').read(),
	packages         =	[ 'generic_prettyprinter' ],
	package_dir      =	{ '' : 'src' },
	scripts          =	[ 'bin/gpp' ],
)
