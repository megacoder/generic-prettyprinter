#!/usr/bin/env python

VERSION	= '0.0.34'

from	distutils.core			import	setup
import	glob
import	os
from	DistUtilsExtra.command	import	*

setup(
	name             ='gpp',
	version          = VERSION,
	description      ='Generic Pretty Printer, using plugins',
	author           ='Tommy Reynolds',
	author_email     ='Tommy.Reynolds@MegaCoder.com',
	license          ='GPL',
	url              ='http://www.MegaCoder.com',
	long_description =open('README.txt').read(),
	packages         =['generic-prettyprinter' ],
	package_dir      ={ 'generic-prettyprinter':'src/gpp' },
	package_data     ={ 'generic-prettyprinter': [ 'plugins/*.py', '*.txt', '*.html' ] },
	scripts			=[ 'scripts/gpp' ],
)
