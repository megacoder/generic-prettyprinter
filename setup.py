#!/usr/bin/env python

VERSION	= '0.0.51'

from	distutils.core			import	setup
import	glob
import	os
from	DistUtilsExtra.command	import	*

setup(
	name             ='generic_prettyprinter',
	version          = VERSION,
	description      ='Generic Pretty Printer, using plugins',
	author           ='Tommy Reynolds',
	author_email     ='Tommy.Reynolds@MegaCoder.com',
	license          ='GPL',
	url              ='http://www.MegaCoder.com',
	long_description =open('README.txt').read(),
	packages         =['generic_prettyprinter' ],
	package_dir      ={ 'generic_prettyprinter':'src/gpp' },
	package_data     ={ 'generic_prettyprinter': [ 'plugins/*.py', '*.txt', '*.html' ] },
	scripts			=[ 'scripts/gpp' ],
)
