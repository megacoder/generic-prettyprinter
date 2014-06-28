#!/usr/bin/env python
# vim: noet sw=4 ts=4

VERSION	= '1.0.12'

from	distutils.core			import	setup
import	glob
import	os

setup(
	name             =	'generic-prettyprinter',
	version          =	VERSION,
	description      =	'Generic Pretty Printer, using plugins',
	author           =	'Tommy Reynolds',
	author_email     =	'Tommy.Reynolds@MegaCoder.com',
	license          =	'GPL',
	url              =	'http://www.MegaCoder.com',
	long_description =	open('README').read(),
	packages         =	[ 'generic-prettyprinter' ],
	package_dir      =	{ 'generic-prettyprinter' : 'src' },
	scripts          =	[ 'bin/gpp' ],
)
